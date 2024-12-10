from urllib.parse import urljoin
import requests
import base64
import sys
import time


class AdoEvaluateClient():
    def __init__(self, host, token):
        self.host = host
        encoded_pat = base64.b64encode(f":{token}".encode()).decode()
        self.headers = {
            'Authorization': f'Basic {encoded_pat}'
        }
        self.params = {
            'api-version': '7.0-preview'
        }

    def generate_request_url(self, host, api, sub_api=None):
        base_url = host
        if not base_url.startswith("https://"):
            base_url = f"https://{base_url}"
        if sub_api:
            base_url_parts = base_url.split("://")
            base_url = f"{base_url_parts[0]}://{sub_api}.{base_url_parts[1]}"
        return urljoin(base_url + '/', api)

    def get_descriptor(self, project_id, params=None):
        url = self.generate_request_url(self.host, api=f"_apis/graph/descriptors/{project_id}", sub_api="vssps")
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()["value"]
        except Exception as e:
            print(f"Error fetching descriptors {url}: {e}", file=sys.stderr)

    def get_project_administrators_group(self, project_id, params=None):
        scopeDescriptor = self.get_descriptor(project_id)
        url = self.generate_request_url(self.host, api=f"_apis/graph/groups?scopeDescriptor={scopeDescriptor}", sub_api="vssps")
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            project_admins = next((item for item in response.json()["value"] if item["displayName"] == "Project Administrators"), None)
            if project_admins:
                return project_admins["originId"]
            else:
                return None
        except Exception as e:
            print(f"Error fetching descriptors {url}: {e}", file=sys.stderr)

    def get_project_administrators(self, project_id, params=None):
        project_group_id = self.get_project_administrators_group(project_id)
        url = self.generate_request_url(self.host, api=f"_apis/GroupEntitlements/{project_group_id}/members", sub_api="vsaex")
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            admins = []
            for member in response.json()["members"]:
                admins.append(f"{member['user']['displayName']} <{member['user']['mailAddress']}>")
            return admins
        except Exception as e:
            print(f"Error fetching descriptors {url}: {e}", file=sys.stderr)

    def get_work_items(self, project_id, project_name, params=None):
        params.update(self.params)
        url = self.generate_request_url(self.host, api=f"{project_id}/_apis/wit/wiql")
        query = {
            "query": f"Select [System.Id], [System.Title], [System.State] From WorkItems WHERE [System.TeamProject] = '{project_name}'"
        }
        return requests.post(url, headers=self.headers, params=params, json=query)

    def get_release_definitions(self, project_id, params=None):
        params.update(self.params)
        url = self.generate_request_url(self.host, api=f"{project_id}/_apis/release/definitions", sub_api="vsrm")
        return requests.get(url, headers=self.headers, params=params)

    def get_build_definitions(self, project_id, params=None):
        params.update(self.params)
        url = self.generate_request_url(self.host, api=f"{project_id}/_apis/build/definitions")
        return requests.get(url, headers=self.headers, params=params)

    def get_commits(self, project_id, repository_id, params=None):
        params.update(self.params)
        url = self.generate_request_url(self.host, api=f"{project_id}/_apis/git/repositories/{repository_id}/commits")
        return requests.get(url, headers=self.headers, params=params)

    def get_prs(self, project_id, repository_id, params=None):
        params.update(self.params)
        url = self.generate_request_url(self.host, api=f"{project_id}/_apis/git/repositories/{repository_id}/pullrequests")
        return requests.get(url, headers=self.headers, params=params)

    def get_branches(self, project_id, repository_id, params=None):
        params.update(self.params)
        url = self.generate_request_url(self.host, api=f"{project_id}/_apis/git/repositories/{repository_id}/refs")
        return requests.get(url, headers=self.headers, params=params)

    def get_repos(self, project_id, params=None):
        params.update(self.params)
        url = self.generate_request_url(self.host, api=f"{project_id}/_apis/git/repositories")
        return requests.get(url, headers=self.headers, params=params)

    def get_project(self, project_id, params=None):
        params.update(self.params)
        url = self.generate_request_url(self.host, api=f"_apis/project/{project_id}")
        return requests.get(url, headers=self.headers, params=params)

    def get_projects(self, params=None):
        params.update(self.params)
        url = self.generate_request_url(self.host, api='_apis/projects')
        return requests.get(url, headers=self.headers, params=params)

    def get_users(self, params=None):
        params.update(self.params)
        url = self.generate_request_url(self.host, api='_apis/graph/users', sub_api="vssps")
        return requests.get(url, headers=self.headers, params=params)

    def retry_request(self, request_func, params, *args, max_retries=3, retry_delay=5):
        for retry_count in range(max_retries):
            response = request_func(*args, params=params)
            if response.status_code == 200:
                return response
            print(f"Received error {response.status_code}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        print(f"Max retries reached ({retry_count}). Unable to complete the request.")
        raise Exception(f"Failed to complete the request after {max_retries} retries: {response.status_code}")

    def test_connection(self, params=None):
        params.update(self.params)
        url = self.generate_request_url(self.host, api='_apis/ConnectionData')
        return requests.get(url, headers=self.headers, params=params)
