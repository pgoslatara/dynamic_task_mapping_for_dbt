{{ config(enabled=var('ad_reporting__google_ads_enabled', True)) }}
-- depends_on: {{ ref('ad_stats_data') }}
-- depends_on: {{ ref('account_history_data') }}
-- depends_on: {{ ref('campaign_history_data') }}
-- depends_on: {{ ref('ad_group_history_data') }}
-- depends_on: {{ ref('ad_history_data') }}
select 1 as id
