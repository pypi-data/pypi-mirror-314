from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
import google.auth
import googleapiclient.discovery
import googleapiclient.errors
import io
import json
import logging
import os
import pprint
import requests
import socket


logger = logging.getLogger(__name__)

timeout_in_sec = 3
socket.setdefaulttimeout(timeout_in_sec)

folder_id = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
#google_username = "oktopus-development@oktopus-397222.iam.gserviceaccount.com"

FOLDER_MIMETYPE = "application/vnd.google-apps.folder"


class GoogleDrive:
	default_mimetype = 'application/octet-stream'

	def __init__(self, credentials_file_path = None):
		self.common_paramters = {
			"supportsAllDrives": True
		}
		self.search_paramters = {
			  "includeItemsFromAllDrives": True
			, "corpora": 'allDrives'
		}
		logger.info(f"GOOGLE_APPLICATION_CREDENTIALS: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'not present')}")
		logger.info(f"GOOGLE_DRIVE_FOLDER_ID: {os.environ.get('GOOGLE_DRIVE_FOLDER_ID', 'not present')}")
		"""
		Load pre-authorized user credentials from the environment.
		TODO(developer) - See https://developers.google.com/identity
		for guides on implementing OAuth2 for the application.
		"""
		creds = None
		project_id = None
		if credentials_file_path:
			logger.info(f"Cred file specified, loading creds from there")
			drive_scopes = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
			creds = service_account.Credentials.from_service_account_file(
										  filename = credentials_file_path, 
										  scopes = drive_scopes)
			"""
			with open(credentials_file_path, 'r') as credentials_file:
				credentials_data = json.load(credentials_file)
				logger.info(f"DATA:")
				logger.info(pprint.pformat(credentials_data))
				creds = google.auth.credentials.Credentials.from_service_account_info(credentials_data)
			"""
			project_id = creds.project_id
		else:
			logger.info(f"Cred file not specified, loading creds from environment")
			creds, project_id = google.auth.default()
		
		logger.info(f"creds='{pprint.pformat(creds)}', project_id='{pprint.pformat(project_id)}'")
		# create drive api client
		self.creds = creds
		self.service = googleapiclient.discovery.build('drive', 'v3', credentials = self.creds)
		logger.info('Initialized google drive api')
		#raise Exception("gd here")

	def search_files(self, q, fields=list(), do_debug = False):
		"""Search file in drive location
		"""
		fields.append('id')
		fields.append('name')
		fields = list(set(fields))
		files = []
		page_token = None
		if do_debug:
			logger.info(f" ## Searching for files with query=\"{q}\" and fields=[ {', '.join(fields)} ] on google drive")
		try:
			while True:
				# pylint: disable=maybe-no-member
				response = self.service.files().list(q = q,
												spaces = 'drive',
												fields = 'nextPageToken, '
													   f'files({",".join(fields)})',
												pageToken = page_token,
												**self.common_paramters,
												**self.search_paramters
												).execute()
				#for file in response.get('files', list()):
					# Process change
					#logger.info(F'Found file: {file.get("name")}, {file.get("id")}')
				files.extend(response.get('files', list()))
				page_token = response.get('nextPageToken', None)
				if page_token is None:
					break
	
		except googleapiclient.errors.HttpError as error:
			logger.error(f'An error occurred: {error}')
			files = None
	
		return files

	def recursive_search_worker(self, folder_id, q_files, q_folders, fields=list(), path=list(), exclude_dot_files = True, exclude_dot_folders = True, do_debug = False):
		"""Search files and folders in drive location (one recursive step)
		"""
		path = path or list()
		fields.append('id')
		fields.append('name')
		fields = list(set(fields))
		files = list()
		folders = list()
		
		sub_q_files =   f"'{folder_id}' in parents and mimeType != '{FOLDER_MIMETYPE}' and {q_files}"
		sub_q_folders = f"'{folder_id}' in parents and mimeType =  '{FOLDER_MIMETYPE}' and {q_folders}"
		# https://developers.google.com/drive/api/guides/ref-search-terms#operators
		
		if do_debug:
			logger.info(f" ## Searching recursively for files and folders under {folder_id}")
			logger.info(f"    q_files=\"{q_files}\"")
			logger.info(f"    q_folders=\"{q_folders}\"")
			logger.info(f"    sub_q_files=\"{sub_q_files}\"")
			logger.info(f"    sub_q_folders=\"{sub_q_folders}\"")
			logger.info(f"    fields=[ {', '.join(fields)} ] ")
			logger.info(f"    on google drive")
		try:
			page_token = None
			while True:
				# pylint: disable=maybe-no-member
				response = self.service.files().list(q = sub_q_files,
												spaces = 'drive',
												fields = 'nextPageToken, '
													   f'files({",".join(fields)})',
												pageToken = page_token,
												**self.common_paramters,
												**self.search_paramters
												).execute()
				ret = response.get('files')
				if ret: 
					for file in ret:
						if exclude_dot_files and file.get("name").startswith("."):
							continue
						files.append(file)
				page_token = response.get('nextPageToken', None)
				if page_token is None:
					break
			for file in files:
				file["path"] = path
			page_token = None
			while True:
				# pylint: disable=maybe-no-member
				response = self.service.files().list(q = sub_q_folders,
												spaces = 'drive',
												fields = 'nextPageToken, '
													   f'files({",".join(fields)})',
												pageToken = page_token,
												**self.common_paramters,
												**self.search_paramters
												).execute()
				ret = response.get('files')
				if ret:
					if do_debug:
						logger.info(f"Extending folders {pprint.pformat(folders)} with ret {pprint.pformat(ret)}")
					for folder in ret:
						if exclude_dot_folders and folder.get("name").startswith("."):
							continue
						folders.append(folder)
					if do_debug:
						logger.info(f"To {pprint.pformat(folders)}")
				page_token = response.get('nextPageToken', None)
				if page_token is None:
					break
			recurse_folders = folders.copy()
			for folder in recurse_folders:
				if not folder:
					continue
				if do_debug:
					logger.info(f"RECURSING FOLDER: {pprint.pformat(folder)}, ({pprint.pformat(recurse_folders)})")
				sub_folder_id = folder.get("id")
				sub_path = path.copy()
				sub_path.append(folder)
				sub_files, sub_folders = self.recursive_search_worker(sub_folder_id, q_files, q_folders, fields=fields, path = sub_path, do_debug = do_debug)
				files.extend(sub_files)
				folders.extend(sub_folders)
	
		except googleapiclient.errors.HttpError as error:
			logger.error(f'An error occurred: {error}')
			files = list()
			folders = list()
	
		return files, folders
		

	def download_file(self, file_id, do_debug = False):
		"""Download a file
		Args:
			real_file_id - ID of the file to download
		Returns : IO object with location.
		"""
		file = None
		try:
			# pylint: disable=maybe-no-member
			request = self.service.files().get_media(fileId = file_id)
			file = io.BytesIO()
			downloader = googleapiclient.http.MediaIoBaseDownload(file, request)
			done = False
			while done is False:
				status, done = downloader.next_chunk()
				if do_debug:
					logger.info(f'Download {int(status.progress() * 100)}% of "{file_id}"')
	
		except googleapiclient.errors.HttpError as error:
			logger.error(F'An error occurred: {error}')
			file = None
	
		return file and file.getvalue() or None
	
	
	def create_folder(self, file_metadata = dict()):
		"""Create new folder.
		Args:
			file_metadata - the data for the new folder such as parent ids and name 
		Returns : Id's of the new folder
		"""
		try:
			file_metadata["mimeType"] = FOLDER_MIMETYPE
			# pylint: disable=maybe-no-member
			file = self.service.files().create(body = file_metadata, fields = 'id', **self.common_paramters).execute()
			logger.info(F'Folder ID: "{file.get("id")}".')
			return file.get('id')
		except googleapiclient.errors.HttpError as error:
			logger.error(F'An error occurred: {error}')
		return None

	def _upload_media(self, media, file_metadata = dict(), do_debug = False):
		"""Upload new file.
		Args:
			media - the media to upload
		Returns : Id's of the file uploaded
		"""
		file = None
		try:
			# pylint: disable=maybe-no-member
			file = self.service.files().create(body = file_metadata, media_body = media, fields = 'id', **self.common_paramters).execute()
			if do_debug:
				logger.info(F'File upload resulted in ID: {file.get("id")}')
		except googleapiclient.errors.HttpError as error:
			logger.error(F'An error occurred during file upload: {error}')
			file = None
		return file and file.get('id') or None


	def upload_file(self, file_path, file_metadata = dict(), mimetype = default_mimetype):
		"""Upload new file.
		Args:
			file_path - The local path of the file
			file_metadata - The metadata to give the file (NOTE: In no file name is present, the file_path is used)
			mimetype - The file mimetype
		Returns : Id's of the file uploaded
		"""
		if not file_metadata.get('name'):
			file_metadata['name'] = os.path.basename(file_path)
		media = MediaFileUpload(file_path, mimetype = mimetype)
		return self._upload_media(media = media, file_metadata = file_metadata)
				
	def upload_bytes(self, bytes, file_metadata = dict(), mimetype = default_mimetype):
		"""Upload new bytes object.
		Args:
			bytes - The bytes that make up the file body
			file_metadata - The metadata to give the file (NOTE: Needs to have the file's name)
			mimetype - The file mimetype
		Returns : Id's of the file uploaded
		"""
		if not file_metadata.get('name'):
			return None, "No filename provided"
		media = MediaIoBaseUpload(io.BytesIO(bytes), mimetype = mimetype)
		return self._upload_media(media, file_metadata = file_metadata)

	def update_file_metadata(self, id, file_metadata):
		"""Update file metadata.
		Args:
			id - The id of the file to update
			file_metadata - The metadata to give the file
		Returns : Id's of the file that was updated
		"""
		file = None
		try:
			file = self.service.files().update(fileId=id, body = file_metadata, fields = 'id', **self.common_paramters).execute()
		except googleapiclient.errors.HttpError as error:
			logger.info(F'An error occurred during file update: {error}')
			file = None
		return file and file.get('id') or None

	def file_exists(self, id):
		"""Check if file exists
		Args:
			id - The id of the file to look for
		Returns : True if file exists
		"""
		try:
			ret = self.service.files().get(fileId = id, **self.common_paramters).execute()
			return ret and True or False
		except googleapiclient.errors.HttpError as error:
			logger.info(F'An error occurred during file exist check: {error}')
		return False

	def file_meta(self, id):
		"""Return file meta
		Args:
			id - The id of the file to look for
		Returns : Meta for the file
		"""
		try:
			ret = self.service.files().get(fileId = id, **self.common_paramters).execute()
			return ret or None
		except googleapiclient.errors.HttpError as error:
			logger.info(F'An error occurred during file meta: {error}')
		return False

def create_service_account(project_id, name, display_name):
	"""Creates a service account."""

	credentials = service_account.Credentials.from_service_account_file(
		filename = os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
		scopes = ['https://www.googleapis.com/auth/cloud-platform'])

	service = googleapiclient.discovery.build(
		'iam', 'v1', credentials = credentials)

	my_service_account = service.projects().serviceAccounts().create(
		name = 'projects/' + project_id,
		body = {
			'accountId': name,
			'serviceAccount': {
				'displayName': display_name
			}
		}).execute()

	logger.error('Created service account: ' + my_service_account['email'])
	return my_service_account
