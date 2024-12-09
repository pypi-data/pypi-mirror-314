-- Return the number of users where given email and passowrd_hash match.
select
	count(id)
from
	access_users
where
	email = %(email)s
and
	password_hash = crypt(%(password)s, password_hash)
;
