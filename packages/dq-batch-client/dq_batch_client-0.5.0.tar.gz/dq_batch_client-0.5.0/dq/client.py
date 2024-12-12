# -*- coding: utf-8 -*-

import json

from .account import Account
from .error import DQError
from .job import Job, JobReport
from .request_client import RequestClient
from .response import from_response


class DQClient:

    def __init__(self, url, user, token, port=9001, api_ver='v1'):
        self.url = '{}/api/{}'.format(url, api_ver)
        self.port = port
        self.user = user
        self.token = token
        self.request_client = RequestClient(self.url, self.token)

    @from_response(Job)
    def list_jobs(self):
        """ GET 'https://app.dataquality.pl/api/v1/jobs' """
        return self.request_client.get('/jobs')

    @from_response(Job)
    def submit_job(self, config, input_data=None, input_file=None):
        """ POST 'https://app.dataquality.pl/api/v1/jobs' """
        parts = {
            'config': {
                'filename': None,
                'content-type': 'application/json',
                'content': json.dumps(config.data())
            },
            'file': {
                'filename': 'tmp.csv',
                'content-type': 'text/csv',
            }
        }
        if input_data:
            parts['file']['content'] = str(input_data)
        else:
            parts['file']['content'] = open(input_file, 'rb')
        return self.request_client.post_multipart('/jobs', parts=parts)

    def job_state(self, job_id):
        """ GET 'https://app.dataquality.pl/api/v1/jobs/{{job_id}}/status' """
        @from_response()
        def get_response():
            return self.request_client.get('/jobs/{}/status'.format(job_id))
        response = get_response()
        if response is None:
            return None
        return response['status']

    @from_response(JobReport)
    def job_report(self, job_id):
        """ GET 'https://app.dataquality.pl/api/v1/jobs/{{job_id}}' """
        return self.request_client.get('/jobs/{}'.format(job_id))

    def job_results(self, job_id, out_file=None, encoding='utf-8'):
        """ GET 'https://app.dataquality.pl/api/v1/jobs/{{job_id}}/result' """
        response = self.request_client.get('/jobs/{}/result'.format(job_id), encoding=encoding)
        if not response.is_ok():
            raise DQError(status=response.status, message=response.content)
        if out_file:
            with open(out_file, 'w', encoding=encoding) as file:
                file.write(response.content)

    def delete_job(self, job_id):
        """ DELETE 'https://app.dataquality.pl/api/v1/jobs/{{job_id}}' """
        return self.request_client.delete('/jobs/{}'.format(job_id))

    def cancel_job(self, job_id):
        """ PUT 'https://app.dataquality.pl/api/v1/jobs/{{job_id}}/stop' """
        return self.request_client.put('/jobs/{}/stop'.format(job_id))

    @from_response(Account)
    def account_status(self):
        """ GET 'https://app.dataquality.pl/api/v1/account/status' """
        return self.request_client.get('/account/status')
