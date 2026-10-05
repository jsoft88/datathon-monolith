with

source as (

    select * from {{ source('datathon_factored', 'service_agents') }}

),

renamed as (

    select

        ----------  ids
        _agent_id as agent_id,
        employee_code,
        assigned_branch_id,

        ----------  text
        first_name,
        last_name,
        email,
        phone,
        native_accent,
        country_of_origin,
        agent_type,
        experience_level,
        languages,
        specialty,
        agent_status,
        work_shift,

        ----------  numerics
        avg_csat,
        total_monthly_interactions,

        ----------  dates
        hire_date

    from source

)

select * from renamed
