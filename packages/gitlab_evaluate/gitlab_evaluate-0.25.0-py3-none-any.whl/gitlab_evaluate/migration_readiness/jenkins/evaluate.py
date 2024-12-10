import os
from dacite import from_dict
from gitlab_evaluate.migration_readiness.jenkins.data_classes.plugin import JenkinsPlugin
from sklearn.cluster import KMeans
import numpy as np
import torch.nn as nn
import torch
import sqlite3
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
from gitlab_ps_utils.processes import MultiProcessing
from gitlab_evaluate.migration_readiness.jenkins.jenkins import MultiProcessJenkins
from gitlab_evaluate.migration_readiness.jenkins.auto_encoder import AutoEncoder
from gitlab_evaluate.migration_readiness.jenkins.simple_neural_network import SimpleNN

class JenkinsEvaluateClient():
    def __init__(self, host, user, token, ssl_verify, processes=None) -> None:
        self.setup_db()
        self.processes = processes
        self.server = MultiProcessJenkins(host, username=user, password=token, ssl_verify=ssl_verify, processes=self.processes)
        self.user = self.server.get_whoami()
        self.version = self.server.get_version()
        self.plugins = self.server.get_plugins_info()
        self.jobs, self.job_types = self.server.get_all_jobs()
        self.multi = MultiProcessing()

    def setup_db(self):
        if os.path.exists('jenkins.db'):
            os.remove('jenkins.db')
        con = sqlite3.connect('jenkins.db', check_same_thread=False)
        cur = con.cursor()
        cur.execute("CREATE TABLE jobs(_class, name, url, color, fullName UNIQUE)")
        cur.execute("CREATE TABLE job_types(type)")
        cur.execute("CREATE TABLE jobs_to_process(id UNIQUE, job)")
        con.commit()
        con.close()
    
    def drop_tables(self):
        con = sqlite3.connect('jenkins.db')
        cur = con.cursor()
        cur.execute("DROP TABLE jobs")
        cur.execute("DROP TABLE job_types")
        con.commit()
        con.close()

    def list_of_plugins(self):
        for plugin in self.plugins:
            yield from_dict(JenkinsPlugin, plugin)

    def build_job_data(self, job):
        job_name = job['fullName']
        job_history = self.get_job_history(job_name)
        total_executions = len(job_history)
        total_duration = sum(build['duration'] for build in job_history)
        success_count = sum(1 for build in job_history if build['result'] == 'SUCCESS')
        avg_duration = total_duration / total_executions if total_executions > 0 else 0
        success_rate = success_count / total_executions if total_executions > 0 else 0

        resource_usage = self.get_resource_usage(job_name)

        return {
            'fullname': job.get('fullName', "N/A"),
            'name': job_name,
            'url': job.get('url', "N/A"),
            'color': job.get('color', "N/A"),
            '_class': job.get('_class', "N/A"),
            'execution_frequency': total_executions,
            'avg_duration': avg_duration,
            'success_rate': success_rate,
            'cpu_usage': resource_usage['cpu'],
            'memory_usage': resource_usage['memory']
        }
    
    def build_full_job_list(self):
        return list(self.multi.start_multi_process(self.build_job_data, self.jobs, processes=self.processes))

    def get_job_history(self, job_name):
        # Retrieve job build history and return relevant data
        builds = self.server.get_job_info(job_name).get('builds', [])
        build_data = []
        for build in builds:
            build_info = self.server.get_build_info(job_name, build.get('number'))
            build_data.append({
                'number': build.get('number', 'N/A'),
                'duration': build_info.get('duration', 0),
                'result': build_info.get('result', 'UNKNOWN'),
                'timestamp': build_info.get('timestamp', 0)
            })
        return build_data

    def get_resource_usage(self, job_name):
        # Placeholder for retrieving resource usage data
        # This would require Jenkins plugins or additional monitoring tools
        return {
            'cpu': 'N/A',
            'memory': 'N/A'
        }
    
    def train_predictive_model(self, job_data):
        input_size = 2
        hidden_size = 10
        output_size = 1
        model = SimpleNN(input_size, hidden_size, output_size)
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        X = np.array([[job['execution_frequency'], job['avg_duration']] for job in job_data])
        y = np.array([job['success_rate'] for job in job_data])
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        y = y.reshape(-1, 1)

        dataset = TensorDataset(torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32))
        dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

        model.train()
        for epoch in range(100):  # loop over the dataset multiple times
            for inputs, targets in dataloader:
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        return model, scaler

    def predict_impact(self, model, scaler, job):
        model.eval()
        inputs = scaler.transform([[job['execution_frequency'], job['avg_duration']]])
        inputs = torch.tensor(inputs, dtype=torch.float32)
        output = model(inputs).item()
        return output

    def train_anomaly_detection_model(self, job_data):
        input_size = 3
        hidden_size = 2
        model = AutoEncoder(input_size, hidden_size)
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        X = np.array([[job['execution_frequency'], job['avg_duration'], job['success_rate']] for job in job_data])
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        dataset = TensorDataset(torch.tensor(X, dtype=torch.float32))
        dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

        model.train()
        for epoch in range(100):  # loop over the dataset multiple times
            for inputs, in dataloader:
                outputs = model(inputs)
                loss = criterion(outputs, inputs)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        return model, scaler

    def detect_anomalies(self, model, scaler, job_data):
        model.eval()
        X = np.array([[job['execution_frequency'], job['avg_duration'], job['success_rate']] for job in job_data])
        X = scaler.transform(X)
        inputs = torch.tensor(X, dtype=torch.float32)
        outputs = model(inputs)
        losses = ((outputs - inputs) ** 2).mean(dim=1).detach().numpy()

        return losses > np.percentile(losses, 95)
    
    def cluster_jobs(self, job_data):
        # Convert job data to a suitable format for clustering
        job_features = np.array([[job['execution_frequency'], job['avg_duration'], job['success_rate']] for job in job_data])
        kmeans = KMeans(n_clusters=min(3, len(job_data)), random_state=0).fit(job_features)
        return kmeans.labels_
