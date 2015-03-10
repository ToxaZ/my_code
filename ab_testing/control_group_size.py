__author__ = 'toxaz'
import math
import scipy.stats as st


def cgsize(mean, stdev, significance=None, power=None, exp_diff=None):
    if exp_diff is None:
        exp_diff = 100
    if significance is None:
        significance = 0.95
    if power is None:
        power = 0.8
    z_sign = st.norm.ppf(1 - ((1 - significance) / 2))
    z_power = st.norm.ppf(power)
    control_size = (math.pow(z_sign + z_power, 2) * math.pow(stdev, 2)) / math.pow(mean / exp_diff, 2)
    return int(round(control_size, 0))

# print (cgsize(0.47038, 0.077125517, significance=0.95, exp_diff=50))
# print (cgsize(0.00217, 0.0009680309, significance=0.95, exp_diff=5))
print (cgsize(12.0, 3.2, exp_diff=16.0, significance=0.9, power=0.9))

print st.norm.ppf(0.9)