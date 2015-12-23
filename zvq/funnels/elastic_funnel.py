__author__ = 'ToxaZ'

from pyanalytics.kpi2.metrics.conversion_utils.processor import funnel, time_based_funnel
import logging
import sys
import yaml
import pandas as pd

logging.basicConfig(level=logging.INFO)
logging.getLogger('elasticsearch').setLevel(logging.WARNING)


def get_queries():
    with open('query.yaml', 'r') as f:
        doc_queries = yaml.load(f)
    return doc_queries


def make_request(time_based=True):
    first_query_step_funnel = {}
    queries = []
    funnel_query = map(lambda x: get_queries().get(x), sys.argv[1:])

    if time_based is True:
        return time_based_funnel(funnel_query[0], funnel_query[1:])
    if time_based is False:
        return funnel(funnel_query)


def dataframe_results(funnel_response):
    df = pd.DataFrame(funnel_response, index=sys.argv[1:])
    return df.transpose()


print dataframe_results(make_request())
