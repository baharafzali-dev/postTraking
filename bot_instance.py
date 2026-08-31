from telebot import TeleBot, apihelper

from config import TOKEN


apihelper.API_URL = "https://tapi.bale.ai/bot{0}/{1}"
apihelper.FILE_URL = "https://tapi.bale.ai/file/bot{0}/{1}"


bot = TeleBot(TOKEN)