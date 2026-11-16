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



fileName = 'master_teamcity_builds.xlsx'
xfile = openpyxl.load_workbook(fileName)
repo_sheet = xfile['Builds']


# Get the column index for the column named 'Column_Name'
# Component_Name_index = get_column_index(repo_sheet, 'Component Name')
TeamCityBuildConfigurationName_index = get_column_index(repo_sheet, 'TeamCityBuildConfigurationName')

print('Fetching all the teamcity builds')
# Get spaces
projects = get_teamcity_builds()

# Loop through projects
print(f'Saving project name in {fileName}')
for j, project in enumerate(projects, 2):
    # print(project)

    repo_sheet.cell(row=j, column= TeamCityBuildConfigurationName_index+1).value = project['name']
            
print('Done')
xfile.save(fileName)