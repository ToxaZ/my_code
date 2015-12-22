__author__ = 'ToxaZ'

from pyanalytics.kpi2.metrics.conversion_utils.processor import funnel, time_based_funnel
import logging
import sys
import yaml
import pandas as pd

logging.basicConfig(level=logging.INFO)
logging.getLogger('elasticsearch').setLevel(logging.WARNING)

json_ex = {'2015-05-01': [3787, 2128, 128], '2015-10-01': [59716, 42404, 426], '2015-03-01': [9713, 6018, 357], '2015-12-01': [20636, 4781, 66], '2014-12-01': [5, 5, 4], '2015-08-01': [15634, 11025, 184], '2015-02-01': [15, 11, 7], '2015-06-01': [4134, 2463, 108], '2015-09-01': [40797, 30107, 210], '2015-04-01': [5234, 3046, 189], '2014-11-01': [3, 2, 1], '2015-11-01': [51560, 35621, 292], '2015-07-01': [6164, 3449, 109], '2015-01-01': [1, 1, 1]}


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
    for funnel_step in sys.argv[1:]:
        for q in get_queries():
            if funnel_step == q['name']:
                if q['name'] == sys.argv[1]:
                    first_query_step_funnel = q['query']
                else:
                    queries.append(q['query'].copy())
    return time_based_funnel(first_query_step_funnel, queries)


def results_to_dataframe(funnel_response):
    df = pd.DataFrame(funnel_response, index=sys.argv[1:])
    return df.transpose()


print make_request()
