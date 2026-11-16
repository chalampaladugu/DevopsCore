import requests
import threading
import openpyxl

TEAMCITY_BASE_URL = 'http://dev-teamcity-gke.ltl.xpo.com:8080'
API_TOKEN = 'eyJ0eXAiOiAiVENWMiJ9.eFAzOGdtWl80Vk5PM2JwTUE4amVaMkYzUjlJ.ZDZlODFiNGUtZTU3Yy00NGY3LWJlODQtNmQ5N2UzNzQ3MmRl' # TODO: Enter the API key from TeamCity
HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}
all_parameters = {}

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
    vcs_endpoint = f"{TEAMCITY_BASE_URL}/app/rest/buildTypes/id:{build_config_id}/vcs-root-entries"

    # Make a GET request to fetch VCS roots
    vcs_response = requests.get(vcs_endpoint, headers=HEADERS)
    vcs_response.raise_for_status()

    # Parse VCS roots response JSON
    vcs_roots = vcs_response.json()
    # print(vcs_roots)
    vcs_root_ids = vcs_roots['vcs-root-entry']
    vcs_root_id=''
    for root in vcs_root_ids:
        id = root['vcs-root']['id']
        if id[-5:] == '-GHES':
            continue
        vcs_root_id = id
        break

    if not vcs_root_id:
        # print(f'No vcs root found for build : {build_name}')
        return None

    response = requests.get(
        url=f"{TEAMCITY_BASE_URL}/app/rest/vcs-roots/id:{vcs_root_id}",
        headers=HEADERS,
    )
    response.raise_for_status()
    vcs_roots = response.json()
    url = ''
    # print(vcs_roots)
    try:
        for property in vcs_roots['properties']['property']:
            if property['name'] == 'url':
                url = property['value'].split('/')[-1].replace('.git', '')
                global build_config_from_vcs_root
                lock.acquire()
                if build_config_from_vcs_root.get(url):
                    build_config_from_vcs_root[url].append(build_name)
                else:
                    build_config_from_vcs_root[url] = [build_name]
                lock.release()
    except Exception as e:
        print(f'Error in parsing url for {build_config_id}')
    return url
 

def get_build_configuration_parameters():
    global all_parameters
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
            # Get parameters for the current build configuration
            t = threading.Thread(target=get_build_configuration_parameters_by_id, args=(param_lock, build_config_id, build_config['name']))
            param_thread_list.append(t)
        
        # starting threads
        print('Start VCS Thread ', datetime.datetime.now())
        for th in vcs_thread_list:
            th.start()
        for th in vcs_thread_list:
            th.join()
        print('Start param Thread ', datetime.datetime.now())
        for th in param_thread_list:
            th.start()
        for th in param_thread_list:
            th.join()

        print("Reading Done")
        print('Done VCS Thread ', datetime.datetime.now())
        return all_parameters
    else:
        print(f"Failed to fetch build configurations. Status code: {response.status_code}")
        return None

def get_build_configuration_parameters_by_id(lock, build_configuration_id, build_name):
    global all_parameters
    # Construct the URL to fetch parameters of a specific build configuration
    # build_configuration_id = 'XpoLtl_Java_Development_LtlJavaCustomerRestDevelopment'
    url = f"{TEAMCITY_BASE_URL}/app/rest/buildTypes/{build_configuration_id}/parameters"

    # Make a GET request to fetch parameters
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        # Parse the JSON response and extract parameters
        parameters = response.json()["property"]    
        if parameters:
           lock.acquire()
           all_parameters[build_name] = parameters 
           lock.release()
        return parameters
    else:
        print(f"Failed to fetch parameters for build configuration {build_configuration_id}. Status code: {response.status_code}")
        return None
    
# Check if a build configuration is attached to a template
def is_attached_to_template(build_config_id):
    url = f'{TEAMCITY_BASE_URL}/app/rest/buildTypes/id:{build_config_id}'
    response = requests.get(url, headers=HEADERS)
    build_config_details = response.json()
    return 'template' in build_config_details


def get_repo_from_sheet():
    xfile = openpyxl.load_workbook('github_repos_tc.xlsx')
    repo_sheet = xfile.get_sheet_by_name('GitHub Repositories')
    # Get the column index for the column named 'Column_Name'
    repo_name_index = get_column_index(repo_sheet, 'Repository Name')
    migration_eligible_index = get_column_index(repo_sheet, 'MigrationEligible')
    migration_status_index = get_column_index(repo_sheet, 'MigrationStatus')
    TeamcityBuildConfigs_index = get_column_index(repo_sheet, 'TeamcityBuildConfigs')

    # generate repo list
    repo_from_sheet = []
    for row in repo_sheet:
        # print(row[repo_name_index].value)
        # print(row[migration_eligible_index].value)
        # print(row[migration_status_index].value)
        if row[repo_name_index].value:
            # and row[migration_eligible_index].value and row[migration_status_index].value
            if row[migration_eligible_index].value != None and row[migration_eligible_index].value.lower() == "needs to check":
                repo_from_sheet.append(row[repo_name_index].value)
            
    # print(repo_from_sheet)
    xfile.close()
    return repo_from_sheet

def save_build_config_to_sheet(repo_build_config_dict):
    xfile = openpyxl.load_workbook('github_repos_tc.xlsx')
    repo_sheet = xfile.get_sheet_by_name('GitHub Repositories')
    repo_name_index = get_column_index(repo_sheet, 'Repository Name')
    TeamcityBuildConfigs_index = get_column_index(repo_sheet, 'TeamcityBuildConfigs')
    

    # generate repo list
    repo_list = repo_build_config_dict.keys()
    # print('print(repo_list)=', repo_list)

    for row in repo_sheet:
        # print('ROW 4 VALUE=', row[TeamcityBuildConfigs_index].value)
        #row[TeamcityBuildConfigs_index].value == ROW4_VALUE
        # if row[TeamcityBuildConfigs_index].value == None :
        if row[repo_name_index].value in repo_list:
            row[TeamcityBuildConfigs_index].value = "\n".join(repo_build_config_dict.get(row[repo_name_index].value))
            print(row[TeamcityBuildConfigs_index].value)
        else:
            row[TeamcityBuildConfigs_index].value = "NA"

    xfile.save('github_repos_tc.xlsx')        
    xfile.close()


def main():
    repos = get_repo_from_sheet()
    # repos = ['ltl-java-venkatpoc-rest']
    all_parameters = get_build_configuration_parameters()

    if all_parameters:
        print("Build Configuration Parameters:")
        for build_config, params in all_parameters.items():
            # print(f"\n{build_config}:")
            component = ''
            project_type = ''
            project_name = ''
            full_project_name = ''
            component_name = ''
            for param in params:
                if param.get('name') == 'component':
                    component = param.get('value')
                if param.get('name') == 'project_type':
                    project_type = param.get('value')
                if param.get('name') == 'project_name':
                    project_name = param.get('value')
                if param.get('name') == 'component_name':
                    component_name = param.get('value') 
                if param.get('name') == 'full_project_name':
                    full_project_name = param.get('value')  
                    #print(f'full_project_name={full_project_name}')          
            if full_project_name and component_name:
                full_project_name = full_project_name.replace('%component_name%', component_name)
                # print(f'full_project_name after replace={full_project_name}')
                project_name = full_project_name
            if project_type:
                project_name = project_name.replace('%project_type%', project_type)    
            if component:
                project_name = project_name.replace('%component%', component) 
            # print(project_name)
            if project_name in repos:
                if repo_build_config.get(project_name):
                    repo_build_config[project_name].append(build_config)
                else:
                    repo_build_config[project_name] = [build_config]
                    repo_with_templates.append(project_name)

            # if project_type and component and project_name:
            #     project_name = project_name.replace('%component%', component).replace('%project_type%', project_type)    
            #     # print(project_name)
            #     if project_name in repos:
            #         if repo_build_config.get(project_name):
            #             repo_build_config[project_name].append(build_config)
            #         else:
            #             repo_build_config[project_name] = [build_config]
            #             repo_with_templates.append(project_name)


    repo_without_templates = []
    for repo in repos:
        if repo not in repo_with_templates:
            repo_without_templates.append(repo)

    for repo in repo_without_templates:
        if repo in build_config_from_vcs_root.keys():
            # print(f'Build Config for {repo} = {build_config_from_vcs_root[repo]}')
            repo_build_config[repo] = build_config_from_vcs_root[repo]

    # print(f'Saving Fetched Data:\n{repo_build_config}')
    save_build_config_to_sheet(repo_build_config)

main()
