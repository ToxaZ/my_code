#!/bin/env bash

set -e

ZA_537=(
    "install_ios registration_agg_by_app_instance" 
    "app_opened_ios active_query_ios"
    "app_opened_ios time_based_trial time_based_subscription" 
    "app_opened_android active_query_android" "app_opened_android time_based_trial time_based_subscription")
ZA_418=(
    "web_users_agg_by_cookie registration_agg_by_user_cookie move_to_zvooq_plus_agg_by_user_cookie"
    "move_to_zvooq_plus payture_gate_shown payture_gate_purchase_clicked time_based_subscription"
    )

for funnel in "${ZA_418[@]}";
do 
    echo "$funnel"
    echo ---
    python funnel_calc.py $funnel
    echo ---
done
