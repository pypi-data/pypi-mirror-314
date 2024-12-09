-- Insert group, returning id.
insert into access_groups
	(
		name
	  , description
	  , enabled
	  , data
	  , updated_at
	  , created_at
	)
values
	(
	  %(name)s
	, %(description)s
	, %(enabled)s
	, %(data)s
	, now()
	, now()
	)
returning id
;
