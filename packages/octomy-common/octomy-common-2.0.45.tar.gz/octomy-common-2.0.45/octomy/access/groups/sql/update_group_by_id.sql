-- Update group by id, returning id.
update access_groups
set
	  name = %(name)s
	, description = %(description)s
	, enabled = %(enabled)s
	, data = %(data)s
	, updated_at = now()
where
	id = %(id)s
returning
	id
;

