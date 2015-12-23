#!/usr/bin/env python
# coding: utf-8
"""
utility for calculating funnels using conversion metrics processor
steps calc settings stored in query.yaml
funnel steps passed as command-line arguments where agrument = query name
ex. "python funnel_calc.py app_opened trial subscription"

author -- ToxaZ
"""

from pyanalytics.kpi2.metrics.conversion_utils.processor import funnel, time_based_funnel
import logging
import sys
import yaml
import pandas as pd

# supressing huge elasticsearch output
logging.basicConfig(level=logging.INFO)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)
# comment below to recieve elasticsearch servers status
logging.getLogger('urllib3').setLevel(logging.ERROR)


def get_queries():
    with open('query.yaml', 'r') as f:
        doc_queries = yaml.load(f)
    return doc_queries


def make_request(time_based=True):
    first_query_step_funnel = {}
    queries = []

    # retrieving queries for funnel steps names passed from command-line
    funnel_query = map(lambda x: get_queries().get(x), sys.argv[1:])

    if time_based is True:
        return time_based_funnel(funnel_query[0], funnel_query[1:])
    if time_based is False:
        return funnel(funnel_query)


def dataframe_results(funnel_response):
    df = pd.DataFrame(funnel_response, index=sys.argv[1:])
    return df.transpose()


def run_funnel():
    dataframe_results(make_request())

if __name__ == '__main__':
    run_funnel()
