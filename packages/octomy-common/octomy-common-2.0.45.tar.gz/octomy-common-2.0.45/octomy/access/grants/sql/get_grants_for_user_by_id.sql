-- Get grants for user by user_id.
select
	  gr.key
	, max(gr.created_at) as created_at
from
	access_grants as gr
inner join
	access_user_group_relations as ugr
on
	gr.group_id = ugr.group_id
where
	ugr.user_id = %(user_id)s
group by
	gr.key
order by
	gr.key desc
limit
	 %(limit)s
;
