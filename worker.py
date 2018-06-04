from app.actions import Actions
from app.utils.slackhelper import SlackHelper


# Main function
def main():
	slackhelper = SlackHelper()
	actions = Actions(slackhelper)
	actions.notify_channel()


if __name__ == '__main__':
	main()
