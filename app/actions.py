from app.utils.gappshelper import GappsHelper
import time
from datetime import datetime
from config import get_env


class Actions:
	def __init__(self, slackhelper, user_info=None):
		self.gappshelper = GappsHelper()
		self.sheet = self.gappshelper.open_sheet()
		self.user_info = user_info
		self.slackhelper = slackhelper

	def my_tasks(self):
		email = self.user_info['user']['profile']['email']
		recipient = self.user_info['user']['id']
		task_cells = list(filter(lambda x: x['Email Address'] == email, self.sheet))
		for index, row in enumerate(task_cells):
			text_detail = (
				'*Task #{} for {}:* \n\n'
				'*Hey {},* Today is the check-in day for your writeup titled\n'
				'`{}`.\n\n'
				'Whats the status of the article?\n'
				'PS: Please reply to this thread, the managers will review and reply you ASAP').format(str(index + 1), row['Next Check-In'], row['Name'], row['Most Recent Learning Experience you\'d like to write about'])
			self.slackhelper.post_message(text_detail, recipient)
		return None

	def show_tasks(self, date=None):
		# if match('', command_text[1]):
		recipient = self.user_info['user']['id']
		date_param = date.replace('-', ' ')
		task_cells = list(filter(lambda x: x['Next Check-In'] == date_param, self.sheet))
		for index, row in enumerate(task_cells):
			text_detail = (
				'*Task #{} for {}:* \n\n'
				'*Hey {},* Today is the check-in day for your writeup titled\n'
				'`{}`.\n\n'
				'Whats the status of the article?\n'
				'PS: Please reply to this thread, the managers will review and reply you ASAP').format(str(index + 1), row['Next Check-In'], row['Name'], row['Most Recent Learning Experience you\'d like to write about'])
			self.slackhelper.post_message(text_detail, recipient)
		# else:
		# 	response_body = {'text': 'Invalid Date/Day Param - `/ranti help` for available commands'}
		return None

	def num_suffix(self, check_in_date):
		"""
		Strip the date suffix and return the date
		Before comparing the date
		"""
		date_value = str(check_in_date).split(' ')
		day_value = date_value[0][:-2]
		date_value[0] = day_value
		return ' '.join(date_value)

	def notify_channel(self):
		while True:
			recipient = get_env('SLACK_CHANNEL')
			curent_time = datetime.now()
			current_hour = curent_time.hour
			current_minute = curent_time.minute

			if current_hour - 8 > 0:
				sleep_time = 24 - current_hour + 8 - (current_minute / 60)
			elif current_hour - 8 < 0:
				sleep_time = 8 - current_hour - (current_minute / 60)
			elif current_hour == 8:
				if current_minute == 0:
					sleep_time = 0
				else:
					sleep_time = 24 - current_hour + 8 - (current_minute / 60)

			# time.sleep(sleep_time * 3600)
			time.sleep(60)
			for index, row in enumerate(self.sheet):
				check_date = datetime.strptime(self.num_suffix(row['Next Check-In']), '%d %B %Y').date()
				todays_date = datetime.now().date()
				send_notif_date = check_date - todays_date

				if send_notif_date.days == 0:
					text_detail = (
						'*Task #{} for {}:* \n\n'
						'*Hey {},* Today is the check-in day for your writeup titled\n'
						'`{}`.\n\n'
						'Whats the status of the article?\n'
						'PS: Please reply to this thread, the managers will review and reply you ASAP').format(
						str(index + 1), row['Next Check-In'], row['Name'],
						row['Most Recent Learning Experience you\'d like to write about'])
					self.slackhelper.post_message(text_detail, recipient)
			# return None

	def help(self):
		return {
			'text': 'Available Commands: \n `/ranti my-task e.g. /ranti my-task` \n To get task assigned to you.\n'
					' \n `/ranti show-task [date] e.g. /ranti show-task 5th-june-2018` \n Show all tasks for a particular date \n'
					'\n `/ranti show-task [today] e.g. /ranti show-task today` \n Show all tasks for today \n'
					'\n `/ranti show-task [tomorrow] e.g. /ranti show-task tomorrow` \n Show all tasks for tomorrow \n'
					'\n `/ranti help` \n This help information \n \n Ranti Ver: 1.0'}
