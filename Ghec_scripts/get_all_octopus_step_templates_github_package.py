import os
import requests


octopus_server_uri = "https://octopus.ltl.xpo.com"
octopus_api_key = os.environ["OCTOPUS_API_KEY"]

def get_all_templates(octopus_uri, api_key):
    headers = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        "X-Octopus-ApiKey": api_key
    }
    response = requests.get(f"{octopus_uri}/api/actiontemplates/all", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get the step template")
        return None
    
res = get_all_templates(octopus_server_uri, octopus_api_key)
for template in res:
    packages = template.get('Packages')
    if not packages:
        continue
    package_id = packages[0].get('PackageId')
    # print(package_id)
    if package_id and ("#{gitHubPackage}" == package_id or "OneXPO/" in package_id):
        print(f'{template['Name']}')