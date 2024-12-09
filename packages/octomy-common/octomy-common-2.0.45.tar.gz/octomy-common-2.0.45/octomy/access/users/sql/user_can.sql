-- Return number of grants matching user identified by email.
select
	count(*)
from
	access_grants as agr
inner join
	access_user_group_relations as augr
on
	agr.group_id = augr.group_id
inner join
	access_users as au
on
	au.id = augr.user_id
inner join
	access_groups as ag
on
	ag.id = augr.group_id
where
	au.email = %(user_email)s
and
	au.enabled = true
and
	ag.enabled = true
and
	au.password_hash is not null
and
	agr.key in %(keys)s
	;
