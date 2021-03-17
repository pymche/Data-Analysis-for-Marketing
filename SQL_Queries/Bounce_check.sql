SELECT lead.email, lead.first_name, lead.last_name, lead.campaigns, lead.lead_source, lead.lead_status, LEFT(lead.created_time, 10) AS CREATED_DATE, LEFT(lead.last_sent_time, 10) AS CREATED_TIME, lead.last_action_time, bounce.bounce_reason
FROM bounces bounce
INNER JOIN all_leads lead
ON lead.email = bounce.email;