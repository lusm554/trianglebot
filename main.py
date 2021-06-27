from telegram.ext import *
from telegram import *
from decouple import config as cfg
import logging
from figures import Figure
from multiprocessing import Process, Queue
from datetime import datetime
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

FIGURE, ARGUMENTS = range(2)
IMG_EXT = 'png'
ASSETS_DIR = 'var'

def cmd_info(header='All commands:\n') -> str:
  '''Create string with information about all bot commands.'''
  cmd_info = {
    'start': 'Start draw figures',
    'help': 'Information about all commands',
    'figure': 'Draw certain figure and get img'
  }
  help_str = ''

  for cmd, ex in cmd_info.items():
    help_str += f'/{cmd} - {ex}\n' 

  return header + help_str

def getFigure(f, coors) -> str:
  img = os.path.join(ASSETS_DIR, '{}.{}'.format(datetime.timestamp(datetime.now()), IMG_EXT))
  if f == 'triangle':
    f = Figure('triangle')
    q = Queue()
    p = Process(target=f.add_value, args=(q, coors, img))
    p.start()
    p.join()
    img = q.get()
  return img

def removeFigure(f) -> None:
  os.remove(f)

def parse_arg(s):
  rawargs = [x.split('=') for x in s.split(' ')]
  return dict(rawargs)

# Commands logic
def help(update, context) -> None:
  '''Sends a message with information about commands.'''
  context.bot.send_message(chat_id=update.effective_chat.id, text=cmd_info())

def start(update, context) -> None:
  '''Sends a message with information about commands.'''
  header = 'Hey! My name is triangle and I can create triangles! U can share me with friend by @createtrianglebot\nHere is a list of my commands:\n' 
  context.bot.send_message(chat_id=update.effective_chat.id, text=cmd_info(header))

def startdraw(update, context) -> int:
  reply_keyboard = [['Triangle']]
  update.message.reply_text(
    'Please choose figure.',
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
  )
  return FIGURE 

def figure(update, context) -> int: 
  figure = update.message.text
  update.message.reply_text(
    f'Good! You selected {figure}.\n' \
    + 'Now enter the data for the Pythagorean theorem!\n' \
    + 'a - cathetus\n' \
    + 'b - cathetus\n' \
    + 'c - hypotenuse\n' \
    + 'Example:\n' \
    + 'a=5 b=5 or c=8 a=5',
    reply_markup=ReplyKeyboardRemove(),
  )
  return ARGUMENTS

def coordinates(update, context) -> int:
  rawcoors = update.message.text
  args = parse_arg(rawcoors) 
  
  f = getFigure('triangle', (args['a'], args['b']))
  context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f, 'rb'))
  removeFigure(f)
  
  return ConversationHandler.END

def cancel(update, context) -> int:
  update.message.reply_text(
    'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
  )

  return ConversationHandler.END

def main() -> None:
  '''Run the bot.'''
  global updater, dispatcher
  
  # Create dir for graphs
  if not os.path.exists('var'):
    os.makedirs('var')

  updater = Updater(token=cfg('TOKEN'))
  dispatcher = updater.dispatcher

  dispatcher.add_handler(CommandHandler('help', help))
  dispatcher.add_handler(CommandHandler('start', start))

  conv_handler = ConversationHandler(
    entry_points = [CommandHandler('figure', startdraw)],
    states = {
      FIGURE: [MessageHandler(Filters.regex('^(Triangle)$'), figure)],
      ARGUMENTS: [MessageHandler(Filters.text, coordinates)]
    },
    fallbacks = [CommandHandler('cancel', cancel)]
  )

  dispatcher.add_handler(conv_handler)
  
  # Start bot
  updater.start_polling()
  
  # Run the bot until user exit from process. i.e. presses Ctrl-C or the process receives SIGINT,
  # SIGTERM or SIGABRT
  updater.idle()

if __name__ == '__main__':
  main()


