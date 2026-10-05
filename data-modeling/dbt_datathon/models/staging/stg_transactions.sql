with

source as (

    select * from {{ source('datathon_factored', 'transactions') }}

),

renamed as (

    select

        ----------  ids
        _transaction_id as transaction_id,
        product_id,
        customer_id,
        branch_id,

        ----------  text
        transaction_type,
        transaction_category,
        currency,
        channel,
        merchant_name,
        merchant_category,
        transaction_country,
        transaction_city,
        transaction_status,
        response_code,

        ----------  numerics
        amount,
        amount_usd,
        fraud_score,
        latitude,
        longitude,

        ----------  booleans
        is_fraud,

        ----------  dates
        transaction_date,
        process_date

    from source

)

select * from renamed
