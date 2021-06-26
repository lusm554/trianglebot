from telegram.ext import *
from telegram import *
from decouple import config as cfg
import logging
from figures import Figure
from multiprocessing import Process, Queue

updater = Updater(token=cfg('TOKEN'))
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Command logic
def start(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text='Hello, World')

def info(update, context):
  inf = '/start - start bot session\n'
  context.bot.send_message(chat_id=update.effective_chat.id, text=inf)

def figure(update, context):
  f = Figure('triangle')
  q = Queue()
  p = Process(target=f.add_value, args=(q, (4, 4)))
  p.start()
  p.join()
  
  img = q.get()  
  
  context.bot.send_message(chat_id=update.effective_chat.id, text=img)

def inline_caps(update, context):
  query = update.inline_query.query
  if not query: return
  resutls = list()
  resutls.append(
    InlineQueryResultArticle(
      id = query.upper(),
      title = 'Caps',
      input_message_content=InputTextMessageContent(query.upper())
    )
  )
  context.bot.answer_inline_query(update.inline_query.id, results)
  

# Add handlers for commands 
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

figure_handler = CommandHandler('figure', figure)
dispatcher.add_handler(figure_handler)

info_handler = CommandHandler('info', info)
dispatcher.add_handler(info_handler)

def main():
  # Start bot
  updater.start_polling()

if __name__ == '__main__':
  main()
