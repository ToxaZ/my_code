#!/usr/bin/env python
# coding: utf-8
"""
utility for calculating funnels using conversion metrics processor
steps calc settings stored in query.yaml
first sys argument is a provided funnel type
funnel steps passed as command-line arguments where agrument = query name
ex. "python funnel_calc.py app_opened trial subscription"

author -- ToxaZ
"""

from pyanalytics.kpi2.metrics.conversion_utils.processor import funnel, time_based_funnel, super_funnel, time_based_super_funnel
import logging
import argparse
import yaml
import pandas as pd

# supressing unneccessary output
logging.basicConfig(level=logging.INFO)
logging.getLogger('elasticsearch').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)


def get_queries(query_yaml, funnel_steps, time_unit=None):
    '''acquiring queries from provided funnel_steps names'''
    with open(query_yaml, 'r') as f:
        all_queries = yaml.load(f)
    filtered_queries = []
    for each in funnel_steps:
        if each not in all_queries:
            raise ValueError('invalid funnel step {0}'.format(each))
        else:
            filtered_queries.append(all_queries[each])

    # changing default queries time unit for provided:
    if time_unit is not None:
        for query in filtered_queries:
            query['time_unit'] = time_unit
    return filtered_queries


def make_request(funnel_type, funnel_query):
    '''making funnel request for certain funnel_type and provided list of queries'''
    if funnel_type == 'funnel':
        return funnel(*funnel_query)
    elif funnel_type == 'super_funnel':
        return super_funnel(*funnel_query)
    elif funnel_type == 'time_based_funnel':
        return time_based_funnel(*funnel_query)
    elif funnel_type == 'time_based_super_funnel':
        return time_based_super_funnel(*funnel_query)
    else:
        raise ValueError(
            'invalid funnel_type {0}'
            '(not "funnel", "time_based_funnel", "super_funnel", "time_based_super_funnel")'
            .format(funnel_type)
        )


def time_based_super_funnel_to_df(results):
    '''converting tb super funnel results to dataframe'''
    first_run = True
    fields = []
    dates = []
    values = []
    for time_unit, values_list in results.items():
        dates.append(time_unit)
        val = []
        tmp_fields = []
        for item in values_list:
            val.append(item['value'])
            tmp_fields.append(str(item['field']) + " " + str(item['name']))

        # checking fields consistency
        if first_run:
            fields = tmp_fields
            first_run = False
        else:
            if fields != tmp_fields:
                raise ValueError('item fields are not the same')

        values.append(val)
    return pd.DataFrame(values, index=dates, columns=fields)


def main():
    '''main script logic'''
    # parsing command-line arguments
    parser = argparse.ArgumentParser(description='Processing zvq funnels using conversion utils processor '
                                    '(https://github.com/dreamindustries/zvq-report/tree/master/pyanalytics/kpi2/metrics/conversion_utils).')
    parser.add_argument('-s', '--super', help='return superfunnel instead of common funnel, '
                        'superfunnel allows to aggregate multiple identifiers.',
                        action="store_true")
    parser.add_argument('-t', '--time_based', help='splitting funnel by time units,'
                        'requires specifying a unit ("day", "week" or "month").',
                        type=str, choices=['day', 'week', 'month'], default=None)
    parser.add_argument('funnel_steps', nargs='+', help='names of funnel steps in config file')
    args = parser.parse_args()

    # checking for selected funnel type and obtaining funnel steps
    if args.super is False and args.time_based is None:
        funnel_type = 'funnel'
    elif args.super is False and args.time_based in ('day', 'week', 'month'):
        funnel_type = 'time_based_funnel'
    elif args.super is True and args.time_based is None:
        funnel_type = 'super_funnel'
    elif args.super is True and args.time_based in ('day', 'week', 'month'):
        funnel_type = 'time_based_super_funnel'
    else:
        raise ValueError('invalid funnel_type')

    funnel_steps = args.funnel_steps
    query_file = 'query.yaml'
    if args.super is True:
        query_file = 'super_query.yaml'
    print funnel_steps
    print get_queries(
                    query_file, funnel_steps, args.time_based
                    )

    if funnel_type == 'time_based_super_funnel':
        return time_based_super_funnel_to_df(
            make_request(
                funnel_type, get_queries(
                    query_file, funnel_steps, args.time_based
                )
            )
        )
    elif funnel_type == 'super_funnel':
        return pd.DataFrame(
            make_request(
                funnel_type, get_queries(
                    query_file, funnel_steps, args.time_based
                    )
                ),
        ).transpose()
    else:
        return pd.DataFrame(
            make_request(
                funnel_type, get_queries(
                    query_file, funnel_steps, args.time_based
                    )
                ),
            funnel_steps
        ).transpose()

# if __name__ == '__main__':
#     main

print main()
