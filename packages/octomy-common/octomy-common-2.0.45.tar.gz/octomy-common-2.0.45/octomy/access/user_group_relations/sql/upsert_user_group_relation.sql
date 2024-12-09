--  Insert or ignore user group relation given user_id and group_id
insert into access_user_group_relations
	(
	  group_id
	, user_id
	, created_at
	)
values
	(
	  %(group_id)s
	, %(user_id)s
	, now()
	)
on
	conflict
do
	nothing
;
