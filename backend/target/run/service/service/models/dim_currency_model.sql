
  
    USE [AdventureWorks2022];
    USE [AdventureWorks2022];
    
    

    

    
    USE [AdventureWorks2022];
    EXEC('
        create view "dbo"."dim_currency_model__dbt_tmp__dbt_tmp_vw" as -- models/dim_currency_model.sql

SELECT
    CurrencyKey,
    CurrencyName,
    CurrencyAlternateKey
FROM "AdventureWorks2022"."dbo"."DimCurrency";
    ')

EXEC('
            SELECT * INTO "AdventureWorks2022"."dbo"."dim_currency_model__dbt_tmp" FROM "AdventureWorks2022"."dbo"."dim_currency_model__dbt_tmp__dbt_tmp_vw" 
    OPTION (LABEL = ''dbt-sqlserver'');

        ')

    
    EXEC('DROP VIEW IF EXISTS dbo.dim_currency_model__dbt_tmp__dbt_tmp_vw')



    
    use [AdventureWorks2022];
    if EXISTS (
        SELECT *
        FROM sys.indexes with (nolock)
        WHERE name = 'dbo_dim_currency_model__dbt_tmp_cci'
        AND object_id=object_id('dbo_dim_currency_model__dbt_tmp')
    )
    DROP index "dbo"."dim_currency_model__dbt_tmp".dbo_dim_currency_model__dbt_tmp_cci
    CREATE CLUSTERED COLUMNSTORE INDEX dbo_dim_currency_model__dbt_tmp_cci
    ON "dbo"."dim_currency_model__dbt_tmp"

   


  