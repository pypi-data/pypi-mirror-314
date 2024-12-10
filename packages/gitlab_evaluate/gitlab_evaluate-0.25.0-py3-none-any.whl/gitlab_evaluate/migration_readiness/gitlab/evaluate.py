from re import findall
from traceback import print_exc
from copy import deepcopy as copy
from json import dumps as json_dumps
from dacite import from_dict
from gitlab_ps_utils.misc_utils import safe_json_response, is_error_message_present
from gitlab_ps_utils.dict_utils import dig
from gitlab_evaluate import log
from gitlab_evaluate.lib import utils
from gitlab_evaluate.migration_readiness.gitlab.flag_remediation import FlagRemediationMessages
from gitlab_evaluate.lib.api_models.user import User
from gitlab_evaluate.migration_readiness.gitlab import limits
from gitlab_evaluate.migration_readiness.gitlab.queries import *


class EvaluateApi():

    app_api_url = "/application/statistics"
    app_ver_url = "/version"

    supported_package_types = ['generic', 'npm', 'pypi', 'maven']

    def __init__(self, gitlab_api):
        self.gitlab_api = gitlab_api

    # Project only keyset-based pagination - https://docs.gitlab.com/ee/api/#keyset-based-pagination

    def get_last_id(self, link):
        # Get id_after value. If the Link key is missing it's done, with an empty list response
        return findall(r"id_after=(.+?)&", link)[0] if link else None

    '''
    Generates the URL to get the full project info with statistics
    '''

    def proj_info_get(self, i, source):
        '''Trying to create proper api call with project id.'''
        return f"{source}/api/v4/projects/{str(i)}?statistics=true"

    def proj_packages_url(self, i):
        return f"projects/{str(i)}/packages"

    def proj_registries_url(self, i):
        return f"projects/{str(i)}/registry/repositories"

    def proj_registries_tags_url(self, pid, rid):
        return f"projects/{str(pid)}/registry/repositories/{str(rid)}/tags"

    def proj_registries_tag_details_url(self, pid, rid, tid):
        return f"projects/{str(pid)}/registry/repositories/{str(rid)}/tags/{tid}"

    def get_registry_details(self, i):
        return f"registry/repositories/{str(i)}?size=true"

    # Functions - Return API Data
    # Gets the X-Total from the statistics page with the -I on a curl
    def check_x_total_value_update_dict(self, check_func, p, host, token, api=None, value_column_name="DEFAULT_VALUE", over_column_name="DEFAULT_COLUMN_NAME", results={}):
        flag = False
        if api is not None:
            count = self.get_total_count(
                host, token, api, p['fullPath'], value_column_name, p.get('id'))
        else:
            count = self.get_result_value(results, value_column_name)
        if count is not None:
            num_over = check_func(count)
            if num_over:
                flag = True
            results[value_column_name] = count
            results[over_column_name] = num_over
        else:
            log.debug(
                f"No {value_column_name} retrieved for project: {p.get('id')} - {p.get('fullPath')}")
        return flag

    def get_total_count(self, host, token, api, full_path, entity, project_id=None):
        count = self.gitlab_api.get_count(host, token, api)
        if count is not None:
            return count
        else:
            log.debug(
                f"Could not retrieve total '{api}' count via API, using GraphQL instead")
            formatted_entity = utils.to_camel_case(entity)
            query = {
                "query": """
                    query {
                        project(fullPath: "%s") {
                            name,
                            %s {
                                count
                            }
                        }
                    }
                """ % (full_path, formatted_entity)
            }

            if gql_resp := safe_json_response(self.gitlab_api.generate_post_request(host, token, None, json_dumps(query), graphql_query=True)):
                return dig(gql_resp, 'data', 'project', formatted_entity, 'count')

    # gets the full stats of the project and sorts based on the returned items, passing a few through the HumanReadable utility
    def check_full_stats(self, url, project, my_dict, headers={}):
        project_path = project.get('fullPath')
        log.info(f"Listing full stats for project '{project_path}'")
        if result := safe_json_response(self.gitlab_api.generate_get_request(host="", api="", token=headers.get("PRIVATE-TOKEN"), url=url)):
            my_dict.update(
                {"last_activity_at": result.get("lastActivityAt")})
            if kind := result.get("namespace"):
                my_dict.update({"kind": kind.get("kind")})
            if stats := result.get("statistics"):
                export_total = 0
                for k, v in stats.items():
                    updated_dict_entry = {
                        k: v, k + "_over": utils.check_size(k, v)}
                    my_dict.update(updated_dict_entry)

                    # If 'k' is an item that would be part of the export, add to running total
                    if k in [
                        "repositorySize",
                        "wikiSize",
                        "lfsObjectsSize",
                        "snippetsSize",
                        "uploadsSize"
                    ]:
                        export_total += int(v)

                # Get Mirrors
                my_dict['mirror'] = result.get('mirror', False)

                # Write running total to my_dict
                export_total_key = "Estimated Export Size"
                my_dict.update({f"{export_total_key}": export_total})
                # 5Gb
                my_dict.update({f"{export_total_key} Over": utils.check_size(
                    export_total_key, export_total)})
                # 10Gb
                my_dict.update({f"{export_total_key} S3 Over": utils.check_size(
                    f"{export_total_key} S3", export_total)})
            else:
                log.warning(
                    "Could not retrieve project '{project_path}' stats.\n")
        else:
            log.warning(
                f"Could not retrieve project '{project_path}' (ID: {project.get('id')})")

    def get_registry_size(self, path_with_namespace, source, token):
        """
            Iterates over a project's registry data and returns the total size of registry data
        """
        total_size = self.get_registry_size_by_graphql(
            path_with_namespace, source, token)
        if total_size is not None and total_size > 0:
            log.debug(
                f"Retrieved project '{path_with_namespace}' registry size ({total_size}) by single GraphQL query")
        return total_size, utils.check_storage_size(total_size)

    def get_registry_size_by_graphql(self, path_with_namespace, source, token):
        """
            Makes a single GraphQL query to get the total registry size
            of a project. This query could return an error stating
            the query result is too large
        """
        query = {
            'query': """
                query {
                    project(fullPath: "%s") {
                        statistics {
                            containerRegistrySize
                            }
                        }
                    }

            """ % path_with_namespace
        }
        if gql_resp := safe_json_response(self.gitlab_api.generate_post_request(source, token, None, data=json_dumps(query), graphql_query=True)):
            return dig(gql_resp, 'data', 'project', 'statistics', 'containerRegistrySize')
        return None
    
    def get_all_projects_by_graphql(self, source, token, full_path=None):
        after = ""
        levels = []
        try:
            while True:
                if full_path:
                    query = generate_group_project_query(full_path, after)
                    levels = ['data', 'group', 'projects', 'nodes']
                else:
                    query = generate_all_projects_query(after)
                    levels = ['data', 'projects', 'nodes']
                if resp := safe_json_response(
                    self.gitlab_api.generate_post_request(source, token, None, data=json_dumps(query), graphql_query=True)):
                    for project in dig(resp, *levels, default=[]):
                        yield project
                    page_info = dig(resp, *levels[:-1], 'pageInfo', default={})
                    if cursor := page_info.get('endCursor'):
                        after = cursor
                    if page_info.get('hasNextPage', False) is False:
                        break
        except Exception as e:
            print(e)

    def genericGet(self, host, token, api):
        return safe_json_response(self.gitlab_api.generate_get_request(host=host, token=token, api=api))

    def getApplicationInfo(self, host, token):
        return self.genericGet(host, token, self.app_api_url)

    def getVersion(self, host, token):
        return self.genericGet(host, token, self.app_ver_url)

    def getArchivedProjectCount(self, host, token):
        if resp := self.gitlab_api.generate_get_request(host=host, token=token, api='projects?archived=True'):
            result = resp.headers.get('X-Total')
            return result

    def get_total_project_count(self, host, token, group_id):
        if resp := self.gitlab_api.generate_get_request(host=host, token=token, api=f'/groups/{group_id}/projects'):
            result = resp.headers.get('X-Total')
            return result

    def build_initial_results(self, project):
        return {
            'Project': project.get('name'),
            'ID': project.get('id'),
            'archived': project.get('archived'),
            'last_activity_at': project.get('lastActivityAt'),
            'URL': project.get('webUrl'),
            'namespace': dig(project, 'namespace', 'fullPath'),
            'mirror': project.get('mirror')
        }

    def get_all_project_data(self, host, token, p):
        results = {}
        flags = []
        messages = ''
        if isinstance(p, dict) and p:
            results = self.build_initial_results(p)
            pid = int(p.get('id','').split('/')[-1])
            p['id'] = pid
            statistics = p.get('statistics')
            # if self.output_to_screen:
            #     print('+' * 40)
            #     print(f"Name: {p.get('name')} ID: {pid}")
            #     print(f"Desc: {p.get('description')}")
            #     print(f"Archived: {p.get('archived')}")
            headers = {
                'PRIVATE-TOKEN': token
            }

            # Get the full project info with stats
            messages = FlagRemediationMessages(p.get('name'))
            full_stats_url = self.proj_info_get(pid, host)

            self.check_full_stats(
                full_stats_url,
                p,
                results,
                headers=headers
            )

            try:
                # Get number of pipelines per project
                pipeline_endpoint = f"projects/{pid}/pipelines"
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_num_pl, p, host, token, pipeline_endpoint, "Pipelines", "Pipelines_over", results),
                    "pipelines",
                    limits.PIPELINES_COUNT))

                # Get number of issues per project
                issues_endpoint = f"projects/{pid}/issues"
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_num_issues, p, host, token, issues_endpoint, "Issues", "Issues_over", results),
                    "issues",
                    limits.ISSUES_COUNT))

                # Get number of branches per project
                branches_endpoint = f"projects/{pid}/repository/branches"
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_num_br, p, host, token, branches_endpoint, "Branches", "Branches_over", results),
                    "branches",
                    limits.BRANCHES_COUNT))
                
                # Get number of commits per project
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_num_commits, p, host, token, None, "Commits", "Commits_over", results),
                    "commits",
                    limits.COMMITS_COUNT))

                # Get number of merge requests per project
                mrequests_endpoint = f"projects/{pid}/merge_requests"
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_num_mr, p, host, token, mrequests_endpoint, "Merge Requests", "Merge Requests_over", results),
                    "merge_requests",
                    limits.MERGE_REQUESTS_COUNT))

                # Get number of tags per project
                tags_endpoint = f"projects/{pid}/repository/tags"
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_num_tags, p, host, token, tags_endpoint, "Tags", "Tags_over", results),
                    "tags",
                    limits.TAGS_COUNT))

                # Get list of package types
                self.handle_packages(p, pid, host, token,
                                    messages, flags, results)

                # Check repository size
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_repository_size, p, host, token, None, "Repository", "repository_size_over", results),
                    "repo_size",
                    limits.REPOSITORY_SIZE))
                
                # Check storage size
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_storage_size, p, host, token, None, "Storage", "storage_size_over", results),
                    "storage_size",
                    limits.STORAGE_SIZE))

                # Get total packages size
                flags.append(self.handle_check(
                    messages,
                    self.check_x_total_value_update_dict(
                        utils.check_packages_size, p, host, token, None, "Packages", "packages_size_over", results),
                    "packages_size",
                    limits.PACKAGES_SIZE))
                
                # TODO: GET single project statistics when listing group projects
                if statistics:
                    results['Total Packages Size'] = statistics.get(
                        "packagesSize", 0)

                # Get container registry size
                results['Container Registry Size'], flag_registries = self.get_registry_size(
                    p['fullPath'], host, token)
                self.handle_check(messages, flag_registries, 'container_registries',
                                limits.CONTAINERS_SIZE)
            except Exception:
                log.error(print_exc())
            finally:
                return flags, messages, results
        else:
            return flags, messages, results

    def get_token_owner(self, host, token):
        return self.genericGet(host, token, "user")

    def handle_check(self, messages, flagged_asset, asset_type, flag_condition):
        if flagged_asset == True:
            messages.add_flag_message(asset_type, flag_condition)
        return flagged_asset

    def get_user_data(self, u):
        return from_dict(data_class=User, data=u)
    
    def get_result_value(self, results, value_column_name):
        key_mapping = {
            'Storage': 'storage_size',
            'Repository': 'repository_size',
            'Packages': 'packages_size',
            'Commits': 'commit_count'
        }

        # Get the actual key to use in results
        actual_key = key_mapping.get(value_column_name, value_column_name)

        # Return the value from results or 0 if not found
        return results.get(actual_key, 0)

    def handle_packages(self, project, pid, host, token, messages, flags, results):
        if project.get('packages_enabled', False):
            packages_in_use = set()
            for package in self.gitlab_api.list_all(host, token, self.proj_packages_url(pid)):
                if isinstance(package, dict):
                    packages_in_use.add(package.get("package_type", ""))
                else:
                    log.error(
                        f"failed to get project {pid} packages; expected dict got str or something else; '{package}'")

            results['Package Types In Use'] = ", ".join(
                packages_in_use) if packages_in_use else "N/A"
            # If a package type is found that doesn't match the constant in the class, raise a flag
            any_unsupported_packages = any(
                p not in self.supported_package_types for p in packages_in_use)
            if packages_in_use and any_unsupported_packages:
                flags.append(True)
                self.handle_check(messages, True, "packages",
                                  copy(results['Package Types In Use']))
