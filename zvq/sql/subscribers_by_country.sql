select
    count(distinct user_id) as cnt,
    country
from
    (
    select
        user_id,
        dense_rank() over(partition by user_id order by packet_date desc) as rank,
        country
    from 
        playevent
    where
        user_id in (
            select
                user_id
            from
                app_subscription
            where
                is_trial = false
                and app in ('openplay', 'zvooq')
                and year(added) = 2015
                and month(added) = 11
            group by
                user_id
        )
    group by
        user_id,
        packet_date,
        country
    ) as ranked_subs
where
    rank = 1
group by
    country
order by
    cnt desc
