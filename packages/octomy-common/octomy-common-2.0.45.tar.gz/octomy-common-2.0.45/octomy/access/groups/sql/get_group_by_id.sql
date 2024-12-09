-- Return group by id.
select
	  id
	, name
	, description
	, enabled
	, data
	, updated_at
	, created_at
from
	access_groups
where
	id = %(id)s
limit 1
;
