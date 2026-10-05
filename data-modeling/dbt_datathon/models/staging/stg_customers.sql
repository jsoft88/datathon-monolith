with

source as (

    select * from {{ source('datathon_factored', 'customers') }}

),

renamed as (

    select

        ----------  ids
        _customer_id as customer_id,
        document_number,
        registration_branch_id,

        ----------  text
        document_type,
        first_name,
        last_name,
        gender,
        email,
        mobile_phone,
        landline_phone,
        address,
        city,
        state,
        country,
        postal_code,
        detected_accent,
        segment,
        occupation,
        marital_status,
        education_level,
        customer_status,

        ----------  numerics
        credit_score,
        estimated_monthly_income,

        ----------  booleans
        accepts_marketing,

        ----------  dates
        date_of_birth,
        registration_date,
        last_updated

    from source

)

select * from renamed
