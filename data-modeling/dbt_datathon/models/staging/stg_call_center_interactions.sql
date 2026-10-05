with

source as (

    select * from {{ source('datathon_factored', 'call_center_interactions') }}

),

renamed as (

    select

        ----------  ids
        _interaction_id as interaction_id,
        customer_id,
        agent_id,

        ----------  text
        interaction_type,
        channel,
        contact_reason,
        reason_category,
        detected_sentiment,
        customer_detected_accent,
        agent_used_accent,
        mentioned_products,

        ----------  numerics
        duration_seconds,
        wait_time_seconds,
        sentiment_score,

        ----------  booleans
        was_resolved,
        requires_followup,
        was_escalated,
        has_transcript,
        has_recording,

        ----------  dates
        interaction_date,
        process_date

    from source

)

select * from renamed
