from sys import exit as sys_exit
import datetime
import xlsxwriter
from gitlab_evaluate.lib import utils
from gitlab_evaluate.migration_readiness.bitbucket.evaluate import BitbucketEvaluateClient

class BitbucketReportGenerator:

    def __init__(self, host, token, filename=None, output_to_screen=False, processes=None):
        self.host = host
        self.bitbucket_client = BitbucketEvaluateClient(host, token)
        self.validate_token()
        if filename:
            self.workbook = xlsxwriter.Workbook(f'{filename}.xlsx')
        else:
            self.workbook = xlsxwriter.Workbook('bitbucket_evaluate_report')
        self.app_stats = self.workbook.add_worksheet('App Stats')
        self.align_left = self.workbook.add_format({'align': 'left'})
        self.header_format = self.workbook.add_format({'bg_color': 'black', 'font_color': 'white', 'bold': True, 'font_size': 10})
        self.users = self.workbook.add_worksheet('Users')
        self.raw_output = self.workbook.add_worksheet('Raw Project Data')
        self.output_to_screen = output_to_screen
        self.using_admin_token = self.is_admin_token()
        self.processes = processes
        self.csv_columns = [
            'Project',
            'ID',
            'URL',
            'last_activity_at',
            'Branches',
            'Commit Count',
            'Pull Requests',
            'Repository Size in MB',
            'Tags',
            'Repository Archived'
        ]
        self.user_headers = ['Username', 'Email', 'State']
        utils.write_headers(0, self.raw_output, self.csv_columns, self.header_format)
        utils.write_headers(0, self.users, self.user_headers, self.header_format)

    def write_workbook(self):
        self.app_stats.autofit()
        self.raw_output.autofit()
        self.users.autofit()
        self.workbook.close()

    def get_app_stats(self):
        '''
            Gets Bitbucket instance stats
        '''
        response = self.bitbucket_client.get_application_properties()
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch application properties: {response.status_code} - {response.text}")

        app_properties = response.json()
        
        report_stats = [
            ('Basic information from source', self.host),
            ('Customer', '<CUSTOMERNAME>'),
            ('Date Run', utils.get_date_run()),
            ('Source', 'Bitbucket'),
            ('Bitbucket Version', app_properties.get('version')),
            ('Total Projects', len(self.get_total_projects())),
            ('Total Repositories', self.get_total_repositories()),
            ('Total Archived Repositories', self.get_total_archived_repositories())
        ]
        
        for row, stat in enumerate(report_stats):
            self.app_stats.write(row, 0, stat[0])
            self.app_stats.write(row, 1, stat[1])
        
        return report_stats
    
    def get_total_projects(self):
        all_projects = []
        params = {'limit': 100}
        print("Fetching all projects...")
        while True:
            response = self.bitbucket_client.get_projects(params=params)
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch projects: {response.status_code} - {response.text}")
            
            projects = response.json()
            all_projects.extend(projects['values'])
            
            print(f"Retrieved {len(all_projects)} projects so far...")

            # Check if there's a next page
            if 'nextPageStart' in projects:
                params['start'] = projects['nextPageStart']
            else:
                break  # No more pages
        return all_projects

    def get_total_repositories(self):
        total_repos = 0
        projects = self.get_total_projects()
        print("Fetching total repositories for all projects...")
        
        for project in projects:
            project_key = project['key']
            params = {'limit': 100}
            while True:
                response = self.bitbucket_client.get_repos(project_key, params=params)
                
                if response.status_code != 200:
                    raise Exception(f"Failed to fetch repositories for project {project_key}: {response.status_code} - {response.text}")
                
                repos = response.json()
                total_repos += len(repos['values'])

                print(f"Project {project_key}: Retrieved {total_repos} repositories so far...")

                # Check if there's a next page
                if 'nextPageStart' in repos:
                    params['start'] = repos['nextPageStart']
                else:
                    break  # No more pages
        return total_repos
    
    def get_total_archived_repositories(self):
        archived_count = 0
        projects = self.get_total_projects()
        print("Fetching total archived repositories for all projects...")
        
        for project in projects:
            project_key = project['key']
            params = {'limit': 100}

            while True:
                response = self.bitbucket_client.get_repos(project_key, params=params)
                
                if response.status_code != 200:
                    raise Exception(f"Failed to fetch repositories for project {project_key}: {response.status_code} - {response.text}")
                
                repos = response.json()
                for repo in repos.get('values', []):
                    if repo.get('archived', False):
                        archived_count += 1
    
                print(f"Project {project_key}: Retrieved {archived_count} archived repositories so far...")

                # Check if there's a next page
                if 'nextPageStart' in repos:
                    params['start'] = repos['nextPageStart']
                else:
                    break  # No more pages
        return archived_count

    def handle_getting_data(self):
        params = {'limit': 100}
        print("Fetching project data...")
        while True:
            response = self.bitbucket_client.get_projects(params=params)
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch projects: {response.status_code} - {response.text}")
            
            projects = response.json()
            
            for project in projects['values']:
                project_key = project['key']
                print(f"Fetching data for project {project_key}...")
                self.handle_getting_repo_data(project_key)

            # Check if there's a next page
            if 'nextPageStart' in projects:
                params['start'] = projects['nextPageStart']
            else:
                break  # No more pages


    def handle_getting_repo_data(self, project_key):
        params = {'limit': 100}
        total_repos = 0
        print(f"Fetching repositories for project {project_key}...")

        while True:
            response = self.bitbucket_client.get_repos(project_key, params=params)
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch repositories for project {project_key}: {response.status_code} - {response.text}")
            
            repos = response.json()
            total_repos += len(repos['values'])
            
            for repo in repos['values']:
                print(f"Processing repository {repo['slug']} in project {project_key}...")
                self.write_output_to_files(repo)

            # Print progress
            print(f"Project {project_key}: Retrieved and processed {total_repos} repositories so far...")

            # Check if there's a next page
            if 'nextPageStart' in repos:
                params['start'] = repos['nextPageStart']
            else:
                break  # No more pages

    def handle_getting_user_data(self):
        params = {'limit': 100}
        print("Fetching user data...")
        while True:
            response = self.bitbucket_client.get_admin_users(params=params)
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch users: {response.status_code} - {response.text}")
            
            users = response.json()
            
            for user in users['values']:
                user_data = {
                    'Username': user['name'],
                    'Email': user.get('emailAddress', 'N/A'),
                    'State': user['active']
                }
                utils.append_to_workbook(self.users, [user_data], self.user_headers)

            print(f"Retrieved {len(users['values'])} users so far...")

            # Check if there's a next page
            if 'nextPageStart' in users:
                params['start'] = users['nextPageStart']
            else:
                break  # No more pages

    def write_output_to_files(self, repo):
        project_key = repo['project']['key']
        repo_slug = repo['slug']

        # Get branches count
        branches_response = self.bitbucket_client.get_branches(project_key, repo_slug)
        if branches_response.status_code != 200:
            raise Exception(f"Failed to fetch branches for repo {repo_slug}: {branches_response.status_code} - {branches_response.text}")
        branches = branches_response.json()['values']
        
        # Get pull requests count with pagination
        pull_requests = []
        params = {'limit': 100}
        print(f"Fetching pull requests for repo {repo_slug}...")
        while True:
            prs_response = self.bitbucket_client.get_prs(project_key, repo_slug, params=params)
            if prs_response.status_code != 200:
                raise Exception(f"Failed to fetch pull requests for repo {repo_slug}: {prs_response.status_code} - {prs_response.text}")

            pull_requests.extend(prs_response.json()['values'])

            
            print(f"Retrieved {len(pull_requests)} pull requests so far...")

            # Check if there's a next page
            if 'nextPageStart' in prs_response.json():
                params['start'] = prs_response.json()['nextPageStart']
            else:
                break

        # Get last commit information to determine last activity
        commits_response = self.bitbucket_client.get_commits(project_key, repo_slug)
        if commits_response.status_code != 200:
            raise Exception(f"Failed to fetch commits for repo {repo_slug}: {commits_response.status_code} - {commits_response.text}")
        commits = commits_response.json()['values']
        last_activity = commits[0]['committerTimestamp'] if commits else 'N/A'
        if last_activity != 'N/A':
            last_activity = datetime.datetime.fromtimestamp(last_activity/1000).strftime('%c')
        commit_count = len(commits)

        # Get repository size
        repository_size = self.bitbucket_client.get_repo_size(repo)
        
        # Get tags count
        tags_response = self.bitbucket_client.get_tags(project_key, repo_slug)
        if tags_response.status_code != 200:
            raise Exception(f"Failed to fetch tags for repo {repo_slug}: {tags_response.status_code} - {tags_response.text}")
        tags = tags_response.json()['values']

        repo_data = {
            'Project': repo['project']['name'],
            'ID': repo['id'],
            'URL': repo['links']['self'][0]['href'],
            'last_activity_at': last_activity,
            'Branches': len(branches),
            'Commit Count': commit_count,
            'Pull Requests': len(pull_requests),
            'Repository Size in MB': repository_size,
            'Tags': len(tags),
            'Repository Archived' : self.bitbucket_client.is_repo_archived(project_key, repo_slug)
        }
        utils.append_to_workbook(self.raw_output, [repo_data], self.csv_columns)
        if self.output_to_screen:
            print(f"Repository Data: {repo_data}")
    
    def validate_token(self):
        response = self.bitbucket_client.get_users()
        if response.status_code != 200:
            print("Invalid token. Exiting...")
            sys_exit(1)

    def is_admin_token(self):
        response = self.bitbucket_client.get_admin_users()
        return response.status_code == 200
