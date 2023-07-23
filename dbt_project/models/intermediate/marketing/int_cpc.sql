with
    t1 as (select * from {{ ref("stg_google_analytics__hits") }}),
    t2 as (select * from {{ ref("stg_google_analytics__page_views") }})

select 1 as id
