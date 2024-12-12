#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dq_client
----------------------------------

Tests for `dq` module.
"""

import pytest

import dq.error
from dq import DQClient


def test_import():
    """Sample pytest test function.
    """
    import dq
    assert 1 == 1


@pytest.fixture(scope="session")
def dq_client():
    client = DQClient("https://app.dataquality.pl", "", "")
    # with  as client:
    yield client


def test_client_status(dq_client):
    with pytest.raises(dq.error.DQError, match='401'):
        dq_client.account_status()


def test_client_jobs(dq_client):
    with pytest.raises(dq.error.DQError, match='401'):
        dq_client.list_jobs()()


def test_client_create_job(dq_client):
    from dq import JobConfig
    input_data = '''"ID","ADRES"
    6876,"34-404, PYZÓWKA, PODHALAŃSKA 100"
    '''
    job_config = JobConfig('my job')
    with pytest.raises(dq.error.DQError, match='401'):
        dq_client.submit_job(job_config, input_data=input_data)


def test_client_job_state(dq_client):
    from dq import JobConfig
    with pytest.raises(dq.error.DQError, match='401'):
        dq_client.job_state('')


def test_client_job_cancel(dq_client):
    from dq import JobConfig
    # with pytest.raises(dq.error.DQError, match='401'):
    dq_client.cancel_job('')
    assert 1


def test_client_job_report(dq_client):
    with pytest.raises(dq.error.DQError, match='401'):
        dq_client.job_report('')


def test_client_job_results(dq_client):
    with pytest.raises(dq.error.DQError, match='401'):
        dq_client.job_results('', 'output.csv')


def test_client_job_delete(dq_client):
    # with pytest.raises(dq.error.DQError, match='401'):
    dq_client.delete_job('')
    assert 1
