import os
# open file for reading repo names
import json
import openpyxl
import openpyxl.workbook
import requests

# octopus server details
octopus_server_uri = "https://octopus.ltl.xpo.com"
octopus_api_key = os.environ["OCTOPUS_API_KEY"]

headers = {'X-Octopus-ApiKey': octopus_api_key}


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


def get_teamcity_builds():
    # Construct the URL to fetch all build configurations
    url = f"{TEAMCITY_BASE_URL}/app/rest/buildTypes"
     # Make a GET request to fetch all build configurations
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        # print(response.json())
        build_configurations = response.json()["buildType"]
        return build_configurations
    else:
        print('Error in getting builds')
        print(response)
        return []



fileName = 'teamcity_builds.xlsx'
xfile = openpyxl.load_workbook(fileName)
repo_sheet = xfile['Builds']


# Get the column index for the column named 'Column_Name'
Component_Name_index = get_column_index(repo_sheet, 'Component Name')
TeamCityBuildConfigurationName_index = get_column_index(repo_sheet, 'TeamCityBuildConfigurationName')

# Get spaces
projects = get_teamcity_builds()


for i, row in enumerate(repo_sheet):
    if i == 0:
        continue
    template = row[Component_Name_index].value

    if template == None:
        continue
    if row[TeamCityBuildConfigurationName_index].value:
        continue
    print(f'Checking for component = {template}')
    
    # Loop through projects
    matching_builds = []
    row_id =i
    # Loop through projects
    for j, project in enumerate(projects, i):
        # print(project)
        project_words = project['name'].split('-')
        # we need to match the third word to check for template value
        if len(project_words) >= 3 and template.lower() == project_words[2].lower():
             matching_builds.append(project['name'])
        #------------------------------
        elif template.lower() == project['name'].lower():
            matching_builds.append(project['name'])
        #------------------------------     
        else:
             
            project_template = project['name'].split(' ')
            # if template.lower() == "batchframework":
            # print(project['name'])
            if len(project_template) > 1:
                if template.lower() == "batchframework":
                    print(project['name'])
                if project_template[0].lower() == template.lower():
                    matching_builds.append(project['name'])


    first_project = True
    row_id =i
    if len(matching_builds) > 0:
        for project in matching_builds:
            if first_project:
                repo_sheet.cell(row=row_id+1, column= TeamCityBuildConfigurationName_index+1).value = project 
                first_project = False
            else:
                # print('Adding a new row before ', row_id)
                repo_sheet.insert_rows(row_id+1)
                repo_sheet.cell(row=row_id+1, column= TeamCityBuildConfigurationName_index+1).value = project 
            row_id += 1
    else:
        repo_sheet.cell(row=row_id+1, column= TeamCityBuildConfigurationName_index+1).value = "NA"         
            
print('Done')
xfile.save(fileName)