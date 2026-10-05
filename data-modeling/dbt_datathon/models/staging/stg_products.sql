with

source as (

    select * from {{ source('datathon_factored', 'products') }}

),

renamed as (

    select

        ----------  ids
        _product_id as product_id,
        customer_id,
        product_number,
        opening_branch_id,

        ----------  text
        product_type,
        currency,
        product_status,
        opening_channel,

        ----------  numerics
        current_balance,
        credit_limit,
        interest_rate,
        days_past_due,

        ----------  booleans
        has_linked_app,

        ----------  dates
        opening_date,
        expiration_date,
        last_transaction_date,
        last_updated

    from source

)

select * from renamed
