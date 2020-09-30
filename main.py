from telegram import File, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
import requests
from subprocess import Popen, PIPE
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

try:  
  os.system('mkdir downloads')
  os.system('cd downloads')
except:
  pass

def start(bot, update):
  START = '''❤️ Welcome To <b>AnonFiles</b> Bot

This Bot Can Upload Document,Videos,Photos To anonfiles.com
For Now Currently Limit Is 20MB, Its Gonna Increased Upto 1.5GB In Future

♨️ Just Send The File You Wanna Upload and Leave The Rest On Bot :-) '''

  keyboard = [[InlineKeyboardButton(text="🔥Support🔥", url="https://t.me/Technology_Arena"),
               InlineKeyboardButton(text="♻️Donate♻️", url="https://t.me/TheDarkW3b")]]
  
  if update.effective_message.chat.type != "private":
    update.message.reply_text("Use Me In Private :-)")
  else:
    update.message.reply_text(START, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
      
def photo(bot, update):
  try:
    media_id = update.effective_message.photo[-1].file_id
    newFile = bot.getFile(media_id)
    fileName = os.path.split(newFile.file_path)[-1]
    newFile.download(fileName)
    bot.sendMessage(chat_id=update.message.chat_id, text="⚡️ Downloaded, Trying To Upload On AnonFile")
    stdout = Popen(f'curl -F "file=@{fileName}" https://api.anonfiles.com/upload', shell=True, stdout=PIPE).stdout
    output = stdout.read()
    visit = json.loads(output)
    full_link = visit['data']['file']['url']['full']
    short_link = visit['data']['file']['url']['short']
    messagee = f'''❤️ <b>Succesfully Uploaded</b>

Short Link :- {short_link}
Full Link :- {full_link}
'''

    update.message.reply_text(messagee, parse_mode=ParseMode.HTML)
  except:
    update.message.reply_text("Kindly Send Me Photos Less Then 20 MB")
  try:
    os.remove(fileName)
  except:
    pass
    
def documentt(bot, update):
  try:
      media_id = update.effective_message.document.file_id
      fileName = update.effective_message.document.file_name
      
      newFile = bot.getFile(media_id)
      newFile.download(fileName)
      bot.sendMessage(chat_id=update.message.chat_id, text="Downloaded, Trying To Upload On AnonFile")
      stdout = Popen(f'curl -F "file=@{fileName}" https://api.anonfiles.com/upload', shell=True, stdout=PIPE).stdout
      output = stdout.read()
      visit = json.loads(output)
      full_link = visit['data']['file']['url']['full']
      short_link = visit['data']['file']['url']['short']
      messagee = f'''❤️ <b>Succesfully Uploaded</b>

Short Link :- {short_link}
Full Link :- {full_link}
'''

      update.message.reply_text(messagee, parse_mode=ParseMode.HTML)
  except:
      update.message.reply_text("Kindly Send Me Files Less Then 20 MB")
  try:
      os.remove(fileName)
  except:
      pass

def videoo(bot, update):
  try:
      video_id = update.effective_message.video.file_id
      fileName = os.path.split(newFile.file_path)[-1]
      newFile = bot.getFile(video_id)
      newFile.download(fileName)
      bot.sendMessage(chat_id=update.message.chat_id, text="Downloaded, Trying To Upload On AnonFile")
      stdout = Popen(f'curl -F "file=@{fileName}" https://api.anonfiles.com/upload', shell=True, stdout=PIPE).stdout
      output = stdout.read()
      visit = json.loads(output)
      full_link = visit['data']['file']['url']['full']
      short_link = visit['data']['file']['url']['short']
      messagee = f'''❤️ <b>Succesfully Uploaded</b>

Short Link :- {short_link}
Full Link :- {full_link}
'''

      update.message.reply_text(messagee, parse_mode=ParseMode.HTML)
  except:
      update.message.reply_text("Kindly Send Me Videos Less Then 20 MB")
  try:
      os.remove(fileName)
  except:
      pass
    
def main():
  updater = Updater(TOKEN)
  dp = updater.dispatcher
  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(MessageHandler(Filters.photo, photo))
  dp.add_handler(MessageHandler(Filters.document, documentt))
  dp.add_handler(MessageHandler(Filters.document, videoo))
  updater.start_polling()
  logging.info("Starting Long Polling!")
  updater.idle()

if __name__=='__main__':
  main()
