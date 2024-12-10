from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse
from octomy.web.context import Context, get_context, context_dependency
from typing import List, Optional, Annotated
import jinja2.exceptions
import json
import logging
import pprint
import datetime
from fastapi.templating import Jinja2Templates


logger = logging.getLogger(__name__)


def prepare_templates():
	try:
		context = get_context()
		templates = Jinja2Templates(directory=f"{context.webroot}")
		templates.env.globals['datetime'] = datetime
		templates.env.globals['context'] = get_context()
		return  templates
	except Exception as e:
		logger.exception("No templates folder found, skipping...")
	return None

templates = prepare_templates()
 
def abortj(status_code, detail):
	content = {"status_code":status_code, "detail":detail}
	response = JSONResponse(status_code=status_code, content=content)
	logger.error("abortj")
	logger.warning(content)
	return response

json_content_type = "application/json"
html_content_type = "text/html"

FALLBACK_LIMIT = 100


def get_content_type(request):
	content_type = request.headers.get("content-type", None)
	if not content_type:
		return True
	if content_type == json_content_type:
		return "json"
	if content_type == html_content_type:
		return "html"
	else:
		raise HTTPException(
			status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
			detail = f"Unsupported content type {content_type}")
	return False

def expect_json(request):
	content_type = request.headers.get("content-type", None)
	if not content_type:
		return True
	if content_type == json_content_type:
		return True
	else:
		raise HTTPException(
			status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
			detail = f"Unsupported content type {content_type}")
	return False

def expect_html(request):
	content_type = request.headers.get("content-type", None)
	if not content_type:
		return True
	if content_type == html_content_type:
		return True
	else:
		raise HTTPException(
			status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
			detail = f"Unsupported content type {content_type}")
	return False

async def db_get(request, context, query_key, params = dict(), mode="none", item_type = dict | None, prepare=True, do_debug=False):
	if do_debug:
		logger.info(f"db_get(request={request}, context={context}, query_key={query_key}, item_type={item_type})")
		logger.warning(f"PARAMS: {params}")
	params["limit"] = context.config.get("app-db-fetch-limit", FALLBACK_LIMIT)
	db_items, db_err = await context.db.key_query(query_key=query_key, params=params, mode=mode, item_type=item_type, prepare=prepare)
	#if None == db_items and mode != "none":
	#	raise Exception(db_err or f"No items found for '{query_key}'")
	return db_items, db_err

async def db_json(request, context, query_key, params = dict(), mode="none", item_type = dict | None, prepare=True, do_debug=False):
	if do_debug:
		logger.info(f"db_json(request={request}, context={context}, query_key={query_key}, item_type={item_type})")
	expect_json(request)
	return await db_get(request = request, context = context, query_key = query_key, params = params, mode=mode, item_type = item_type, prepare=prepare, do_debug = do_debug)


def handled_template(template_path, template_params):
	try:
		return templates.TemplateResponse(template_path, template_params)
	except Exception as e:
		if isinstance(e, jinja2.exceptions.TemplateError):
			logger.error("")
			logger.error(f"Template error: {type(e).__name__}: {e.message}")
			logger.error("")
			logger.warning(f"  for {template_path}")
			logger.warning("")
			logger.warning(f" with {pprint.pformat(template_params)}")
			logger.warning("")
			raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Template error")
		else:
			raise e

