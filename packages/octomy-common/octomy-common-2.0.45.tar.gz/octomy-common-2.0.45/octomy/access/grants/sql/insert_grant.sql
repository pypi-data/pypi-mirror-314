-- Insert or ignore grant.
insert into access_grants
	(
		group_id
	  , key
	  , created_at
	)
values
	(
	  %(group_id)s
	, %(key)s
	, now()
	)
on
	conflict
do
	nothing
;
