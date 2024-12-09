-- Return if user identified by email is super user.
select
	count(*)
from
	access_users as au
where
	au.email = %(user_email)s
and
	au.enabled = true
and
	au.super = true
	;
