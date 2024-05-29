from telethon.sync import TelegramClient

# Your API ID and API hash obtained from my.telegram.org
api_id = '18699028'
api_hash = '867b7de317dbe0159276be1b56191e25'

# Create a new Telethon client session
with TelegramClient('session_name', api_id, api_hash) as client:
    # Print the string session
    print(client.session.save())

# Replace 'session_name', 'YOUR_API_ID', and 'YOUR_API_HASH' with your own values.
