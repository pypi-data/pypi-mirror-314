from sys import exit as sys_exit
import xlsxwriter
from dacite import from_dict
from gitlab_ps_utils.json_utils import json_pretty
from gitlab_ps_utils.api import GitLabApi
from gitlab_ps_utils.processes import MultiProcessing
from gitlab_ps_utils.misc_utils import is_error_message_present
from gitlab_evaluate import log
from gitlab_evaluate.lib import utils
from gitlab_evaluate.lib.api_models.application_stats import GitLabApplicationStats
from gitlab_evaluate.migration_readiness.gitlab import evaluate as evaluateApi


class ReportGenerator():
    def __init__(self, host, token, filename=None, output_to_screen=False, evaluate_api=None, processes=None):
        self.host = host
        self.token = token
        self.evaluate_api = evaluate_api if evaluate_api else evaluateApi.EvaluateApi(
            GitLabApi())
        self.validate_token()
        if filename:
            self.workbook = xlsxwriter.Workbook(f'{filename}.xlsx')
        else:
            self.workbook = xlsxwriter.Workbook('evaluate_report.xlsx')
        self.app_stats = self.workbook.add_worksheet('App Stats')
        self.align_left = self.workbook.add_format({'align': 'left'})
        # Create Header format with a black background
        self.header_format = self.workbook.add_format(
            {'bg_color': 'black', 'font_color': 'white', 'bold': True, 'font_size': 10})
        self.final_report = self.workbook.add_worksheet('Evaluate Report')
        self.workbook.add_format({'text_wrap': True, 'font_size': 10})
        self.flagged_projects = self.workbook.add_worksheet('Flagged Projects')
        self.using_admin_token = self.is_admin_token()
        self.users = self.workbook.add_worksheet('Users')
        self.raw_output = self.workbook.add_worksheet('Raw Project Data')
        self.output_to_screen = output_to_screen
        self.multi = MultiProcessing()
        self.processes = processes
        self.csv_columns = [
            'Project',
            'ID',
            'URL',
            'kind',
            'namespace',
            'mirror',
            'archived',
            'last_activity_at',
            'Pipelines',
            'Pipelines_over',
            'Issues',
            'Issues_over',
            'Branches',
            'Branches_over',
            'commit_count',
            'commit_count_over',
            'Merge Requests',
            'Merge Requests_over',
            'storage_size',
            'storage_size_over',
            'repository_size',
            'repository_size_over',
            'wiki_size',
            "lfs_objects_size",
            "lfs_objects_size_over",
            "job_artifacts_size",
            "job_artifacts_size_over",
            "snippets_size",
            "snippets_size_over",
            "uploads_size",
            "uploads_size_over",
            'Tags',
            'Tags_over',
            'Package Types In Use',
            'Total Packages Size',
            'Container Registry Size',
            'Estimated Export Size',
            'Estimated Export Size Over',
            'Estimated Export Size S3 Over',
            'packages_size_over']
        self.report_headers = [
            'Project',
            'Reason'
        ]
        self.user_headers = [
            'username',
            'email',
            'state',
            'using_license_seat'
        ]
        self.account_headers = [
            'Account',
            'Comments'
        ]
        self.projects_summary_headers = [
            'Projects',
            'ALL PROJECTS',
            'ONLY GROUP PROJECTS',
            'Comments'
        ]
        self.projects_to_review_headers = [
            'Projects To Review',
            'ALL PROJECTS',
            'ONLY GROUP PROJECTS',
            'Comments'
        ]
        self.metrics_headers = [
            'Metrics',
            'ALL PROJECTS',
            'ONLY GROUP PROJECTS',
            'Comments'
        ]
        utils.write_headers(0, self.raw_output,
                            self.csv_columns, self.header_format)
        utils.write_headers(0, self.flagged_projects,
                            self.csv_columns, self.header_format)
        utils.write_headers(0, self.final_report,
                            self.report_headers, self.header_format)
        utils.write_headers(
            0, self.users, self.user_headers, self.header_format)
        # Merging the first two headers of account summary
        self.app_stats.merge_range(
            'A1:B1', self.account_headers[0], self.header_format)
        self.app_stats.merge_range(
            'C1:D1', self.account_headers[1], self.header_format)
        self.final_report.set_default_row(150)
        self.final_report.set_row(0, 20)

    def write_workbook(self):
        self.app_stats.autofit()
        self.final_report.autofit()
        self.flagged_projects.autofit()
        self.raw_output.autofit()
        self.users.autofit()
        self.workbook.close()

    def handle_getting_data(self, group_id):
        # Determine whether to list all instance or all group projects (including sub-groups)
        full_path = None
        if group_id:
            full_path = self.evaluate_api.gitlab_api.generate_get_request(self.host, self.token, f'groups/{group_id}').json()['full_path']
        for flags, messages, results in self.multi.start_multi_process_stream_with_args(self.evaluate_api.get_all_project_data, self.evaluate_api.get_all_projects_by_graphql(
                self.host, self.token, full_path), self.host, self.token, processes=self.processes):
            self.write_output_to_files(flags, messages, results)

    def handle_getting_user_data(self, group_id=None):
        endpoint = f"groups/{group_id}/members" if group_id else "/users?exclude_internal=true&without_project_bots=true"
        for user in self.multi.start_multi_process_stream(self.evaluate_api.get_user_data, self.evaluate_api.gitlab_api.list_all(
                self.host, self.token, endpoint), processes=self.processes):
            utils.append_to_workbook(
                self.users, [user.to_dict()], self.user_headers)

    def get_app_stats(self, source, token, group_id):
        report_stats = []
        additional_info = []
        app_stats = {}
        archived_projects = ""
        error, resp = is_error_message_present(
            self.evaluate_api.getApplicationInfo(source, token))
        if not error:
            app_stats = from_dict(data_class=GitLabApplicationStats, data=resp)
            archived_projects = self.evaluate_api.getArchivedProjectCount(
                source, token)
            report_stats += [
                ('Basic information from source', source),
                ('Customer', '<CUSTOMERNAME>'),
                ('Date Run', utils.get_date_run()),
                ('Evaluate Version', utils.get_package_version()),
                ('Source', '<SOURCE>'),
                ('Total Users', app_stats.users),
                ('Total Active Users', app_stats.active_users),
                ('Total Groups', app_stats.groups),
                ('Total Projects', app_stats.projects),
                ('Total Merge Requests', app_stats.merge_requests),
                ('Total Forks', app_stats.forks),
                ('Total Issues', app_stats.issues),
                ('Total Group Projects', utils.get_countif(
                    self.raw_output.get_name(), 'group', 'D')),
                ('Total User Projects', utils.get_countif(
                    self.raw_output.get_name(), 'user', 'D')),
                ('Total Archived Projects', archived_projects)
            ]
            additional_info += [('Reading the Output',
                                 utils.get_reading_the_output_link())]
        else:
            log.warning(
                f"Unable to pull application info from URL: {source}")

        if resp := self.evaluate_api.getVersion(source, token):
            if len(report_stats) > 0:
                report_stats.insert(1, ('GitLab Version', resp.get('version')))
            else:
                report_stats.append(('GitLab Version', resp.get('version')))
            additional_info.append(
                ('Upgrade Path', utils.get_upgrade_path(resp.get('version'))))
            additional_info.append(
                ('What\'s new', utils.get_whats_changed(resp.get('version'))))
        else:
            log.warning(f"Unable to pull application info from URL: {source}")

        for row, stat in enumerate(report_stats):
            self.app_stats.write(row+1, 0, stat[0])
            if stat[0] == 'Total Group Projects' or stat[0] == 'Total User Projects':
                self.app_stats.write_formula(
                    row+1, 1, '='+stat[1], self.align_left)
            else:
                self.app_stats.write(row+1, 1, stat[1])

        for row, stat in enumerate(additional_info):
            self.app_stats.write(row+1, 2, stat[0])
            self.app_stats.write(row+1, 3, stat[1])

        project_summary_row_start_index = len(report_stats) + 2
        self.get_projects_summary(project_summary_row_start_index,
                                  app_stats, archived_projects, group_id, source, token)

    def get_projects_summary(self, row_start_index, app_stats, archived_projects, group_id, source, token):
        projects_summary = []
        if not app_stats and len(archived_projects) > 0:
            projects_summary += [
                ('Total', app_stats.projects, utils.get_countif(
                    self.raw_output.get_name(), 'group', 'D')),
                ('Active', utils.get_countif(self.raw_output.get_name(), 'Fals*', 'F'),
                 utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Fals*', 'F')),
                ('Archived', archived_projects, utils.get_countifs(
                    self.raw_output.get_name(), 'group', 'D', 'Tru*', 'F')),
                ('Outliers', utils.get_if(utils.get_counta(self.flagged_projects.get_name(), 'A')+'=0', 0, utils.get_counta(self.flagged_projects.get_name(), 'A')+'-1'),
                 utils.get_if(utils.get_countif(self.flagged_projects.get_name(), 'group', 'D')+'=0', 0, utils.get_countif(self.flagged_projects.get_name(), 'group', 'D'))),
            ]
        elif group_id:
            projects_summary += [
                ('Total', self.evaluate_api.get_total_project_count(source, token,
                 group_id), utils.get_countif(self.raw_output.get_name(), 'group', 'D')),
                ('Active', utils.get_countif(self.raw_output.get_name(), 'Fals*', 'F'),
                 utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Fals*', 'F')),
                ('Archived', utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*',
                 'F'), utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'F')),
                ('Outliers', utils.get_if(utils.get_counta(self.flagged_projects.get_name(), 'A')+'=0', 0, utils.get_counta(self.flagged_projects.get_name(), 'A')+'-1'),
                 utils.get_if(utils.get_countif(self.flagged_projects.get_name(), 'group', 'D')+'=0', 0, utils.get_countif(self.flagged_projects.get_name(), 'group', 'D'))),
            ]
        utils.write_headers(row_start_index, self.app_stats,
                            self.projects_summary_headers, self.header_format)
        for row_num, row_data in enumerate(projects_summary):
            for col_num, value in enumerate(row_data):
                if col_num == 0:
                    self.app_stats.write(
                        row_num+row_start_index+1, col_num, value)
                else:
                    self.app_stats.write_formula(
                        row_num+row_start_index+1, col_num, '=' + str(value) if value is not None else '')

        projects_to_review_row_start_index = row_start_index + \
            len(projects_summary) + 2
        self.get_projects_to_review(projects_to_review_row_start_index)

    def get_projects_to_review(self, row_start_index):
        projects_to_review = [
            ('Outlier Projects', utils.get_if(utils.get_counta(self.flagged_projects.get_name(), 'A')+'=0', 0, utils.get_counta(self.flagged_projects.get_name(), 'A')+'-1'),
             utils.get_if(utils.get_countif(self.flagged_projects.get_name(), 'group', 'D')+'=0', 0, utils.get_countif(self.flagged_projects.get_name(), 'group', 'D'))),
            ('Pipelines > 5,000', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'J'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'J')),
            ('Issues > 5,000', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'L'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'L')),
            ('Branches > 1,000', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'N'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'N')),
            ('Commits > 50,000', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'P'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'P')),
            ('Merge Requests > 5,000', utils.get_countif(self.raw_output.get_name(), 'Tru*',
             'Q'), utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'R')),
            ('Storage Size > 20 GB', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'T'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'T')),
            ('Repo Size > 5 GB', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'V'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'V')),
            ('Object Size', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'Y'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'Y')),
            ('Job Artifacts', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'AA'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'AA')),
            ('Snippets', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'AC'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'AC')),
            ('Uploads', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'AE'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'AE')),
            ('Tags > 5000', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'AG'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'AG')),
            ('Export Size > 5 GB', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'AL'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'AL')),
            ('Export Size > 10 GB', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'AM'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'AM')),
            ('Total Packages Size > 20 GB', utils.get_countif(self.raw_output.get_name(), 'Tru*', 'AN'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'Tru*', 'AN')),
        ]
        utils.write_headers(row_start_index, self.app_stats,
                            self.projects_to_review_headers, self.header_format)
        for row_num, row_data in enumerate(projects_to_review):
            for col_num, value in enumerate(row_data):
                if col_num == 0:
                    self.app_stats.write(
                        row_num+row_start_index+1, col_num, value)
                else:
                    self.app_stats.write_formula(
                        row_num+row_start_index+1, col_num, '=' + str(value) if value is not None else '')

        metrics_row_start_index = row_start_index + len(projects_to_review) + 2
        self.get_metrics(metrics_row_start_index)

    def get_metrics(self, row_start_index):
        metrics = [
            ('Pipelines', utils.get_sum(self.raw_output.get_name(), 'H'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'H', 'group')),
            ('Issues', utils.get_sum(self.raw_output.get_name(), 'J'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'J', 'group')),
            ('Branches', utils.get_sum(self.raw_output.get_name(), 'L'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'L', 'group')),
            ('Commits', utils.get_sum(self.raw_output.get_name(), 'N'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'N', 'group')),
            ('Merge Requests', utils.get_sum(self.raw_output.get_name(), 'P'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'P', 'group')),
            ('Storage', utils.get_sum(self.raw_output.get_name(), 'R'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'R', 'group')),
            ('Repo Size', utils.get_sum(self.raw_output.get_name(), 'T'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'T', 'group')),
            ('Object Size', utils.get_sum(self.raw_output.get_name(), 'W'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'W', 'group')),
            ('Job Artifacts', utils.get_sum(self.raw_output.get_name(), 'Y'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'Y', 'group')),
            ('Snippets', utils.get_sum(self.raw_output.get_name(), 'AA'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'AA', 'group')),
            ('Uploads Size', utils.get_sum(self.raw_output.get_name(), 'AC'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'AC', 'group')),
            ('Tags', utils.get_sum(self.raw_output.get_name(), 'AE'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'AE', 'group')),
            ('maven Packages', utils.get_countif(self.raw_output.get_name(), 'maven', 'AG'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'maven', 'AG')),
            ('npm Packages', utils.get_countif(self.raw_output.get_name(), 'npm', 'AG'),
             utils.get_countifs(self.raw_output.get_name(), 'group', 'D', 'npm', 'AG')),
            ('Package Size', utils.get_sum(self.raw_output.get_name(), 'AH'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'AH', 'group')),
            ('Container Size', utils.get_sum(self.raw_output.get_name(), 'AI'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'AI', 'group')),
            ('Export Size', utils.get_sum(self.raw_output.get_name(), 'AJ'),
             utils.get_sumif(self.raw_output.get_name(), 'D', 'AJ', 'group'))
        ]
        utils.write_headers(row_start_index, self.app_stats,
                            self.metrics_headers, self.header_format)
        for row_num, row_data in enumerate(metrics):
            for col_num, value in enumerate(row_data):
                if col_num == 0:
                    self.app_stats.write(
                        row_num+row_start_index+1, col_num, value)
                else:
                    self.app_stats.write_formula(
                        row_num+row_start_index+1, col_num, '=' + str(value) if value is not None else '')

    def write_output_to_files(self, flags, messages, results):
        dict_data = []
        dict_data.append({x: results.get(x) for x in self.csv_columns})
        utils.append_to_workbook(self.raw_output, dict_data, self.csv_columns)

        if True in flags:
            utils.append_to_workbook(
                self.flagged_projects, dict_data, self.csv_columns)
            utils.append_to_workbook(self.final_report, [{'Project': results.get(
                'Project'), 'Reason': messages.generate_report_entry()}], self.report_headers)
        if self.output_to_screen:
            print(f"""
            {'+' * 40}
            {json_pretty(results)}
            """)

    def validate_token(self):
        error, resp = is_error_message_present(
            self.evaluate_api.get_token_owner(self.host, self.token))
        if error:
            log.error("\nToken appears to be invalid. See API response below. Exiting script")
            log.error(resp)
            sys_exit(1)

    def is_admin_token(self):
        user = self.evaluate_api.get_user_data(
            self.evaluate_api.get_token_owner(self.host, self.token))
        return user.is_admin
