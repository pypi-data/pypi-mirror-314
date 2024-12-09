-- Update or insert group, returning id.
insert into access_groups
	(
		id
	  , name
	  , description
	  , enabled
	  , data
	  , updated_at
	  , created_at
	)
values
	(
	  %(id)s
	, %(name)s
	, %(description)s
	, %(enabled)s
	, %(data)s
	, now()
	, now()
	)
on
	conflict (id)
do
	update
set
	  name = %(name)s
	, description = %(description)s
	, enabled = %(enabled)s
	, data = %(data)s
	, updated_at = now()
returning id
;
