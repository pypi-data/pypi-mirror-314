from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
import datetime
import frontmatter
import jinja2
import logging
import markdown
import os
import pprint
import traceback


logger = logging.getLogger(__name__)


def gen_tags(parts):
	tags = ["-".join(parts[:-1])] + [part for part in parts]
	# logger.info(f"TAGS: {pprint.pformat(parts)} --> {tags}")
	return  tags

def url_for(index):
	return "http://TODO_MAKE_URLFOR/"+str(index)

class AutoRouter:

	exts = ['html', 'md']
	#md_extensions = ['tables', 'md_in_html', 'footnotes', 'fenced_code', 'def_list', 'attr_list', 'abbr', 'toc', 'smarty']
	md_extensions = ['tables', 'md_in_html', 'footnotes', 'fenced_code', 'def_list', 'abbr', 'toc', ]

	def __init__(self, app, context):
		self.app = app
		self.context = context
		self.env = self.prepare_env()
		self.auto_routes = {}
		self.auto_route_all(self.context.webroot)
		#logger.info(f"ROUTES: {pprint.PrettyPrinter(indent=4, compact=False).pformat(self.auto_routes)}")


	def prepare_env(self):
		loader = jinja2.ChoiceLoader(
			[
				jinja2.FileSystemLoader(self.context.webroot)
	#			, jinja2.FileSystemLoader(os.path.join(project_folder, os.path.dirname(template_name)))
			]
		)
		env = jinja2.Environment(loader=loader)
		env.globals['datetime'] = datetime
		env.globals['context'] = self.context
#		env.globals['current_user'] = user
#		env.globals['current_user_can'] = current_user_can
#		env.globals['url_for'] = url_for
		#env.globals.update(get_expiry=octomy.utils.expiry_cache.get_expiry)
		#env.filters['myfilter'] = filter
		return env


	def _subpages(self, path, max_level=2):
		out = {}
		#space = max_level * "   "
		parts = os.path.normpath(path).strip(os.path.sep).split(os.path.sep) 
		path = "/".join(parts)
		obj = self.auto_routes.get(path, dict())
		if max_level > 1:
			out[path] = obj
			if obj:
				subs = obj.get("children", list())
				for sub in subs:
					subsubs = self._subpages(sub, max_level - 1)
					for subsub in subsubs:
						if subsub not in out:
							subobj = self.auto_routes.get(subsub, dict())
							if subobj:
								out[subsub] = subobj
		return out



	def _perform_markdown(self, template_string):
		template_string = markdown.markdown(template_string, extensions = self.md_extensions)
		return template_string
	
	def _perform_frontmatter(self, template_string):
		page = frontmatter.loads(template_string)
		logger.info(f"FRONTMATTER:{dict(page)}")
		return page.content, dict(page)
		

	def _perform_jinja_string(self, template_string, data=dict()):
		template = self.env.from_string(template_string)
		if not template:
			return None, f"Error creating template for '{template_fn}'"
		#logger.info(f"template_fn:{template_fn}")
		html = template.render(title="TODO: Set title from context", **data)
		return html, None

	def _perform_jinja_file(self, template_fn, data=dict()):
		template_string = ""
		if not os.path.isabs(template_fn):
			template_fn = os.path.join(self.context.webroot, template_fn)
		# logger.info(f"AMENDED PATH:{template_fn}")
		with open(template_fn, "r") as template_file:
			template_string = template_file.read()
		return self._perform_jinja_string(template_string, data=data)

	def _perform_wrapping(self, template_string:str, data:dict = dict(), pre_wrappers:list = list(), post_wrappers:list = list()):
		out = ""
		for wrapper in pre_wrappers:
			content, error = self._perform_jinja_file(template_fn = wrapper, data = data)
			if error:
				logger.warning(f"Error appending pre wrapper '{wrapper}', skipping: {error}")
			else:
				out += content
		out += template_string
		for wrapper in post_wrappers:
			content, error = self._perform_jinja_file(template_fn = wrapper, data = data)
			if error:
				logger.warning(f"Error appending post wrapper '{wrapper}', skipping: {error}")
			else:
				out += content
		return out

	def _find_index(self, path):
		template_fn = None
		type = None
		for ext in self.exts:
			candidate = f"{self.context.webroot}/{path}/index.{ext}"
			if os.path.isfile(candidate):
				template_fn = candidate;
				type = ext
				break
		return template_fn, type

	def _get_path_parts(self, path):
		parts = os.path.normpath(path).strip(os.path.sep).split(os.path.sep) 
		return parts

	def handler_raw(self, path, request):
		try:
			template_fn, type = self._find_index(path)
			if not template_fn:
				return None, f"No index file found for {path}"
			template_string = ""
			parts = self._get_path_parts(path)
			subs = self._subpages(path, 4)
			logger.info(f"Reading template {template_fn}:")
			with open(template_fn, "r") as template_file:
				template_string = template_file.read()
			template_string, frontmatter = self._perform_frontmatter(template_string)
			if 'md' == type:
				template_string = self._perform_markdown(template_string)
			data = {
				  'type': type
				, 'subpages': subs
				, 'request': request
				, 'frontmatter': frontmatter
				, 'context': self.context
			}
			if frontmatter:
				pre_wrappers = frontmatter.get('pre_wrappers', list())
				post_wrappers = frontmatter.get('post_wrappers', list())
				template_string = self._perform_wrapping(template_string, data = data, pre_wrappers = pre_wrappers, post_wrappers = post_wrappers)
			html, err = self._perform_jinja_string(template_string, data)
			return html, err
		except Exception as e:
			logger.exception(f"Could not handle {path}")
			return None, f"Error rendering template '{template_fn}' with error\n{traceback.format_exc()}"


	def auto_route_all(self, base):
		for ext in self.exts:
			for path in Path(base).rglob(f'index.{ext}'):
				self.auto_route_path(path)
	

	def auto_route_path(self, template_fn):
		dir = Path(os.path.relpath(os.path.dirname(template_fn), self.context.webroot))
		self.auto_routes[str(dir)] = { "children":[], "path": str(dir), "title": os.path.basename(str(dir)).capitalize() }
		name = os.path.basename(dir)
		#logger.info(f"GOT ROUTE{pprint.pformat(dir.parts)} {name}")
		self.app.add_api_route(path=f"/{dir}", endpoint=self.handler, methods=["GET"], tags=gen_tags(dir.parts), name=name, response_class=HTMLResponse)
		acc = []
		for part in dir.parts:
			key = "/".join(acc)
			node = self.auto_routes.get(key, dict())
			children = node.get("children", list())
			childkey = f"{key}/{part}"
			if childkey not in children:
				children.append(childkey)
			node["children"] = children
			node["path"] = str(key)
			node["title"] = os.path.basename(str(key)).capitalize()
			self.auto_routes[key] = node
			#index_page(str(key))
			acc.append(part)
		return {"dir":dir, "name":name, }
	

	def _generr(self, err):
		return f"""
		<h1>An error occurred</h1>
		<pre>
		{err}
		</pre>
		"""
	def handler(self, request:Request):
		path = request.scope['route'].path
		logger.info(f"GOT HANDLER{pprint.pformat(path)}, {pprint.pformat(request.path_params)} {request.url.path}")
		res, err = self.handler_raw(path, request)
		if err:
			#return HTTPException(status_code=500, detail=err)
			return HTMLResponse(content=self._generr(err), status_code=200)
		return HTMLResponse(content=res, status_code=200)
