__author__ = 'toxaz'

import math
import numpy as np
import pandas as pd
import pyhs2
import scipy.stats as st
from datetime import *


conn = pyhs2.connect(host='nif-nif.zvq.me', port=10000, authMechanism="NOSASL", user='hive', password='test',
                     database='default')
cur = conn.cursor()

cur.execute(
    'select u.zuid as user_id, min(registered) as reg, min(packet_date) as active, min(added) as subscribed from u '
    'left join (select * from playevent where play_duration >= 30 and ok_flag) a on (u.zuid = a.user_id) '
    'left join (select * from app_subscription where not is_trial) b on (a.user_id = b.user_id) '
    'where u.registered is not null group by zuid')
table = cur.fetch()
cur.close()
conn.close()

headers = ['id', 'registered', 'activated', 'subscribed']
raw_table = pd.DataFrame(table, columns=headers)
raw_table = raw_table[raw_table.registered > "2014-06-29"]
raw_table.sort(['registered'], ascending=[True])

# for row_num in raw_table.index:
# if raw_table.landed[row_num] == None:
#         raw_table.landed[row_num] = np.NaN
#     if raw_table.activated[row_num] == None:
#         raw_table.activated[row_num] = np.NaN
#     if raw_table.subscribed[row_num] == None:
#         raw_table.subscribed[row_num] = np.NaN

raw_table['activation'] = ''
raw_table['subscription'] = ''

for i in xrange(len(raw_table.activated) - 1000):
    n = i + 1000
    c_reg = (pd.Series(raw_table.registered[i:n]).count())
    c_act = (pd.Series(raw_table.activated[i:n]).count())
    c_sub = (pd.Series(raw_table.subscribed[i:n]).count())
    share_a = round((c_act / c_reg), 5)
    share_s = round((c_sub / c_act), 5)
    # print c_reg, c_act, c_sub, round(share_a, 5), round(share_s, 5),
    raw_table.activation[n + 1] = share_a
    raw_table.subscription[n + 1] = share_s

print (raw_table)


def cgsize(goal, significance=None, power=None, exp_diff=None):
    if exp_diff is None:
        exp_diff = 100
    if significance is None:
        significance = 0.95
    if power is None:
        power = 0.8
    z_sign = st.norm.ppf(1 - ((1 - significance) / 2))
    z_power = st.norm.ppf(power)

    if goal == 'activation':
        stdev = np.std('raw_table.' + goal)
        print stdev
        control_size = (math.pow(z_sign + z_power, 2) * math.pow(stdev, 2)) / math.pow(stdev / exp_diff, 2)
        return control_size
    elif goal == 'subscription':
        stdev = np.std('raw_table.' + goal)
        print stdev
        control_size = (math.pow(z_sign + z_power, 2) * math.pow(stdev, 2)) / math.pow(stdev / exp_diff, 2)
        return control_size
    else:
        raise AttributeError("provide valid KPI: 'activation' or 'subscription'")


print cgsize('activation')
