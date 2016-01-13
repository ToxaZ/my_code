--preprocess
with
    --fitering playevents
    filtered_playevent as (
        select distinct
            from_unixtime(
                unix_timestamp(packet_date)
            ,'yyyy-MM-01') as month,
            user_id,
            case 
                when good_app = 'web' 
                then good_app 
                else good_phone_type 
            end as app
        from 
            playevent
        where
            ok_flag = true
            and (
                (
                    good_phone_type is null 
                    and good_app = 'web'
                ) 
                or (
                    good_app = 'openplay' 
                    and (
                        good_phone_type = 'ios' 
                        or good_phone_type = 'android'
                    )
                )
            )
    ),
    --creating registration date table
    reg_date as (
        select
            min(month) as regdate,
            user_id
        from
            filtered_playevent
        group by
            user_id
        having
            min(month) >= '2014-07-01'      
    )

-- running queries for different app retention
select
    count(distinct pl.user_id) as cnt,
    regdate,
    round(
        datediff(month, regdate)/30
    ) as month,
    app
from
    filtered_playevent as pl
    inner join
    reg_date as rd
    on (
        pl.user_id = rd.user_id
    )
group by
    regdate,
    round(
        datediff(month, regdate)/30
    ),
    app

-- concatenating results from query for total retention
union all
select
    count(distinct pl.user_id) as cnt,
    regdate, 
    round(
        datediff(month, regdate)/30
    ) as month, 
    'total' as app
from
    filtered_playevent as pl
    inner join
    reg_date rd 
    on (
        pl.user_id = rd.user_id
    )
group by
    regdate,
    round(
        datediff(month, regdate)/30
    )
