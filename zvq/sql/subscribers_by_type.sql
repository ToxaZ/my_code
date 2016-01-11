select
    count(distinct user_id) as cnt,
    name
from
    app_subscription
where
    month(added) = 12
    and year(added) >= 2015
    and is_trial = false
    and price > 0
group by
    name
