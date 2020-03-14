# telegram-self-bot

Telegram self bot written in Python. Meant for user accounts to use for utility
functions.

You'll need a file called `.env`. In it, copy paste the below:

```
# The values below won't work. Get your own values from
# https://my.telegram.org under API development.
API_ID=3245234
API_HASH=39489aoeui392343o43p3
```

## Usage

```
usage: python bot.py [-h] [--chats] [--chat-id CHAT_ID] [--replace REPLACE]
                     [--search SEARCH] [--delete DELETE]

Run the Telegram Self Bot

optional arguments:
  -h, --help            show this help message and exit
  --chats, -c           Get all chats and their IDs.
  --chat-id CHAT_ID, -i CHAT_ID
                        Get ID of a chat based on name. For example, --chat-id
                        "Chat Name"
  --replace REPLACE, -r REPLACE
                        Replace instances of a word with another word in a
                        chat and is case insensitive. For example, --replace
                        "chat_id hello hi"
  --search SEARCH, -s SEARCH
                        Search for a phrase said by me and is case
                        insensitive. For example, --search "chat_id a phrase"
  --delete DELETE, -d DELETE
                        Delete messages in a chat by IDs. For example,
                        --delete "chat_id 111,222,333"
```
