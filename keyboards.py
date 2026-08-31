from telebot.types import(
ReplyKeyboardMarkup ,
KeyboardButton,
InlineKeyboardButton,
InlineKeyboardMarkup,
CopyTextButton
)

def admin_menu():
    keyboard = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    
    keyboard.add(
        KeyboardButton("➕ افزودن مرسوله"),
        KeyboardButton("📤 آپلود Excel"),
        KeyboardButton("📦 مشاهده مرسوله‌ها"),
        KeyboardButton("🔎 جستجوی مرسوله"),
        KeyboardButton("🗑 حذف مرسوله"),
        KeyboardButton("📊 آمار")
    )
    return keyboard


def customer_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    
    keyboard.add(
        KeyboardButton("🔎 جستجوی کد پیگیری")
    )
    return keyboard


def selection_menu(results):
    keyboard = InlineKeyboardMarkup()
    
    for i , shipment in enumerate(results,start=1):
        button_text =(
            f"📦 {shipment['city']} | "
            f"{shipment['shipment_date']}"
        )
        
        callback_data = (
           f"shipment_{shipment['id']}" 
        )
        
        keyboard.add(
            InlineKeyboardButton(
                button_text,
                callback_data=callback_data
            )
        )
    return keyboard
    
    
def follow_menu(tracking_code):
    keyboard = InlineKeyboardMarkup()
    
    keyboard.add(
        InlineKeyboardButton(
            text ="📋 کپی کد پیگیری", 
            copy_text = CopyTextButton(
                text = tracking_code
            )
        ),
        InlineKeyboardButton("🌐 پیگیری در سایت پست",url="https://tracking.post.ir/")
    )
    return keyboard
        
