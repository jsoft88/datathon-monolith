with

source as (

    select * from {{ source('datathon_factored', 'campaign_sends') }}

),

renamed as (

    select

        ----------  ids
        _send_id as send_id,
        campaign_id,
        customer_id,

        ----------  text
        send_channel,
        template_used,
        subject,
        send_status,
        open_device,
        open_country,
        failure_reason,

        ----------  numerics
        click_count,
        conversion_value,
        send_cost,

        ----------  booleans
        was_delivered,
        was_opened,
        was_clicked,
        had_conversion,

        ----------  dates
        send_date,
        process_date,
        open_date,
        click_date,
        conversion_date

    from source

)

select * from renamed
