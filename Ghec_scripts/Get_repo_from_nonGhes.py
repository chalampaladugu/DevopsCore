import os
from openpyxl import Workbook
from github import Github


import openpyxl

def get_column_index(sheet, column_name):
    for cell in sheet[1]:
        if cell.value == column_name:
            return cell.column-1

def get_repo_size(repo):
    repo_size_kb = repo.size
    return repo_size_kb / 1024  # Convert kilobytes to megabytes

def main():
    source_org="OneXPO"
    username="venkata-paladugu"
    password=os.environ["GHES_TOKEN"]


    source_github = Github(base_url="https://github.xpo.com/api/v3".format(source_org), login_or_token=username, password=password)
    # Initialize Excel workbook and worksheet
    wb = Workbook()
    # ws = wb.active
    file_name = "github_repos_non_xpo.xlsx"
    sheet_name= "Repo-list-1"
    xfile = openpyxl.load_workbook(file_name)

    repo_sheet = xfile.get_sheet_by_name(sheet_name)
    
    # Get the column index for the column named 'Column_Name'
    org_name_index = get_column_index(repo_sheet, 'Organization')
    repo_name_index = get_column_index(repo_sheet, 'Repository Name')
    migration_eligible_index = get_column_index(repo_sheet, 'MigrationEligible')
    migration_status_index = get_column_index(repo_sheet, 'MigrationStatus')
    open_pr_index = get_column_index(repo_sheet, 'Open PR Count')
    repo_size_index = get_column_index(repo_sheet, 'Size Of the Repo in MB')

    existing_repo = []
    repo_row = 2
    while repo_sheet['B'+str(repo_row)].value:
        # print(sheet['A'+str(row)].value)
        existing_repo.append(repo_sheet['B'+str(repo_row)].value)
        repo_row += 1
    row=2

    # Get all repositories
    print('checking for all repo in ', source_org)
    repo_obj_list = source_github.get_user().get_repos()
    # for repo in repo_obj_list:
    #     print(repo.organization.login)
    print(repo_obj_list.totalCount)
    
    for repo in repo_obj_list:
        if repo.name not in existing_repo:
            print('repo not found=',repo.name)
            # repo_sheet.append([repo.name])
            # row[org_name_index].value = repo.organization.login
            # row[repo_name_index].value = repo.name
            # row[open_pr_index].value = repo.get_pulls(state='open').totalCount
            # row[repo_size_index].value =  get_repo_size(repo)
            repo_sheet['A'+str(repo_row)] = repo.organization.login
            repo_sheet['B'+str(repo_row)] = repo.name
            # open_pr_count = repo.get_pulls(state='open').totalCount   
            # repo_size = get_repo_size(repo)
            # repo_sheet['C'+str(repo_row)] = open_pr_count
            # repo_sheet['D'+str(repo_row)] = repo_size
            repo_row += 1

   # Save Excel file
    xfile.save(filename=file_name)



   

main()  