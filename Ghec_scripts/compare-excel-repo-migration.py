import openpyxl


def get_column_index(sheet, column_name):
    for cell in sheet[1]:
        if cell.value == column_name:
            return cell.column-1


team_xfile = openpyxl.load_workbook('GitHub Team Migration.xlsx')
# team_sheet = team_xfile.get_sheet_by_name('CTY SHM PKR')
team_sheet = team_xfile.get_sheet_by_name('Missed')

github_file_name = 'github_repos.xlsx'
xfile = openpyxl.load_workbook(github_file_name)
github_repo_sheet = xfile.get_sheet_by_name('GitHub Repositories')
# Get the column index for the column named 'Column_Name'

repo_name_index = get_column_index(github_repo_sheet, 'Repository Name')
migration_eligible_index = get_column_index(github_repo_sheet, 'MigrationEligible')


num_repos_found = 0
num_repos_not_found = 0
for team_row in team_sheet:
    first_row = True
    for github_repo in github_repo_sheet:
        if first_row:
            first_row = False
            continue

        found = False

        if github_repo[repo_name_index].value.lower() == team_row[0].value.lower():
            github_repo[migration_eligible_index].value = "Needs to Check"
            # print(github_repo[repo_name_index].value)
            found = True
            num_repos_found += 1
            break
        
    if not found:
        print(f"{team_row[0].value} not found !!")
        num_repos_not_found+=1

print(f"Number of repos found = {num_repos_found}")
print(f"Number of repos not  found = {num_repos_not_found}")
xfile.save(github_file_name)
xfile.close()
team_xfile.close()

