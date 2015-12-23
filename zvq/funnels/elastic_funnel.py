__author__ = 'ToxaZ'

from pyanalytics.kpi2.metrics.conversion_utils.processor import funnel, time_based_funnel
import logging
import sys
import yaml
import pandas as pd

logging.basicConfig(level=logging.INFO)
logging.getLogger('elasticsearch').setLevel(logging.WARNING)

def get_queries():
    queries = []
    with open('query.yaml', 'r') as f:
        doc = yaml.load_all(f)
        for d in doc:
            queries.append(d.copy())
    return queries


def make_request(time_based=True):
    first_query_step_funnel = {}
    queries = []
    if time_based is True:
        for funnel_step in sys.argv[1:]:
            for q in get_queries():
                if funnel_step == q['name']:
                    if q['name'] == sys.argv[1]:
                        first_query_step_funnel = q['query']
                    else:
                        queries.append(q['query'].copy())
        return time_based_funnel(first_query_step_funnel, queries)
    if time_based is False:
        for funnel_step in sys.argv[1:]:
            for q in get_queries():
                queries.append(q['query'].copy())
        return funnel(queries)


def df_results(funnel_response):
    df = pd.DataFrame(funnel_response, index=sys.argv[1:])
    return df.transpose()


print df_results(make_request())
