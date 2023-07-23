with t1 as (select * from {{ ref("stg_stripe__payments") }}) select 1 as id
