-- depends_on: {{ ref("stg_google_analytics__hits") }}
-- depends_on: {{ ref("stg_google_analytics__page_views") }}
-- depends_on: {{ ref("stg_google_ads__url_report") }}
-- depends_on: {{ ref("stg_google_ads__ad_report") }}
-- depends_on: {{ ref("stg_google_ads__campaign_report") }}
select 1 as id
