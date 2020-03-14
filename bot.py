import argparse
import os
import re

from dotenv import load_dotenv
from telethon import TelegramClient, sync, errors

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the Telegram Self Bot")
    parser.add_argument(
        "--chats", "-c", action="store_true", help="Get all chats and their IDs."
    )
    parser.add_argument(
        "--chat-id",
        "-i",
        help='Get ID of a chat based on name. For example, --chat-id "Chat Name"',
    )
    parser.add_argument(
        "--replace",
        "-r",
        help='Replace instances of a word with another word in a chat and is case insensitive. For example, --replace "chat_id hello hi"',
    )
    parser.add_argument(
        "--search",
        "-s",
        help='Search for a phrase said by me and is case insensitive. For example, --search "chat_id a phrase"',
    )
    parser.add_argument(
        "--delete",
        "-d",
        help='Delete messages in a chat by IDs. For example, --delete "chat_id 111,222,333"',
    )
    args = parser.parse_args()
    return args


def get_cannot_edit_msg(message, reason):
    return f"Cannot edit {message.id}: {message.text}, {reason}"


def replace(client, args):
    chat_id, src_word, dest_word = args.replace.split()
    chat_id = int(chat_id)

    uneditable_message_ids = []
    for message in client.iter_messages(chat_id, search=src_word, from_user="me"):
        pattern = r"(\w*%s\w*)" % src_word
        new_message = re.sub(pattern, dest_word, message.text, flags=re.IGNORECASE)
        try:
            if message.forward is None:
                message.edit(new_message)
            else:
                print(get_cannot_edit_msg(message, "Message is forwarded"))
                uneditable_message_ids.append(message.id)
        except errors.rpcbaseerrors.ForbiddenError as e:
            print(get_cannot_edit_msg(message, f"Exception: {e}"))
            uneditable_message_ids.append(message.id)
    if len(uneditable_message_ids) > 0:
        print(
            "IDs of uneditable messages:", ",".join(map(str, uneditable_message_ids)),
        )


if __name__ == "__main__":
    args = parse_arguments()

    with TelegramClient("self_bot_session", API_ID, API_HASH) as client:
        if args.chats:
            for dialog in client.iter_dialogs():
                print(dialog.name, "has ID", dialog.id)
        elif args.chat_id is not None:
            chat_name = args.chat_id

            for dialog in client.iter_dialogs():
                if chat_name.lower() == dialog.name.lower():
                    print(dialog.name, "has ID", dialog.id)
        elif args.replace is not None:
            replace(client, args)
        elif args.search is not None:
            chat_id, phrase = args.search.split(" ", 1)
            chat_id = int(chat_id)

            for message in client.iter_messages(chat_id, search=phrase, from_user="me"):
                print(f"{message.id}: {message.text}")
        elif args.delete is not None:
            chat_id, message_ids = args.delete.split()
            chat_id = int(chat_id)

            message_ids = list(map(int, message_ids.split(",")))
            client.delete_messages(chat_id, message_ids)
