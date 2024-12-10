-- Insert a new test access item into db
insert into test_access default values
	returning id
;
