import os
import github

target_github = github.Github(base_url="https://api.github.com", login_or_token='venkata.paladugu_xpo', password=os.environ["GITHUB_COM_TOKEN"])
target_org = target_github.get_organization('xpo-org')

repos_list = [
    'ltl-component-technology-subtech-master',
]


team_name_list = {
    'ltl-ea-devops': 'admin',
    'ltl-ea-service-governance': 'admin',
    'ltl-service-governance': 'admin'
}

def create_repo_from_template(repo_template):
    # Authenticate using your GitHub token
    # token = os.getenv('GITHUB_TOKEN')
    # g = Github(token)
    for repo_tocreate, template_repo in repo_template.items():
        # Specify the owner and repository name of the template
        template_owner = 'xpo-org'
        template_repo_name = template_repo

        # Specify the details of the new repository
        new_repo_name = repo_tocreate
        new_repo_description = 'Description for the new repository'

        # Get the template repository
        template_repo = target_github.get_repo(f'{template_owner}/{template_repo_name}')
        print(f'template_repo={template_repo}')

        # Create a new repository from the template
        # user = target_github.get_user()
        # print(f'user={user}')
        # target_org.create_repo_from_template
        try:
            new_repo = target_org.create_repo_from_template(
                new_repo_name,
                template_repo,
                # owner=user.login,
                description=new_repo_description,
                private=True,
                include_all_branches=True,
                # team_id=None,
                # gitignore_template=None,
                # license_template=None
            )
        except Exception as err:
            print(f'Error in repo creation {new_repo_name} ...{err}')    
        else:
            print(f'Repository {new_repo_name} created successfully')
            for team_name, permission in team_name_list.items():
                team = target_org.get_team_by_slug(team_name)
                print(f'Updating team [{team_name}] with [{permission}] for repo [{new_repo_name}]')
                team.update_team_repository(new_repo, permission)

            try:
                v = target_github.get_user("venkata-paladugu_xpo")
                new_repo.remove_from_collaborators(v)
            except Exception as err:
                print(f'Error in removing user: {err}')
                

def crete_repo_in_ghec(repos_list):
    for repo_name in repos_list:
        repo = None
        try:
            repo = target_org.get_repo(repo_name)
        except Exception as err:
            if err.args[0] == 404:
                print('Creating repo=', repo_name)
                repo = target_org.create_repo(repo_name, private=True)
            else:
                print(err)
                continue
        finally:
            for team_name, permission in team_name_list.items():
                team = target_org.get_team_by_slug(team_name)
                print(f'Updating team [{team_name}] with [{permission}] for repo [{repo_name}]')
                team.update_team_repository(repo, permission)
            print('Done')

def generate_repo_name(component, tech, subtech):
    """
    ltl-java-component-rest
    ltl-api-component-contract 
    ltl-api-component-property
    ltl-api-component-dist
    ltl-java-component-master
    """
    repo_template = {}
    if tech == 'java':
        if subtech == 'jaxrs':
            repo_template[f'ltl-java-{component}-rest'] = f'ltl-java-component-rest'
            # repo_template[f'ltl-java-{component}-master'] = f'ltl-java-component-master'
            # repo_template[f'ltl-api-{component}-contract'] = f'ltl-java-component-contract'
            # repo_template[f'ltl-api-{component}-dist'] = f'ltl-java-component-dist'
            # repo_template[f'ltl-api-{component}-property'] = f'ltl-java-component-property'
        elif subtech == 'springboot':
            repo_template[f'ltl-java-{component}-rest'] = f'ltl-java-component-rest--springboot-pf'
            repo_template[f'ltl-api-{component}-contract'] = f'ltl-api-component-contract--springboot'
            repo_template[f'ltl-api-{component}-dist'] = f'ltl-java-component-dist'
            repo_template[f'ltl-api-{component}-property'] = f'ltl-java-component-property'
    
    return repo_template

def main():
    print('Enter Component')
    component = input()
    print(component)
    print('Enter Tech')
    tech = input()
    print(tech)
    # TODO: Add validation for tech and subtech
    # if tech != 'java':
    print('Enter Subtech')
    subtech = input()
    print(subtech)

    repo_template = generate_repo_name(component, tech, subtech)
    print(f'Genrated repo names: {repo_template}')
    create_repo_from_template(repo_template)

main()