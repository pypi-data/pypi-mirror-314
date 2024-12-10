from fastapi import APIRouter, Depends, Request, HTTPException, status
from functools import lru_cache
from pydantic import BaseModel, StringConstraints
import pydantic.version
from typing import List, Optional, Annotated, Any, Dict
import datetime
import logging
import pprint
import uuid
import json


logger = logging.getLogger(__name__)
logger.info(f" # # # # # # PYDANTIC VERSION: {pydantic.version.version_info()}")


some_time = datetime.datetime(2024,1,1,0,0,0)


from pydantic import (
	PlainSerializer,
	TypeAdapter,
	WithJsonSchema,
)


JSONSerializableDict = Annotated[
	dict,
	PlainSerializer(lambda x: json.dumps(x) if isinstance(x, str) else x, return_type=str),
	WithJsonSchema({'type': 'string'}, mode='serialization'),
]


class NewPassword(BaseModel):
	new_password: str


class GeneralID(BaseModel):
	id: uuid.UUID


class UserGroupRelationStump(BaseModel):
	group_id: uuid.UUID
	user_id: uuid.UUID
	
	
class UserGroupRelation(UserGroupRelationStump):
	created_at: datetime.datetime
	
	
class UserStump(BaseModel):
	name: Annotated[str, StringConstraints(max_length=1023)] | None = None
	email: Annotated[str, StringConstraints(max_length=1023)] | None = None
	enabled: bool = False
	super: bool = False
	data: JSONSerializableDict | None = dict()


class User(UserStump):
	id: uuid.UUID
	updated_at:datetime.datetime
	password_changed_at:datetime.datetime | None = None
	login_at:datetime.datetime | None = None
	created_at: datetime.datetime | None = None


	def get_id(self, *args, **kvargs):
		do_debug = False
		if do_debug:
			logger.info(f"user.get_id args='{pprint.pformat(args)}', kvargs='{pprint.pformat(kvargs)}'")
		return id


	def can(self, *args, **kvargs):
		do_debug = False
		if do_debug:
			logger.info(f"user.can args='{pprint.pformat(args)}', kvargs='{pprint.pformat(kvargs)}'")
		return True


class UserDatabase(User):
	password_hash: Annotated[str, StringConstraints(max_length=1023)]


class GroupStump(BaseModel):
	name: Annotated[str, StringConstraints(max_length=1023)] | None
	description: str | None = None
	enabled: bool = False
	data: JSONSerializableDict | None = dict()


class Group(GroupStump):
	id: uuid.UUID
	created_at: datetime.datetime
	updated_at:datetime.datetime


class GrantType(BaseModel):
	key: Annotated[str, StringConstraints(max_length=1023)]
	description: Annotated[str, StringConstraints(max_length=1023)]


class GrantStump(BaseModel):
	key: str
	#key: Annotated[str, StringConstraints(max_length=1023)]


class Grant(GrantStump):
	group_id: uuid.UUID
	created_at: datetime.datetime | None


class UserGrant(BaseModel):
	key: str
	created_at: datetime.datetime | None


@lru_cache()
def get_dummy_user() -> User:
	return User(
		  id="69696969-6969-6969-6969-696969696969"
		, name="Dummy User"
		, email="dummy@example.com"
		, password_hash="dlghjlkszdfjglkdfjglkdfjglkjdfgkljdfgkljsdfgjhayhiyhpiosdvkældfmgjklhwerfuwopdlf"
		, enabled=True
		, super=True
		, data={"data":"lol"}
		, created_at=some_time
		, password_changed_at=some_time
		, login_at=some_time
		, updated_at=some_time
	)

@lru_cache()
def get_current_user() -> User:
	current_user = get_dummy_user()
	return current_user


class AccessContext(BaseModel):
	current_user: User | None
	status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
	status_message:str = "Unknown"

	def get_id(self, *args, **kvargs):
		do_debug = False
		if do_debug:
			logger.info(f"AccessContext.get_id args='{pprint.pformat(args)}', kvargs='{pprint.pformat(kvargs)}'")
		if self.current_user:
			return self.current_user.get_id()
		return None

	def can(self, *args, **kvargs):
		do_debug = False
		if do_debug:
			logger.info(f"AccessContext.can args='{pprint.pformat(args)}', kvargs='{pprint.pformat(kvargs)}'")
		if self.current_user:
			return self.current_user.can(*args, **kvargs)
		return False


#@lru_cache()
def dummy_access_context(required_scopes: List[str] | None) -> AccessContext | None:
	return AccessContext(current_user = get_dummy_user(), status_code=status.HTTP_200_OK, status_message="OK")


def get_access_context(required_scopes: Optional[List[str]] = None) -> AccessContext | None:
	user:User = get_current_user()
	if not user:
		return AccessContext(current_user=None, status_code=status.HTTP_401_UNAUTHORIZED, status_message="Not authenticated")
	user_scopes = ["overwatch.access.profile.view"]  # Dummy scopes
	if not set(required_scopes or list()).issubset(set(user_scopes)):
		return AccessContext(current_user=user, status_code=status.HTTP_403_FORBIDDEN, status_message="Insufficient privileges")
	return AccessContext(current_user=user, status_code=status.HTTP_200_OK, status_message="OK")


async def access_context_dependency(required_scopes: Optional[List[str]] = None) -> AccessContext | None:
	#return dummy_access_context(required_scopes)
	async def annotated():
		return get_access_context(required_scopes)
	return annotated


def is_safe_url(request, target):
	ref_url = urlparse(request.host_url)
	test_url = urlparse(urljoin(request.host_url, target))
	return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


'''



def verify_access_email(email, grant_keys, match_all=True):
	ret = False
	if email:
		db = get_access_db(current_app.config)
		if db.user_is_super(email) > 0:
			ret = True
		else:
			num = db.user_can(email, tuple(grant_keys))
			total = len(grant_keys)
			if match_all:
				# All must match
				if num == total:
					ret = True
			else:
				# At least one must match
				if num > 0:
					ret = True
	return ret


def verify_access_user(user, grant_keys, match_all=True):
	if user:
		return verify_access_email(user.id, grant_keys, match_all)
	return False


def verify_access(grant_keys, match_all=True):
	user = flask_login.current_user
	return verify_access_user(user, grant_keys, match_all)




##################


from functools import wraps

from flask import session, redirect, url_for, request, current_app

from ..common import abortj

from fk.api.access import FlaskLoginUser, flask_login_manager, verify_access, verify_access_user, verify_access_email
from fk.api.access.db import get_access_db

import flask_login
from urllib.parse import urlparse, urljoin


import pprint
import logging

logger = logging.getLogger(__name__)

overwatch_auth = flask_login_manager


overwatch_login_required = flask_login.login_required


def overwatch_login_required_old(func):
    # logger.info("overwatch_login_required")

    @flask_login.login_required
    def wrapper(*args, **kwargs):
        # logger.info("overwatch_login_required.wrapper")
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


def overwatch_verify_access(grant_keys, match_all=True, do_debug=False):
    def decorator(f):
        # logger.info("overwatch_verify_access.decorator")

        @wraps(f)
        def wrapper(*args, **kwargs):
            user = flask_login.current_user
            if verify_access_user(user, grant_keys, match_all):
                if do_debug:
                    logger.info(f"overwatch_verify_access access granted; Needed {'all' if match_all else 'any'} of [{','.join(grant_keys)}]")
                return f(*args, **kwargs)
            if do_debug:
                logger.warning(f"overwatch_verify_access access blocked; Needed {'all' if match_all else 'any'} of [{','.join(grant_keys)}], coming from {request.referrer}")
            url = request.headers.get("Referer")
            if not url:
                url = url_for("access_bp.hall", next=request.args.get("next"))
            return redirect(url)

        return wrapper

    return decorator


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


##########################################################################


@flask_login_manager.unauthorized_handler
def unauthorized_handler():
    # logger.info("unauthorized_handler")
    return redirect(url_for("access_bp.login", next=request.args.get("next")))


@flask_login_manager.user_loader
def user_loader(email):
    user = None
    if email:
        authenticate = False
        db = get_access_db(current_app.config)
        db_user = db.get_user_by_email(email)
        if db_user:
            # logger.info(f"FOUND USER IN DB")
            authenticate = True
        if authenticate:
            user = FlaskLoginUser()
            user.id = email
    # logger.info(f"user_loader for {email} returns {user}")
    return user


@flask_login_manager.request_loader
def request_loader(request):
    email = request.form.get("email")
    user = user_loader(email)
    # logger.info(f"request_loader for {email} returns {user}")
    return user







# BASIC



from functools import wraps

from flask import session, redirect, url_for, request, current_app

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from ..common import abortj

from fk.api.access.db import get_access_db

import pprint
import logging

logger = logging.getLogger(__name__)


overwatch_auth = HTTPBasicAuth()

users_cache = {}


def get_users():
    if not users_cache:
        users_cache = {current_app.config.get("overwatch-user", "no-user"): current_app.config.get("overwatch-password", None)}
        db = get_access_db(current_app.config)
        db_users = db.get_users()
        for user in db_users:
            username = user.get("email")
            password = user.get("password")
            users_cache[username] = password

    return users_cache


def overwatch_login_required(func):
    @overwatch_auth.login_required
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@overwatch_auth.verify_password
def verify_password_basic(username, password):
    users = {current_app.config.get("overwatch-user", "no-user"): current_app.config.get("overwatch-password", None)}
    if username in users and users.get(username, None):
        ret = check_password_hash(generate_password_hash(users.get(username)), password)
        if not ret:
            logger.warning(f"Overwatch verify auth failed")
        return ret
    return False


@overwatch_auth.verify_password
def verify_password(username, password):
    users = get_users()
    if username in users and users.get(username, None):
        ret = check_password_hash(generate_password_hash(users.get(username)), password)
        if not ret:
            logger.warning(f"Overwatch verify auth failed")
            return ret
        return False


def verify_access_worker(username, grant_keys, match_all=True):
    ret = False
    db = get_access_db(current_app.config)
    num = db.user_can(username, tuple(grant_keys))
    total = len(grant_keys)
    if match_all:
        # All must match
        if num == total:
            ret = True
    else:
        # At least one must match
        if num > 0:
            ret = True
    if not ret:
        logger.warning(f"Overwatch verify access failed with {num} of {total} matched, and match_all={match_all}")
    return ret


def overwatch_verify_access(grant_keys, match_all=True):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            username = overwatch_auth.current_user()
            logger.info(f"overwatch_verify_access(username={username}, grant_keys={pprint.pformat(grant_keys)}, match_all={match_all})")
            if not verify_access_worker(username, grant_keys, match_all):
                logger.warning(f"overwatch_verify_access block access. Need {'all' if match_all else 'any'} of {pprint.pformat(grant_keys)}")
                abortj(401, "Access not granted")
            return f(*args, **kwargs)

        return wrapper

    return decorator


##########################################################################


@login_manager.unauthorized_handler
def unauthorized_handler():
    return "Unauthorized Biaaach"


'''
