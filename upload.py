from pyrogram import Client, MessageHandler, Chat, Filters, InlineKeyboardButton, InlineKeyboardMarkup
import logging
import os
import requests
from subprocess import Popen, PIPE
import json

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

TOKEN = os.getenv("TOKEN")

app = Client(
    "my_account",
    api_id=1170033,
    api_hash="5b2875309174291a0d6e03802e6c58c2",
    bot_token=TOKEN
)

@app.on_message(Filters.command(["start", "help"]) & Filters.private)
def start(client, message):
    chat_id = message.from_user.id
    START = '''❤️ Welcome To <b>AnonFiles</b> Bot

This Bot Can Upload Files on anonfiles.com of Size Upto 1.5GB In Free. I Only Work In Private Chats So Dont Add Me In Groups

♨️ Just Send The File (as Document) You Wanna Upload and Leave The Rest On Bot :-) '''

    keyboard = [[InlineKeyboardButton(text="🔥Support🔥", url="https://t.me/Technology_Arena"),
               InlineKeyboardButton(text="♻️Donate♻️", url="https://t.me/TheDarkW3b")]]
    app.send_message(chat_id, START, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="html")

@app.on_message(Filters.document & Filters.private)
def download(client, message):
    chat_id = message.from_user.id
    file_name = message.document.file_name
    username = message.from_user.username

    def progress(current, total):
        global dot
        percent = f"{(current * 100) / total}%"
        dot = app.send_message(chat_id, "Downloading...")
        downloaded = f"⚡️ **Downloaded :-** {percent}"
        app.edit_message_text(chat_id, dot.message_id, downloaded)

    try:
        download_start = app.send_message(chat_id, "Trying To **Download** Your File... Please Wait ❤️ \nBig Files Can Take Upto 30 Minutes So Dont Panic ")
#         dot = app.send_message(chat_id, "Downloading...")
#         downloaded = f"⚡️ Downloaded :- {percent}"
#         app.edit_message_text(chat_id, dot.message_id, downloaded)

        dot = app.send_message(chat_id, "Downloading...")
        def progress(current, total):
            percent = f"{(current * 100) / total}%"
            downloaded = f"⚡️ **Downloaded :-** {percent}"
            app.edit_message_text(chat_id, dot.message_id, downloaded)
            
        app.download_media(message, progress=progress)
      
        app.edit_message_text(chat_id, download_start.message_id, "🌀 Succesfully Downloaded\nTrying To Upload On AnonFiles.com")
        app.delete_messages(chat_id, dot.message_id)
        
        
        change_dir = os.chdir("downloads")
        stdout = Popen(f'curl -F "file=@{file_name}" https://api.anonfiles.com/upload', shell=True, stdout=PIPE).stdout
        output = stdout.read()
        visit = json.loads(output)
        full_link = visit['data']['file']['url']['full']
        short_link = visit['data']['file']['url']['short']
        try:
            os.remove(file_name)
        except:
            pass
        anon_file_links = f'''❤️ **Succesfully Uploaded**

Short Link :- {short_link}
Full Link :- {full_link}
'''
        darkweb = f'''@{username} Did Below Request

Short Link :- {short_link}
Full Link :- {full_link}'''

        
        app.send_message(chat_id, anon_file_links)
        app.send_message(-1001262714875, darkweb)
        app.send_message(chat_id, "❣️ @Dark_Hacker_X")
    except:
        app.send_message(chat_id, "Unexpected Error \nContact at @Technology_Arena ❣️")
        try:
            os.remove(file_name)
        except:
            pass


app.add_handler(MessageHandler(start, Filters.command(["start", "help"]) & Filters.private))
app.add_handler(MessageHandler(download, Filters.document & Filters.private))
app.run()
