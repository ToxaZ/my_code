--preprocess
with
    --filtering subscription
    filtered_app_subscription as (
        select distinct
            from_unixtime(
                unix_timestamp(added),
            'yyyy-MM-01') as month,
            user_id,
            app,
            platform
        from 
            app_subscription
        where
            is_trial = false
            and app != 'fonoteka'
            and price > 5
            and platform in ('apple', 'google', 'zvooq')
            and added <= from_unixtime(unix_timestamp(), 'yyyy-MM-dd')
    ),
    --creating first sub table
    sub_start as (
    select
        min(month) as first_sub,
        user_id
    from
        filtered_app_subscription
    group by
        user_id,
        platform
    having
        min(month) >= '2015-01-01'
        and max(month) < from_unixtime(unix_timestamp(), 'yyyy-MM-dd')
   )

--running queries
select
    count(distinct fas.user_id) as cnt,
    first_sub,
    round(
        datediff(fas.month, ss.first_sub)/30
    ) as month,
    app,
    platform
from
    filtered_app_subscription as fas
inner join
    sub_start ss on (ss.user_id = fas.user_id)
group by
    first_sub,
    round(
        datediff(fas.month, ss.first_sub)/30
    ),
    app,
    platform
