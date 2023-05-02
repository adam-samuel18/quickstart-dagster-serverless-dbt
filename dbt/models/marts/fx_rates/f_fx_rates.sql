{{ config(
    tags=['daily','early_morning']
) }}

select * from {{ ref('int_fx_rates') }}
