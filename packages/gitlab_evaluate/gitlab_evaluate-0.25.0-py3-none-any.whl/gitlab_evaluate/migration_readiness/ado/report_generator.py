from sys import exit as sys_exit
import xlsxwriter
from gitlab_evaluate.lib import utils
from gitlab_evaluate.migration_readiness.ado.evaluate import AdoEvaluateClient


class AdoReportGenerator:

    def __init__(self, host, token, filename=None, output_to_screen=False, processes=None):

        self.total_repositories = 0
        self.total_disabled_repositories = 0
        self.total_uninitialized_repositories = 0
        self.total_projects = 0
        self.total_users = 0
        self.host = host
        self.ado_client = AdoEvaluateClient(host, token)
        self.validate_token()
        if filename:
            self.workbook = xlsxwriter.Workbook(f'{filename}.xlsx')
        else:
            self.workbook = xlsxwriter.Workbook('ado_evaluate_report')
        self.app_stats = self.workbook.add_worksheet('Organization Insights')
        self.align_left = self.workbook.add_format({'align': 'left'})
        self.header_format = self.workbook.add_format({'bg_color': 'black', 'font_color': 'white', 'bold': True, 'font_size': 10})
        self.users = self.workbook.add_worksheet('Users')
        self.projects = self.workbook.add_worksheet('Raw Project Data')
        self.raw_output = self.workbook.add_worksheet('Raw Repository Data')
        self.output_to_screen = output_to_screen
        self.processes = processes
        self.csv_columns = [
            'Project Name',
            'Project ID',
            'Repository Name',
            'Repository ID',
            'Default Branch',
            'Git URL',
            'Last activity',
            'Branches',
            'Commits',
            'Pull Requests',
            'Repository Size in MB',
            'Repository Disabled'
        ]
        self.user_headers = ['Object ID', 'Descriptor', 'Display Name', 'Principal Name', 'Email']
        self.project_headers = ['Project ID', 'URL', 'Name', "Total Repositories", "Total Build Definitions", "Total Release Definitions", "Total Work Items", 'Administrators']
        utils.write_headers(0, self.raw_output, self.csv_columns, self.header_format)
        utils.write_headers(0, self.users, self.user_headers, self.header_format)
        utils.write_headers(0, self.projects, self.project_headers, self.header_format)

    def write_workbook(self):
        self.app_stats.autofit()
        self.raw_output.autofit()
        self.users.autofit()
        self.projects.autofit()
        self.workbook.close()

    def get_app_stats(self):
        '''
            Gets Azure DevOps instance stats
        '''
        report_stats = [
            ('Organization URL', self.host),
            ('Customer', '<CUSTOMERNAME>'),
            ('Date Run', utils.get_date_run()),
            ('Source', 'Azure DevOps'),
            ('Total Projects', self.total_projects),
            ('Total Repositories', self.total_repositories),
            ('Total Disabled Repositories', self.total_disabled_repositories),
            ('Total Uninitialized Repositories', self.total_uninitialized_repositories),
            ('Total Users', self.total_users),
        ]
        for row, stat in enumerate(report_stats):
            self.app_stats.write(row, 0, stat[0])
            self.app_stats.write(row, 1, stat[1])
        return report_stats

    def handle_getting_data(self):

        params = {
            "$top": "100"
        }

        print("Fetching projects data...")
        while True:
            response = self.ado_client.retry_request(self.ado_client.get_projects, params)
            projects = response.json()
            self.total_projects += len(projects.get('value'))
            print(f"Retrieved {self.total_projects} projects so far...")
            for project in projects['value']:
                project_id = project['id']
                print(f"Fetching data for project {project_id}...")
                self.handle_getting_project_data(project)
                self.handle_getting_repo_data(project_id)

            # Check if there's a next page
            if not any(key.lower() == "x-ms-continuationtoken" for key in response.headers):
                break  # No more pages
            # There is page, so get the continuation token for the next page
            params["continuationToken"] = response.headers["X-MS-ContinuationToken"]

    def handle_getting_repo_data(self, project_id):

        params = {
            "$top": "100"
        }

        print(f"Fetching repositories for project {project_id}...")

        while True:
            response = self.ado_client.retry_request(self.ado_client.get_repos, params, project_id)
            repos = response.json()
            self.total_repositories += len(repos.get('value'))
            for repo in repos['value']:
                print(f"Processing repository {repo['name']} in project {project_id}...")
                self.write_output_to_files(repo)
                if repo["isDisabled"]:
                    self.total_disabled_repositories += 1
                if repo["size"] == 0:
                    self.total_uninitialized_repositories += 1

            # Print progress
            print(f"Project {project_id}: Retrieved and processed {self.total_repositories} repositories so far...")

            # Check if there's a next page
            if not any(key.lower() == "x-ms-continuationtoken" for key in response.headers):
                break  # No more pages
            # There is page, so get the continuation token for the next page
            params["continuationToken"] = response.headers["X-MS-ContinuationToken"]

    def handle_getting_project_data(self, project):
        params = {}
        print("Fetching project data...")
        project_id = project["id"]
        project_name = project["name"]
        print(f"Retriving project administrators in {project_name}...")
        project_admins = self.ado_client.get_project_administrators(project_id)
        if project_admins and isinstance(project_admins, list):
            project_admins_str = ', '.join(project_admins)
        else:
            project_admins_str = str(project_admins) if project_admins is not None else "No administrators found"

        print(f"Retriving total repositories, yaml definitions, classic releases and work items in {project_name}...")

        get_repos_response = self.ado_client.get_repos(project_id, params=params)
        try:
            total_repos = len(get_repos_response.json().get("value", []))
        except get_repos_response.exceptions.JSONDecodeError:
            print(f"Failed to decode JSON for repositories. Raw response: {get_repos_response.text}")
            total_repos = 0  # or handle this case as appropriate for your application

        get_build_definitions_response = self.ado_client.get_build_definitions(project_id, params=params)
        try:
            total_build_definitions = len(get_build_definitions_response.json().get("value", []))
        except get_build_definitions_response.exceptions.JSONDecodeError:
            print(f"Failed to decode JSON for repositories. Raw response: {get_build_definitions_response.text}")
            total_build_definitions = 0  # or handle this case as appropriate for your application

        get_release_definitions_response = self.ado_client.get_release_definitions(project_id, params=params)
        try:
            total_release_definitions = len(get_release_definitions_response.json().get("value", []))
        except get_release_definitions_response.exceptions.JSONDecodeError:
            print(f"Failed to decode JSON for repositories. Raw response: {get_release_definitions_response.text}")
            total_release_definitions = 0  # or handle this case as appropriate for your application

        get_work_items_response = self.ado_client.get_work_items(project_id, project_name, params=params)
        try:
            total_work_items = len(get_work_items_response.json().get("workItems", []))
        except get_work_items_response.exceptions.JSONDecodeError:
            print(f"Failed to decode JSON for work items. Raw response: {get_work_items_response.text}")
            total_work_items = 0  # or handle this case as appropriate for your application

        project_data = {
            'Project ID': project['id'],
            'URL': project['url'],
            'Name': project['name'],
            'Total Repositories': total_repos,
            'Total Build Definitions': total_build_definitions,
            'Total Release Definitions': total_release_definitions,
            'Total Work Items': total_work_items,
            'Administrators': project_admins_str
        }
        utils.append_to_workbook(self.projects, [project_data], self.project_headers)

    def handle_getting_user_data(self):
        params = {
            "subjectTypes": "aad,msa"
        }
        print("Fetching user data...")
        while True:
            response = self.ado_client.retry_request(self.ado_client.get_users, params)
            users = response.json()
            for user in users["value"]:
                user_data = {
                    'Object ID': user['originId'],
                    'Descriptor': user['descriptor'],
                    'Display Name': user['displayName'],
                    'Principal Name': user['principalName'],
                    'Email': user.get('mailAddress', 'N/A')
                }
                utils.append_to_workbook(self.users, [user_data], self.user_headers)
            self.total_users += len(users['value'] if 'value' in users else [])
            
            print(f"Retrieved {self.total_users} users so far...")

            # Check if there's a next page
            if not any(key.lower() == "x-ms-continuationtoken" for key in response.headers):
                print(f"Retrieved a total of {self.total_users} users.")
                break  # No more pages
            # There is page, so get the continuation token for the next page
            params["continuationToken"] = response.headers["X-MS-ContinuationToken"]
            # print(response.request.url)

    def write_output_to_files(self, repo):
        project_id = repo['project']['id']
        repository_id = repo['id']
        last_activity = "N/A"
        default_branch = repo['defaultBranch'] if 'defaultBranch' in repo else 'N/A'

        if repo["isDisabled"] is False:

            branches = []
            params = {'$top': 100}
            print(f"Fetching branches for repo {repository_id}...")
            while True:
                branches_response = self.ado_client.retry_request(self.ado_client.get_branches, params, project_id, repository_id)
                branches.extend(branches_response.json()['value'])
                print(f"Retrieved {len(branches)} branches so far...")

                # Check if there's a next page
                if not any(key.lower() == "x-ms-continuationtoken" for key in branches_response.headers):
                    break  # No more pages
                # There is page, so get the continuation token for the next page
                params["continuationToken"] = branches_response.headers["X-MS-ContinuationToken"]

            pull_requests = []
            params = {'limit': 100}
            print(f"Fetching pull requests for repo {repository_id}...")
            while True:
                prs_response = self.ado_client.retry_request(self.ado_client.get_prs, params, project_id, repository_id)
                pull_requests.extend(prs_response.json()['value'])
                print(f"Retrieved {len(pull_requests)} pull requests so far...")

                # Check if there's a next page
                if not any(key.lower() == "x-ms-continuationtoken" for key in prs_response.headers):
                    break  # No more pages
                # There is page, so get the continuation token for the next page
                params["continuationToken"] = prs_response.headers["X-MS-ContinuationToken"]

            commits = []
            params = {'$top': 10000}
            print(f"Fetching commits for repo {repository_id}...")
            commits_response = self.ado_client.retry_request(self.ado_client.get_commits, params, project_id, repository_id)
            commits.extend(commits_response.json()['value'])
            print(f"Retrieved {len(commits)} commits so far...")
            last_activity = commits[0]['committer']['date'] if commits else 'N/A'
            commit_count = len(commits)

        repo_data = {
            'Project Name': repo['project']['name'],
            'Project ID': repo['project']['id'],
            'Repository Name': repo['name'],
            'Repository ID': repo['id'],
            'Default Branch': default_branch,
            'Git URL': repo['webUrl'],
            'Last activity': last_activity,
            'Branches': len(branches) if repo["isDisabled"] is False else "N/A",
            'Commits': commit_count if repo["isDisabled"] is False else "N/A",
            'Pull Requests': len(pull_requests) if repo["isDisabled"] is False else "N/A",
            'Repository Size in MB': round(repo.get('size') / 1024 / 1024, 2) if repo["isDisabled"] is False else "N/A",
            'Repository Disabled': repo.get('isDisabled')
        }
        utils.append_to_workbook(self.raw_output, [repo_data], self.csv_columns)
        if self.output_to_screen:
            print(f"Repository Data: {repo_data}")

    def validate_token(self):
        params = {}
        response = self.ado_client.test_connection(params=params)
        if response.status_code != 200:
            print("Invalid URL or PAT. Exiting...")
            sys_exit(1)
