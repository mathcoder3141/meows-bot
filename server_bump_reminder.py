#!/home/randall/anaconda3/bin/python

from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv
import os

load_dotenv()

def server_bump_reminder():
    """
    Executes webhook sending a reminder moderators to bump the channel.
    """
    user_id = os.getenv('user_id')
    allowed_mentions = {
    "users" : user_id.split(',')
    }
    webhook = DiscordWebhook(
        url=os.getenv('webhook_url'),
        content='Reminder to bump server. Command for this is `!d bump`. cc <@!'+user_id.split(',')[0]+'>, <@!'+user_id.split(',')[1]+'>, <@!'+user_id.split(',')[2]+'>, <@!'+user_id.split(',')[3]+'>',
        allowed_mentions=allowed_mentions
        )
    result = webhook.execute()

if __name__ == "__main__":
    server_bump_reminder()