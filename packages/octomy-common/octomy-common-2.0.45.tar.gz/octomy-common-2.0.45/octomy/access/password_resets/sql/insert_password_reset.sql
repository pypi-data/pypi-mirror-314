-- Insert password_reset given user_id and time_limit_sec returning token.
insert into access_password_resets
	(
		user_id
	  , token
	  , time_limit
	  , created_at
	)
values
	(
	  %(user_id)s
	, encode(gen_random_bytes(20),'base64')
	, (%(time_limit_sec)s || ' second')::interval
	, now()
	)
returning token
;
