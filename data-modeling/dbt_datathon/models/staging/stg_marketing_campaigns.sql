with

source as (

    select * from {{ source('datathon_factored', 'marketing_campaigns') }}

),

renamed as (

    select

        ----------  ids
        _campaign_id as campaign_id,

        ----------  text
        campaign_name,
        description,
        campaign_type,
        campaign_objective,
        promoted_product,
        target_segment,
        target_country,
        campaign_status,

        ----------  numerics
        budget,
        expected_conversion_rate,

        ----------  dates
        start_date,
        end_date

    from source

)

select * from renamed
