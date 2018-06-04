import gspread
from os import path
from config import get_env
from oauth2client.service_account import ServiceAccountCredentials


class GappsHelper:

	def __init__(self):
		# setup for google sheet - Google Drive API Instance
		self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		json_file_path = path.join(path.dirname(__file__), '../../', get_env('CLIENT_SECRET_FILE'))
		self.credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, self.scope)
		self.client = gspread.authorize(self.credentials)

	def open_sheet(self):
		sheet = self.client.open(get_env('GAPPS_SHEET_NAME')).sheet1
		return sheet.get_all_records(empty2zero=False, head=1, default_blank='')
