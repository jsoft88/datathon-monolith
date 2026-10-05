with

source as (

    select * from {{ source('datathon_factored', 'call_transcripts') }}

),

renamed as (

    select

        ----------  ids
        _transcript_id as transcript_id,
        interaction_id,
        customer_id,
        agent_id,

        ----------  text
        full_text,
        customer_text,
        agent_text,
        detected_language,
        detected_accent,
        detected_keywords,
        mentioned_entities,
        detected_intents,
        main_topics,
        transcription_model,
        audio_quality,

        ----------  numerics
        accent_confidence,
        duration_seconds,

        ----------  dates
        process_date

    from source

)

select * from renamed
