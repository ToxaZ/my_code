select
    month(day) as month,
    year(day) as year,
    count(distinct user_id) as mau
from
    playevent
where
    ok_flag = true
    and good_app = 'fonoteka'
group by
    month(day),
    year(day)
order by
    year,
    month
