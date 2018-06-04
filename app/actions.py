from app.utils.gappshelper import GappsHelper
# from config import get_env


class Actions:
	def __init__(self, slackhelper, user_info):
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
			# self.slackhelper.post_message(text_detail, recipient)
		return self.slackhelper.post_message(text_detail, recipient)

	def show_tasks(self, date=None):
		pass

	def help(self):
		pass
