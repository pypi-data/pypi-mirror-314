import logging
import base64

oktopus_folder_name = '.oktopus'
oktopus_version = '0.0.15'

logger = logging.getLogger(__name__)

def file_properties(id, key):
	properties = {
		  'oktopus_source_id': id
		, 'oktopus_parameter_key': key
		, 'oktopus_version': oktopus_version
	}
	return properties


from octomy.cad.generators.ntop import nTopGenerator
from octomy.cad.generators.openscad import OpenSCADGenerator
from octomy.cad.types import *
from octomy.storage.google_drive import GoogleDrive, FOLDER_MIMETYPE, folder_id as google_drive_folder_id


class GeneratorTool:
	def __init__(self, storage, oktopus_folder_name):
		self.oktopus_folder_id = None
		self.storage = storage
		self.oktopus_folder_name = oktopus_folder_name
		self.ensure_oktopus_folder()

	def find_oktopus_folder(self):
		self.oktopus_folder_id = None
		q = f"'{google_drive_folder_id}' in parents and name = '{self.oktopus_folder_name}' and trashed = false and mimeType = '{FOLDER_MIMETYPE}'"
		folders = self.storage.search_files(q = q)
		if folders and len(folders) >= 0:
			self.oktopus_folder_id = folders[0].get("id")
		return self.oktopus_folder_id

	def ensure_oktopus_folder(self):
		#logger.info("ENSURE DERIVATIVES")
		self.oktopus_folder_id = self.find_oktopus_folder()
		if not self.oktopus_folder_id:
			ret = self.storage.create_folder(file_metadata={"name":self.oktopus_folder_name, "parents":[google_drive_folder_id]})
			if ret:
				#logger.info(f"ret:{pprint.pformat(ret)}")
				self.oktopus_folder_id = ret
		return self.oktopus_folder_id

	def find_source_folder(self, name):
		q = f"'{self.oktopus_folder_id}' in parents and name = '{name}' and trashed = false and mimeType = '{FOLDER_MIMETYPE}'"
		source_folder_id = None
		folders = self.storage.search_files(q = q)
		if folders and len(folders) >= 0:
			source_folder_id = folders[0].get("id")
		return source_folder_id
		
	def ensure_source_folder(self, name):
		source_folder_id = self.find_source_folder(name)
		if not source_folder_id:
			ret = self.storage.create_folder(file_metadata={"name":name, "parents":[self.oktopus_folder_id]})
			if ret:
				#logger.info(f"ret:{pprint.pformat(ret)}")
				source_folder_id = ret
		return source_folder_id
	
	def find_part_folder(self, source_folder_id, name):
		q = f"'{source_folder_id}' in parents and name = '{name}' and trashed = false and mimeType = '{FOLDER_MIMETYPE}'"
		part_folder_id = None
		folders = self.storage.search_files(q = q)
		if folders and len(folders) >= 0:
			part_folder_id = folders[0].get("id")
		return part_folder_id
		
	def ensure_part_folder(self, source_folder_id, name):
		part_folder_id = self.find_part_folder(source_folder_id, name)
		if not part_folder_id:
			ret = self.storage.create_folder(file_metadata={"name":name, "parents":[source_folder_id]})
			if ret:
				#logger.info(f"ret:{pprint.pformat(ret)}")
				part_folder_id = ret
		return part_folder_id



	def upload_derivative(self, local_path, parent_id, name, mimetype, properties = dict(), do_debug = False):
		if do_debug:
			logger.info(f"Uploading file '{local_path}'")
			logger.info(f"  of type '{mimetype}'")
			logger.info(f"  with properties '{pprint.pformat(properties)}'")
			logger.info(f"  to drive at '{parent_id}/{name}'")
		file_metadata = {"parents":[parent_id], "name": name }
		if properties:
			file_metadata["properties"] = properties
		file_id = self.storage.upload_file(
			  file_path = local_path
			, file_metadata = file_metadata
			, mimetype = mimetype)
		#logger.info("UPLOADED '{local_path}' to '{name}' gave ID '{file_id}'")
		return file_id

	def set_drive_thumbnail_from_data(self, file_id, data, do_debug = True):
		if do_debug:
			logger.info(f"Setting thumbnail of {file_id} to raw data ({len(data)} bytes)")
		if not file_id:
			logger.warning("No id")
			return
		metadata = {
			"contentHints": {
				"thumbnail": {
					"image": base64.urlsafe_b64encode(data).decode('utf8'),
					"mimeType": MIMETYPE_PNG_IMAGE,
				}
			}
		}
		res = self.storage.update_file_metadata(file_id, metadata)


	def set_drive_thumbnail_from_local_path(self, file_id, thumbnail_path, do_debug = True):
		if do_debug:
			logger.info(f"Setting thumbnail of {file_id} to content of '{thumbnail_path}")
		if not file_id:
			logger.warning("No id")
			return
		with open(thumbnail_path, "rb") as f:
			return self.set_drive_thumbnail_from_data(file_id, f.read(), do_debug = do_debug)


storage = GoogleDrive()
common = GeneratorTool(storage = storage, oktopus_folder_name = google_drive_folder_id)

generators_map = {
	GeneratorTypeEnum.openscad: OpenSCADGenerator(common = common)
	, GeneratorTypeEnum.ntop: nTopGenerator(common = common)
}
