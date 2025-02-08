-- models/dim_currency_model.sql
{{ config(materialized='table') }}
SELECT
    CurrencyKey,
    CurrencyName,
    CurrencyAlternateKey
FROM {{ source('dbo', 'DimCurrency') }}
