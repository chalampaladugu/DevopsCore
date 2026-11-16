import os
import requests
from openpyxl import Workbook
import openpyxl


username="venkata-paladugu"
password=os.environ["GHES_TOKEN"]

def get_org_repos(org_name):
    # GitHub API URL for the organization's repositories
    url = f"https://github.xpo.com/api/v3/users/{org_name}/repos"
    
    # Sending a GET request to the GitHub API
    response = requests.get(url, auth=(username, password))
    
    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the JSON response
        repos = response.json()
        # Extracting the names of the repositories
        repo_names = [repo['name'] for repo in repos]
        return repo_names
    else:
        # Handling possible errors
        return f"Failed to fetch repositories: {response.status_code}"


wb = Workbook()
# ws = wb.active
file_name = "github_repos_non_xpo.xlsx"
sheet_name= "Repo-list"
xfile = openpyxl.load_workbook(file_name)

repo_sheet = xfile.get_sheet_by_name(sheet_name)
repo_row = 2
# Example usage
org_name = ("AnsibleWorkshop","Enterprise-Architecture","XPO-DevOps","XPO-GCC","XPO-Networking","XPO-Platform-Engineering","XPO-VSE","eicoe","githubschool","xpo-automation","xpo-infosec")


for org in org_name:
    repos = get_org_repos(org)
    print(f"Repositories in the {org} organization:")
    # for repo in repos:
    #     print(repo)
    
    for repo in repos:
        repo_sheet['A'+str(repo_row)] = org
        repo_sheet['B'+str(repo_row)] = repo
        # open_pr_count = repo.get_pulls(state='open').totalCount   
        # repo_size = get_repo_size(repo)
        # repo_sheet['C'+str(repo_row)] = open_pr_count
        # repo_sheet['D'+str(repo_row)] = repo_size
        repo_row += 1
xfile.save(filename=file_name)
print('Done')