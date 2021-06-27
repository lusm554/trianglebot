from telegram.ext import *
from telegram import *
from decouple import config as cfg
import logging
from figures import Figure
from multiprocessing import Process, Queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def cmd_info(header='All commands:\n') -> str:
  '''Create string with information about all bot commands.'''
  cmd_info = {
    'help': 'Information about all commands',
    'figure': 'Start draw figues',
    'start': 'Get img of certain figure'
  }
  help_str = ''
  for cmd, ex in cmd_info.items():
    help_str += f'/{cmd} - {ex}\n' 
  return header + help_str

def getFigure(f, coors):
  img = None
  if f == 'triangle':
    f = Figure('triangle')
    q = Queue()
    p = Process(target=f.add_value, args=(q, (4, 4)))
    p.start()
    p.join()
    img = q.get()
  return img

# Commands logic
def help(update, context) -> None:
  '''Sends a message with information about commands.'''
  context.bot.send_message(chat_id=update.effective_chat.id, text=cmd_info())

def start(update, context) -> None:
  '''Sends a message with information about commands.'''
  header = 'Hey! My name is triangle and I can create triangles! U can share me with friend by @createtrianglebot\nHere is a list of my commands:\n' 
  context.bot.send_message(chat_id=update.effective_chat.id, text=cmd_info(header))

def figure(update, context) -> None:
  '''Sends a messag with three inline buttons attached.'''
  keyboard = [
    [InlineKeyboardButton("Triangle", callback_data='triangle')],
  ] 
    
  reply_markup = InlineKeyboardMarkup(keyboard)
  update.message.reply_text('Please choose figure:', reply_markup=reply_markup)  

def button(update, context) -> None:
  '''Parses the CallbackQuery and updates the message text.''' 
  query = update.callback_query
  query.answer()

  coors = (4, 4)
  f = getFigure(query.data, coors)
    
  query.edit_message_text(text='Loading...')
  #query.message.edit_media(
  #  media=InputMediaPhoto(open('test.jpg', 'rb'), caption='Title')
  #)
  context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('test.jpg', 'rb'))
  query.edit_message_text(text='Done.')
  
def unknown(update, context) -> None:
  '''Recognizes unknown commands and alerts the user.'''
  context.bot.send_message(chat_id=update.effective_chat.id, text="The command was not found.")

def main() -> None:
  '''Run the bot.'''
  global updater, dispatcher

  updater = Updater(token=cfg('TOKEN'))
  dispatcher = updater.dispatcher

  dispatcher.add_handler(CommandHandler('help', help))
  dispatcher.add_handler(CommandHandler('figure', figure))
  dispatcher.add_handler(CallbackQueryHandler(button))
  dispatcher.add_handler(CommandHandler('start', start))
  dispatcher.add_handler(MessageHandler(Filters.command, unknown))
  
  
  # Start bot
  updater.start_polling()
  
  # Run the bot until user exit from process. i.e. presses Ctrl-C or the process receives SIGINT,
  # SIGTERM or SIGABRT
  updater.idle()

if __name__ == '__main__':
  main()


