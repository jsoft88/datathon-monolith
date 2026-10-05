with

source as (

    select * from {{ source('datathon_factored', 'satisfaction_surveys') }}

),

renamed as (

    select

        ----------  ids
        _survey_id as survey_id,
        interaction_id,
        customer_id,
        agent_id,

        ----------  text
        survey_type,
        send_channel,
        nps_category,
        question_1_text,
        question_2_text,
        question_3_text,
        open_comments,
        comment_sentiment,

        ----------  numerics
        main_score,
        question_1_response,
        question_2_response,
        question_3_response,
        response_time_hours,
        campaign_response_rate,

        ----------  dates
        survey_date,
        process_date

    from source

)

select * from renamed
