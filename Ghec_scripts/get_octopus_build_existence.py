import os
import json
import openpyxl
import requests
from requests.api import get, head
import datetime
from dateutil.parser import parse
from copy import deepcopy

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

# octopus_server_uri = 'https://YourURL'
# octopus_api_key = 'API-YourAPIKey'



octopus_server_uri = "https://octopus.ltl.xpo.com"
octopus_api_key = os.environ["OCTOPUS_API_KEY"]

headers = {'X-Octopus-ApiKey': octopus_api_key}
old_projects = []
current_date = datetime.datetime.now()
days_since_last_release = 90

# Get spaces
uri = '{0}/api/spaces'.format(octopus_server_uri)
spaces = get_octopus_resource(uri, headers)

# open file for reading repo names
filename = 'octopus_builds_exists.xlsx' 
xfile = openpyxl.load_workbook(filename)
repo_sheet = xfile.get_sheet_by_name('Builds')

def get_column_index(sheet, column_name):
    for cell in sheet[1]:
        if cell.value == column_name:
            return cell.column-1

ComponentName_index = get_column_index(repo_sheet, 'Component Name')
OctopusBuildConfigurationName_index = get_column_index(repo_sheet, 'OctopusBuildConfigurationName')
AttachDetachSteps_index = get_column_index(repo_sheet, 'Attach-Detach-Steps')
COMPLETED = "Completed"
ELIGIBLE = "yes"

def get_ocotpus_project(spaces, project_name):
    project = {}
    # Loop through spaces
    for space in spaces:
        print(f'Getting project in space {space['Id']}')
        uri = f'{octopus_server_uri}/api/{space['Id']}/projects/{project_name}'
        response = requests.get(uri, headers=headers)
        if response.status_code == 200:
            project = response.json()
            break
    return project


def get_step_list_to_update_property():
    return [item[0] for item in step_to_property_key.keys()]


def get_name_to_slug_map():
    project_url = f'{octopus_server_uri}/api/Spaces-1/projects/all'

    response = requests.get(project_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve step project details. Status code: {response.status_code}")
        return {}
    
    # Get the current project details
    response = response.json()
    build_slug_map = {}
    for project in response:
        build_slug_map[project["Name"]] = project['Slug']
    
    return build_slug_map
    
def is_cloud_step_present(step_name, step_list):
    cloud_step_name = migration_steps.get(step_name)
    if cloud_step_name in step_list:
        return True
    else:
        return False

# step_to_update_properties = get_step_list_to_update_property()
name_to_slug_map = get_name_to_slug_map()

for i, row in enumerate(repo_sheet):
    if i == 0:
        continue
    
    if  row[OctopusBuildConfigurationName_index].value and not row[AttachDetachSteps_index].value:
        build_name = row[OctopusBuildConfigurationName_index].value.strip()
        print(f'Processing for index {i} repo = {build_name}')
 
        build_name = name_to_slug_map.get(build_name, build_name)
 
        project = get_ocotpus_project(spaces, build_name)
        
        if not project:
            continue
        row[AttachDetachSteps_index].value = 'Yes'

xfile.save(filename)
xfile.close()