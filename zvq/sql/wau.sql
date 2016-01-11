select
    first_day_of_week(day) as week,
    count(distinct user_id) as wau
from
    playevent
where
    good_app != 'fonoteka'
    and ok_flag = true
group by
    first_day_of_week(day)
order by
    week
