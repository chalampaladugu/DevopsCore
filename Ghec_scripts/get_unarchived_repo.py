import os
import openpyxl
from github import Github

target_github = Github(base_url="https://api.github.com", login_or_token='venkata.paladugu_xpo', password=os.environ["GITHUB_COM_TOKEN"])
target_org = target_github.get_organization('xpo-org')
source_github = Github(base_url="https://github.xpo.com/api/v3".format('OneXPO'), login_or_token='venkata-paladugu', password=os.environ["GHES_TOKEN"])
source_org = source_github.get_organization('OneXPO')

def get_column_index(sheet, column_name):
    for cell in sheet[1]:
        if cell.value == column_name:
            return cell.column-1

def archive_repo(repo_name):
    source_repo = source_org.get_repo(repo_name)

    # Archive the repository
    source_repo.edit(archived=True)
    return source_repo.archived

def main():  
    # repos = source_org.get_repos()
    for repo in source_github.get_user().get_repos():
        print(repo)
        if not repo.archived:
            print(repo.name)
        
main()
