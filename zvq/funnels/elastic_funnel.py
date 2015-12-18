__author__ = 'ToxaZ'

from pyanalytics.kpi2.metrics.conversion_utils.processor import funnel, time_based_funnel
import logging
import inspect

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('elasticsearch').setLevel(logging.WARNING)

app_opened_query_android = {
    "type": "elastic",
    "q": "NOT properties.app: fonoteka AND properties.os: android",
    "time_unit": "month",
    "index": "cs-app_opened*"
    }

app_opened_query_ios = {
    "type": "elastic",
    "q": "NOT properties.app: fonoteka AND properties.os: iOS",
    "index": "cs-app_opened*",
    "agg_field": "app_instance"
    }

install_vmetro_query = {
    "type": "elastic",
    "q": "properties.sub_site: vmetro",
    "index": "cs-mat_app_install*",
    "agg_field": "app_instance"
    }

install_ios_query = {
    "type": "elastic",
    "q": "properties.mat_app: 'Zvooq iOS'",
    "index": "cs-mat_app_install-2015.1*",
    "agg_field": "app_instance"
    }

active_query_ai = {
    "type": "elastic",
    "q": "NOT properties.app: fonoteka",
    "index": "cs-track_playback*",
    "agg_field": "app_instance"
    }

active_query_android = {
    "type": "elastic",
    "q": "NOT properties.app: fonoteka AND  properties.phoneType: android",
    "index": "cs-playevent*"
    }

active_query_ios = {
    "type": "elastic",
    "q": "NOT properties.app: fonoteka AND  properties.phoneType: ios",
    "index": "cs-playevent*"
    }

app_open_vmetro_query = {
    "type": "elastic",
    "q": "mat_info.sub_site:vmetro",
    "index": "cs-app_opened*"
    }

subscr_query = {
    "type": "psql",
    "q": "select user_id from app_subscription "
    "where is_trial = false and price > 0 and app != 'fonoteka'"
    }

genres_shown_query = {
    "type": "elastic",
    "q": "features: NEW_GENRE_PAGE",
    "index": "cs-main_page_genres_shown*"
}

genres_clicked_query = {
    "type": "elastic",
    "q": "features: NEW_GENRE_PAGE AND properties.url: *\\/genre*",
    "index": "cs-genres_page_clicked*",
    "index": "cs-global_play*"
}

web_users_query = {
    "type": "elastic",
    "q": "properties.app:web AND NOT properties.utm-tags.utm_source:topt",
    "index": "cs-*"
}

web_users_query_agg_by_cookie = {
    "type": "elastic",
    "q": "properties.app:web AND NOT properties.utm-tags.utm_source:topt",
    "index": "cs-*",
    "time_unit": "month",
    "agg_field": "properties.user_cookie"
}


active_10m_query = {
    "type": "hive",
    "q": "select user_id from playevent group by user_id"
    "having sum(play_duration) >= 600"
}

mobile_pop_up_query = {
    "type": "elastic",
    "q": "properties.type: pop-up",
    "index": "cs-mobile_shown*"
}

mobile_pop_up_action_query = {
    "type": "elastic",
    "q": "properties.type: pop-up",
    "index": "cs-mobile_link_requested*",
    "index": "cs-mobile_install_clicked*"
}

app_open_version_query = {
    "type": "elastic",
    "q": "properties.os: android AND properties.app_release: 1.9*",
    "index": "cs-app_opened*",
    "time_unit": "year",
    "agg_field": "app_instance"
}

registration_query_agg_by_app_instance = {
    "type": "elastic",
    "q": "*",
    "index": "cs-authentication_successful*",
    "agg_field": "app_instance"
}

registration_query_agg_by_user_cookie = {
    "type": "elastic",
    "q": "*",
    "index": "cs-authentication_successful*",
    "time_unit": "month",
    "agg_field": "roperties.user_cookie"
}

app_registration_query_elastic = {
    "type": "elastic",
    "q": "properties.os: android AND properties.app_release: 1.10*",
    "index": "cs-authentication_successful*",
}

time_based_trial_query = {
    "type": "psql",
    "q": "select user_id, added from app_subscription "
    "where is_trial = true and app != 'fonoteka'"
}

time_based_subscription_query = {
    "type": "psql",
    "q": "select user_id, added from app_subscription "
    "where is_trial = false and app != 'fonoteka'"
}

# print (time_based_funnel(app_opened_query, [active_query_ai]))
# print (funnel(
#     web_users_query_agg_by_cookie,
#     [registration_query_agg_by_user_cookie]
#     )
# )  # ZA-418
# print(time_based_funnel(web_users_query, [genres_shown_query, genres_clicked_query, active_10m_query])) # ZA-420
# print(time_based_funnel(web_users_query, [mobile_pop_up_query, mobile_pop_up_action_query])) # ZA-419
# print(time_based_funnel(app_open_version_query, [app_inst_registration_query])) # ZA-469
# print(time_based_funnel(app_registration_query, [app_trial_query])) # ZA-469
# print funnel([app_opened_query_ios, active_query_ios], print_query=True) # ZA-537
# print(time_based_funnel(
#     app_opened_query_android,
#     [time_based_trial_query, time_based_subscription_query]
#     )
# )  # ZA-537
# print(time_based_funnel(
#     app_opened_query_android,
#     [active_query_android]
#     )
# )  # ZA-537
print(time_based_funnel(
    app_opened_query_ios,
    [active_query_ios]
    )
)  # ZA-537
