import requests
import threading
import openpyxl



#TeamCityBuildConfigurationName

TEAMCITY_BASE_URL = 'http://dev-teamcity-gke.ltl.xpo.com:8080'
API_TOKEN = 'eyJ0eXAiOiAiVENWMiJ9.eFAzOGdtWl80Vk5PM2JwTUE4amVaMkYzUjlJ.ZDZlODFiNGUtZTU3Yy00NGY3LWJlODQtNmQ5N2UzNzQ3MmRl' # TODO: Enter the API key from TeamCity
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
build_name_list = []

repo_build_config = {}
build_config_from_vcs_root = {}
repo_with_templates = []
# ROW4_VALUE = "Get List of Team City Builds"

def get_column_index(sheet, column_name):
    for cell in sheet[1]:
        if cell.value == column_name:
            return cell.column-1




def get_all_build_configs():
    # Construct the URL to fetch all build configurations
    url = f"{TEAMCITY_BASE_URL}/app/rest/buildTypes"

    # Make a GET request to fetch all build configurations
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        build_configurations = response.json()["buildType"]
    else:
        print(f"Failed to fetch build configurations. Status code: {response.status_code}")
        return None

def get_vcs_root_for_build(lock, build_config_id, build_name):
    global build_name_list
    vcs_endpoint = f"{TEAMCITY_BASE_URL}/app/rest/buildTypes/id:{build_config_id}/vcs-root-entries"

    # Make a GET request to fetch VCS roots
    vcs_response = requests.get(vcs_endpoint, headers=HEADERS)
    vcs_response.raise_for_status()

    # Parse VCS roots response JSON
    vcs_roots = vcs_response.json()
    # print(vcs_roots)
    vcs_root_ids = vcs_roots['vcs-root-entry']
    vcs_contains_ghec = False
    vcs_root_name = "GCP-Teamcity-Auth-ghec"
    for root in vcs_root_ids:
        name = root['vcs-root']['name']
        if name == vcs_root_name:
            build_name_list.append(build_name)
 
       
    return build_name_list
 

def get_build_configuration_parameters():
    global build_name_list
    # Construct the URL to fetch all build configurations
    url = f"{TEAMCITY_BASE_URL}/app/rest/buildTypes"

    # Make a GET request to fetch all build configurations
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        build_configurations = response.json()["buildType"]
        param_lock = threading.Lock()
        root_lock = threading.Lock()
        param_thread_list = []
        vcs_thread_list = []

        # Iterate through each build configuration
        print("Reading all build configs...")
        import datetime        
        for build_config in build_configurations:
            build_config_id = build_config["id"]
           
            t = threading.Thread(target=get_vcs_root_for_build, args=(root_lock, build_config_id, build_config['name']))
            vcs_thread_list.append(t)
            # # Get parameters for the current build configuration
            # t = threading.Thread(target=get_build_configuration_parameters_by_id, args=(param_lock, build_config_id, build_config['name']))
            # param_thread_list.append(t)
        
        # starting threads
        print('Start VCS Thread ', datetime.datetime.now())
        for th in vcs_thread_list:
            th.start()
        for th in vcs_thread_list:
            th.join()
        # print('Start param Thread ', datetime.datetime.now())
        # for th in param_thread_list:
        #     th.start()
        # for th in param_thread_list:
        #     th.join()

        print("Reading Done")
        print('Done VCS Thread ', datetime.datetime.now())
        return build_name_list
    else:
        print(f"Failed to fetch build configurations. Status code: {response.status_code}")
        return None


def main():
    # filename = 'teamcity_builds_noGHEC.xlsx'
    # xfile = openpyxl.load_workbook(filename)
    # repo_sheet = xfile.get_sheet_by_name('Builds')
    # build_configs = get_build_configs(repo_sheet)
# 
    # TeamcityBuildConfigurationName_index = get_column_index(repo_sheet, 'TeamCityBuildConfigurationName')
    
    build_without_ghec_vcs = get_build_configuration_parameters()
    print(build_without_ghec_vcs)
    # get_vcs_root_for_build(True, 'XpoLtl_Angular_Version8_Common_PfmExtract', 'PFM-Extract')

    # if build_without_ghec_vcs:
    #     for row_num, build in enumerate(build_without_ghec_vcs, 2):
    #         repo_sheet.cell(row= row_num, column = TeamcityBuildConfigurationName_index+1).value = build
    # xfile.save(filename)

main()
