import requests
import json
import openpyxl 
import logging
# logging.basicConfig(f'__file__')
#templates-unused

TEAMCITY_BASE_URL = 'http://dev-teamcity-gke.ltl.xpo.com:8080'
API_TOKEN = 'eyJ0eXAiOiAiVENWMiJ9.eFAzOGdtWl80Vk5PM2JwTUE4amVaMkYzUjlJ.ZDZlODFiNGUtZTU3Yy00NGY3LWJlODQtNmQ5N2UzNzQ3MmRl' # TODO: Enter the API key from TeamCity
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

def get_column_index(sheet, column_name):
    for cell in sheet[1]:
        if cell.value == column_name:
            return cell.column-1

def get_templates_from_project(project_id):
    url = f"{TEAMCITY_BASE_URL}/app/rest/projects/{project_id}/templates"
    response = requests.get(
        url=url,
        headers=HEADERS,
    )
    response.raise_for_status()
    templates = response.json()
    
    return templates

# def delete_template(template_id):
#     # url = f"{TEAMCITY_BASE_URL}/app/rest/projects/{project_id}/templates"
#     url = f"{TEAMCITY_BASE_URL}/app/rest/buildtypes/id:{template_id}"
#     response = requests.delete(
#         url=url,
#         headers=HEADERS,
#     )
#     # response.raise_for_status()
#     print(response)

def get_build_type(build_type_id):
    url = f"{TEAMCITY_BASE_URL}/app/rest/buildTypes/id:{build_type_id}"
    response = requests.get(
        url=url,
        headers=HEADERS
    )
    response.raise_for_status()
    build_type = response.json()
    print(build_type)
    return build_type



def get_all_projects(test_run=False):
    if test_run:
        return {
            'project': [
                {'id' : 'XpoLtl_Java_Development'}
            ]
        }
    url = f'{TEAMCITY_BASE_URL}/app/rest/projects'
    response = requests.get(url=url, headers=HEADERS)
    response.raise_for_status()
    projects = response.json()
    return projects

# Function to get usage statistics for each template
def get_template_usage(template_id):
    # response = requests.get(TEAMCITY_BASE_URL + f'/app/rest/builds?locator=affectedProject:(id:{template_id})', auth=auth)
    # url = f'{TEAMCITY_BASE_URL}/app/rest/builds?locator=affectedProject:(id:{template_id})'
    url = f'{TEAMCITY_BASE_URL}/app/rest/buildTypes/template:(templateFlag:true,id:{template_id})'
    response = requests.get(url=url, headers=HEADERS)
    if response.status_code == 200:
        builds = response.json()['builds']
        return len(builds)
    return -1


fileName = 'templates-unused.xlsx'
xfile = openpyxl.load_workbook(fileName)
repo_sheet = xfile['templates']
# Get the column index for the column named 'Column_Name'
# Component_Name_index = get_column_index(repo_sheet, 'Component Name')
TemplateName_index = get_column_index(repo_sheet, 'Template Name')
TemplateId_index = get_column_index(repo_sheet, 'Template Id')
UsedStatus_index = get_column_index(repo_sheet, 'Used Status')

projects = get_all_projects()
sheet_row = 2
print('Starting analysing projects..')
for project in projects['project']:
    project_id = project['id']
    templates = get_templates_from_project(project_id)

    for row_id, template in enumerate(templates['buildType'], sheet_row):
        usage = get_template_usage(template['id'])
        repo_sheet.cell(row=row_id, column=TemplateName_index+1).value = template['name']
        repo_sheet.cell(row=row_id, column=TemplateId_index+1).value = template['id']
        sheet_row=row_id+1
        if usage == -1 or usage == 0:
            #  print('Unused Template Name=',template['name'])
            repo_sheet.cell(row=row_id, column=UsedStatus_index+1).value ='Unused'
        else:
            repo_sheet.cell(row=row_id, column=UsedStatus_index+1).value ='Used'

xfile.save(fileName)
xfile.close()
print('Done')
