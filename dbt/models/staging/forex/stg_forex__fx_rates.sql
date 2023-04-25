{{ config(
    tags=['daily','early_morning']
) }}

/* The purpose of this model is to extract useful values from the raw data
.*/ 

select   
    date,
    cast(json_value(raw_json,'$.USD') as numeric) as USD,
    cast(json_value(raw_json,'$.EUR') as numeric) as EUR
from {{ source('forex', 'fx_rates') }}