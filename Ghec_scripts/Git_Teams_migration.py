import os
from github import Github


def team_exist(target_org, source_team, target_team_list):
    print("Checking team existence in target org for=",  source_team.name)
    if source_team.name in target_team_list:
        print("Team Found in targte ORG")
        return True
    else:
        print("Team is not present in targte ORG")
        return False



def copy_team(source_org, target_org, username, password, source_team_name=None):
   
    source_github = Github(base_url="https://github.xpo.com/api/v3".format(source_org), login_or_token=username, password=password)

    source_org = source_github.get_organization(source_org)
    print("source_team_name", source_team_name)
    if not source_team_name:
        teams=source_org.get_teams()
    else:
        teams = [source_org.get_team_by_slug(source_team_name)]

    target_github = Github(base_url="https://api.github.com", login_or_token='venkata.paladugu_xpo', password=os.environ["GITHUB_COM_TOKEN"])

    old_target= target_org
    target_org = target_github.get_organization(target_org)
    target_all_teams = target_org.get_teams()
    target_all_teams_name = [myteam.name for myteam in target_all_teams]

    list_migrated_teams = []
    list_not_migrated_teams = []

    for team in teams:
        # CHeck if team already exist, no need to process for that team.
        if team_exist(target_org, team, target_all_teams_name):
            continue
        source_team = source_org.get_team(team.id)
        print("source_team.name=",source_team, type(source_team.name))


        members = 0
        target_team = None
        maintainers_list = []
        maintainers = source_team.get_members("maintainer")
        # print(maintainers)

        for member in maintainers:
            print("maintainer=",member.login)
            if member.login == "pjchristopher":
                maintainers_list.append("Paul Christopher")
            else:
                maintainers_list.append(member.name)
        print("maintainers_list", maintainers_list)
        for member in source_team.get_members():
            # print("member=", member, type(member), member.role)

            if member.login == "pjchristopher":
                new_member = "Paul-Christopher" + "_xpo"
            else:
                new_member = member.login + "_xpo"
            # print("new member==", new_member)


            try:
                u = target_github.get_user(new_member)
            except Exception as e:
                print("User not found=", new_member)
            else:
                if member.login == "pjchristopher":
                    print(u.name, u.login)
                if not members:
                    try:
                       target_team =  target_org.create_team(team.name)
                       members += 1
                    except Exception as e:
                        exception_message = str(e) 
                        expected_text = "Name must be unique for this org"
                        if expected_text in exception_message:
                            print("error=", e)
                            continue

                if u.name in maintainers_list:
                    print("Adding maintainer", u.name)
                    target_team.add_membership(u, "maintainer")
                else:
                    target_team.add_membership(u)

        maintainers_list=[]
        v = target_github.get_user("venkata-paladugu_xpo")
        if target_team:
            target_team.remove_membership(v)
            print("\nTeam '{}' copied successfully to '{}' organization.".format(team.name, target_org.login))
            list_migrated_teams.append(team.name)
        else:
            print("\nTeam '{}'not copied to '{}' organization. There are no active members\n\n".format(team.name, target_org.login))
            list_not_migrated_teams.append(team.name)
        members = 0
                # for repo in source_team.get_repos():
        #     target_repo = target_org.get_repo(repo.full_name)
        #     target_team.set_repo_permission(target_repo, repo.get_teams()[0].permission)

    print("\n List of teams not migrated: ", list_not_migrated_teams)



def main():

    copy_team(
        source_org="xpo-infosec",
        target_org="xpo-org",
        username="venkata-paladugu",
        password=os.environ["GHES_TOKEN"],
        # source_team_name="BIDA"
)

main()