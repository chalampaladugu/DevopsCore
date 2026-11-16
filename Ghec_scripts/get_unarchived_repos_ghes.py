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
    # fileConversion.json_to_xlsx('masterMigration.json','github_repos1.xlsx')
    xfile = openpyxl.load_workbook('github_repos.xlsx')

    repo_sheet = xfile.get_sheet_by_name('GitHub Repositories')
    # migrated_sheet = xfile.get_sheet_by_name('MigrationCompleted')
    # Get the column index for the column named 'Column_Name'

    repo_name_index = get_column_index(repo_sheet, 'Repository Name')
    migration_eligible_index = get_column_index(repo_sheet, 'MigrationEligible')
    migration_status_index = get_column_index(repo_sheet, 'MigrationStatus')
    open_pr_index = get_column_index(repo_sheet, 'Open PR Count')
    repo_size_index = get_column_index(repo_sheet, 'Size Of the Repo in MB')

    existing_repo = []
    repo_row = 2
    while repo_sheet['A'+str(repo_row)].value:
        # print(sheet['A'+str(row)].value)
        existing_repo.append(repo_sheet['A'+str(repo_row)].value)
        repo_row += 1
    row=2
    # while migrated_sheet['A'+str(row)].value:
    #     # print(sheet['A'+str(row)].value)
    #     existing_repo.append(migrated_sheet['A'+str(row)].value)
    #     row += 1

    # Get all repositories
    print('checking for all repo')
    for repo in source_github.get_user('OneXPO').get_repos():
       if not repo.archived:
           print(repo.name)
      
#         if repo.name not in existing_repo:
#             print('repo not found=',repo.name)
#             # repo_sheet.append([repo.name])
#             repo_sheet['A'+str(repo_row)] = repo.name
#             open_pr_count = repo.get_pulls(state='open').totalCount   
#             repo_size = get_repo_size(repo)
#             repo_sheet['B'+str(repo_row)] = open_pr_count
#             repo_sheet['C'+str(repo_row)] = repo_size
#             # row[open_pr_index].value = open_pr_count
#             # row[repo_size_index].value = repo_size
#             repo_row += 1

#    # Save Excel file
#     xfile.save(filename="github_repos.xlsx")
    # fileConversion.xlsx_to_json('github_repos.xlsx','masterMigration.json')

    # repos_to_be_migrated = []
    # for row in repo_sheet:
    #     if row[migration_eligible_index].value and row[migration_eligible_index].value.lower() == "yes" and row[migration_status_index].value == None:
    #         repos_to_be_migrated.append(row[repo_name_index].value)
    #         print(row[repo_name_index].value, row[migration_eligible_index].value, row[migration_status_index].value)
    # print(repos_to_be_migrated)


   

main()  