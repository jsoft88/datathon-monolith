with

source as (

    select * from {{ source('datathon_factored', 'digital_events') }}

),

renamed as (

    select

        ----------  ids
        _event_id as event_id,
        customer_id,
        session_id,
        element_id,
        product_id,

        ----------  text
        event_type,
        event_category,
        channel,
        platform,
        browser,
        app_version,
        page_url,
        page_title,
        action,
        ip_address,
        ip_country,
        ip_city,
        referrer,
        utm_source,
        utm_medium,
        utm_campaign,

        ----------  numerics
        event_value,
        duration_seconds,

        ----------  booleans
        is_mobile,

        ----------  dates
        event_date,
        process_date

    from source

)

select * from renamed
