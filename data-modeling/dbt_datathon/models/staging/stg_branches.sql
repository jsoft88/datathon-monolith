with

source as (

    select * from {{ source('datathon_factored', 'branches') }}

),

renamed as (

    select

        ----------  ids
        _branch_id as branch_id,
        branch_code,

        ----------  text
        branch_name,
        branch_type,
        address,
        city,
        state,
        country,
        postal_code,
        geographic_zone,
        phone,
        email,
        branch_status,

        ----------  numerics
        atm_count,
        teller_window_count,
        latitude,
        longitude,

        ----------  booleans
        has_atms,
        has_teller_windows,

        ----------  dates
        opening_time,
        closing_time,
        branch_opening_date

    from source

)

select * from renamed
