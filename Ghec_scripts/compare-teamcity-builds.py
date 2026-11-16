from openpyxl import Workbook
from github import Github
import openpyxl


def get_column_index(sheet, column_name):
    for cell in sheet[1]:
        if cell.value == column_name:
            return cell.column-1

teamcity_builds_file = openpyxl.load_workbook('teamcity_builds.xlsx')
master_tc_builds_file = openpyxl.load_workbook('master_teamcity_builds.xlsx')

teamcity_repo_sheet = teamcity_builds_file.get_sheet_by_name('Builds')
master_tc_repo_sheet = master_tc_builds_file.get_sheet_by_name('Builds')

tc_repo_name_index = get_column_index(teamcity_repo_sheet, 'TeamCityBuildConfigurationName')
master_tc_repo_name_index = get_column_index(master_tc_repo_sheet, 'TeamCityBuildConfigurationName')

tc_attach_index = get_column_index(teamcity_repo_sheet, 'Attach-Detach-Templates')
master_tc_attach_index = get_column_index(master_tc_repo_sheet, 'Attach-Detach-Templates')


tc_attached_list = []
print('Preparing list of attached repo.')
first_row = True
for tc_row in teamcity_repo_sheet:
   if first_row:
      first_row = False
      continue

   tc_attached_list.append(tc_row[tc_repo_name_index].value)

print('Comapring the list of attached repo.')
first_row = True
for master_row in master_tc_repo_sheet:
   if first_row:
       first_row = False
       continue

   if master_row[master_tc_repo_name_index].value not in tc_attached_list:
       master_row[master_tc_attach_index].value = "Not attached(GHEC)"
   else:
       master_row[master_tc_attach_index].value = "Attached(GHEC)"

print('Comapring done.')
master_tc_builds_file.save('master_teamcity_builds.xlsx')