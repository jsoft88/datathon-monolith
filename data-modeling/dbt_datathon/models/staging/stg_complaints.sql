with

source as (

    select * from {{ source('datathon_factored', 'complaints') }}

),

renamed as (

    select

        ----------  ids
        _complaint_id as complaint_id,
        customer_id,
        affected_product_id,
        related_branch_id,
        origin_interaction_id,
        assigned_agent_id,

        ----------  text
        case_type,
        category,
        subcategory,
        reception_channel,
        description,
        currency,
        priority,
        status,
        resolution,

        ----------  numerics
        claimed_amount,
        resolution_days,
        compensation_granted,
        resolution_satisfaction,

        ----------  booleans
        sla_breached,
        is_repeat_complainer,

        ----------  dates
        creation_date,
        process_date,
        assignment_date,
        first_response_date,
        resolution_date,
        closing_date

    from source

)

select * from renamed
