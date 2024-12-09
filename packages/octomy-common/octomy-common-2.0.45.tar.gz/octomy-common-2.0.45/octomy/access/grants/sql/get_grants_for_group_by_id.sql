-- Get grants for group by group_id.
select
	  gr.key
	, gr.group_id
	, gr.created_at
from
	access_grants as gr
where
	gr.group_id = %(group_id)s
order by
	gr.created_at desc
limit
	%(limit)s
;
