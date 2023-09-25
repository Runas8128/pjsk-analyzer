import os.path
import dotenv
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from os import environ
from bot import bot

bot.run(environ.get('TOKEN'))
