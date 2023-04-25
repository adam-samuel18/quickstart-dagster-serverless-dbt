{{ config(
    tags=['daily','early_morning']
) }}

select * from {{ ref('stg_forex__fx_rates') }}