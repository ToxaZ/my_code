select
    month(day) as month,
    year(day) as year,
    count(distinct user_id) as mau
from
    playevent
where
    good_app != 'fonoteka'
    and ok_flag = true
group by
    month(day),
    year(day)
order by
    year,
    month
