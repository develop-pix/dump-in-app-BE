from config.env import env

SLACK_API_TOKEN = env.str("SLACK_API_TOKEN", default=None)
SLACK_ERROR_CHANNEL_ID = env.str("SLACK_ERROR_CHANNEL_ID", default=None)
