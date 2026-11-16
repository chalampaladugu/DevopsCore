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


def get_column_index(sheet, column_name):
    for cell in sheet[1]:
        if cell.value == column_name:
            return cell.column-1




def get_octopus_resource(uri, headers, skip_count = 0):
    items = []
    skip_querystring = ""

    if '?' in uri:
        skip_querystring = '&skip='
    else:
        skip_querystring = '?skip='

    response = requests.get((uri + skip_querystring + str(skip_count)), headers=headers)
    response.raise_for_status()

    # Get results of API call
    results = json.loads(response.content.decode('utf-8'))

    # Store results
    if hasattr(results, 'keys') and 'Items' in results.keys():
        items += results['Items']

        # Check to see if there are more results
        if (len(results['Items']) > 0) and (len(results['Items']) == results['ItemsPerPage']):
            skip_count += results['ItemsPerPage']
            items += get_octopus_resource(uri, headers, skip_count)

    else:
        return results

    
    # return results
    return items

def get_ocotpus_projects(spaces):
    print('Fetching All octopus projects')
    projects = []
    # Loop through spaces
    for space in spaces:
        # Get all projects
        # print(f'Getting all projects in space {space['Id']}')
        uri = '{0}/api/{1}/projects'.format(octopus_server_uri, space['Id'])
        projects.extend(get_octopus_resource(uri, headers))
        
        # print(len(projects))
    return projects



fileName = 'octopus_builds.xlsx'
xfile = openpyxl.load_workbook(fileName)
repo_sheet = xfile['Builds']


# Get the column index for the column named 'Column_Name'
Component_Name_index = get_column_index(repo_sheet, 'Component Name')
OctopusBuildConfigurationName_index = get_column_index(repo_sheet, 'OctopusBuildConfigurationName')

# Get spaces
uri = '{0}/api/spaces'.format(octopus_server_uri)
spaces = get_octopus_resource(uri, headers)
octopus_projects = get_ocotpus_projects(spaces)

from copy import deepcopy
projects = deepcopy(octopus_projects)

for i, row in enumerate(repo_sheet):
    # print("doing for row ", i)
    if i == 0:
        continue
    # print('Component_Name_index', Component_Name_index)
    # print(row)
    template = row[Component_Name_index].value  
    if template == None:
        continue

    # print('Project= ', row[OctopusBuildConfigurationName_index].value)
    if row[OctopusBuildConfigurationName_index].value:
        continue
     
    print(f'Checking for component = {template}')
    
    matching_builds = []
    # Loop through projects
    for j, project in enumerate(projects, i):
        project_words = project['Name'].split('-')
        # we need to match the third word to check for template value
        if len(project_words) >= 3 and template.lower() == project_words[2].lower():
            matching_builds.append(project['Name'])
        #------------------------------
        elif template.lower() == project['Name'].lower():
            matching_builds.append(project['Name'])

        #------------------------------

    first_project = True
    row_id =i
    if len(matching_builds) > 0:
        for project in matching_builds:
            if first_project:
                repo_sheet.cell(row=row_id+1, column= OctopusBuildConfigurationName_index+1).value = project 
                first_project = False
            else:
                print('Adding a new row before ', row_id)
                repo_sheet.insert_rows(row_id+1)
                repo_sheet.cell(row=row_id+1, column= OctopusBuildConfigurationName_index+1).value = project 
            row_id += 1
    else:
        repo_sheet.cell(row=row_id+1, column= OctopusBuildConfigurationName_index+1).value = "NA" 
    # row[OctopusBuildConfigurationName_index].value = '\n'.join(matching_builds)

print('Done')
xfile.save(fileName)