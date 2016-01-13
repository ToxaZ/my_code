select
    count(distinct subs.user_id) as cnt,
    subs.country
from
    (
    select
        pl.user_id,
        dense_rank() over(partition by pl.user_id order by pl.packet_date desc) as rank,
        pl.country
    from 
        playevent as pl
    where
        pl.user_id not in (
            select
                a.user_id
            from
                app_subscription as a
            where
                a.is_trial = false
                and a.app in ('openplay', 'zvooq')
                and year(a.added) = 2015
                and month(a.added) = 11
            group by
                a.user_id
        )
        and year(pl.day) = 2015
        and month(pl.day) = 11
    group by
        pl.user_id,
        pl.packet_date,
        pl.country
    ) as subs
where
    subs.rank = 1
group by
    subs.country
order by
    cnt desc
