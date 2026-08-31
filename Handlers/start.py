from bot_instance import bot
from config import ADMIN_ID

from keyboards import(
    admin_menu,
    customer_menu
)

def register_start_handler():
    
    @bot.message_handler(commands=["start"])
    def start(message):

        user_id = message.from_user.id

        # بررسی مدیر
        if user_id == ADMIN_ID:

            bot.send_message(
                message.chat.id,
                "👨‍💼 به پنل مدیریت خوش آمدید.",
                reply_markup=admin_menu()
            )

        # کاربر عادی
        else:

            bot.send_message(
                message.chat.id,
                "👋 به سامانه پیگیری مرسولات خوش آمدید.",
                reply_markup=customer_menu()
            )
    