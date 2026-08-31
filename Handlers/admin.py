import os

from bot_instance import bot
from config import ADMIN_ID

from keyboards import admin_menu

from Services.excel_service import (
    read_excel,
    validate_columns,
    validate_rows,
    select_required_columns
)

from Database.queries import add_shipment


admin_states = {}


def register_admin_handlers():

    # =========================
    # Admin Panel
    # =========================

    @bot.message_handler(commands=["admin"])
    def admin_panel(message):

        if message.from_user.id != ADMIN_ID:

            bot.send_message(
                message.chat.id,
                "⛔ شما اجازه دسترسی به پنل مدیریت را ندارید."
            )

            return

        bot.send_message(
            message.chat.id,
            "👨‍💼 به پنل مدیریت خوش آمدید.",
            reply_markup=admin_menu()
        )

    # =========================
    # Upload Excel Button
    # =========================

    @bot.message_handler(
        func=lambda message:
        message.text == "📤 آپلود Excel"
    )
    def upload_excel_button(message):

        if message.from_user.id != ADMIN_ID:
            return

        admin_states[message.from_user.id] = {
            "state": "waiting_for_excel"
        }

        bot.send_message(
            message.chat.id,
            "📤 لطفاً فایل Excel را ارسال کنید."
        )

    # =========================
    # Receive Excel
    # =========================

    @bot.message_handler(
        content_types=["document"]
    )
    def receive_excel(message):

        if message.from_user.id != ADMIN_ID:
            return

        user_id = message.from_user.id

        state = admin_states.get(user_id)

        if not state:
            return

        if state["state"] != "waiting_for_excel":
            return

        document = message.document

        if not document.file_name.lower().endswith(
            (".xlsx", ".xls")
        ):

            bot.send_message(
                message.chat.id,
                "❌ لطفاً فایل Excel ارسال کنید."
            )

            return

        file_path = f"temp_{user_id}.xlsx"

        try:

            # -------------------------
            # Download Excel
            # -------------------------

            file_info = bot.get_file(
                document.file_id
            )

            downloaded_file = bot.download_file(
                file_info.file_path
            )

            with open(file_path, "wb") as file:

                file.write(downloaded_file)

            # -------------------------
            # Read Excel
            # -------------------------

            df = read_excel(file_path)
            
            if df is None:

                bot.send_message(
                    message.chat.id,
                    "❌ خواندن فایل Excel ناموفق بود."
                )

                return
            
            df = select_required_columns(df)

            # -------------------------
            # Validate Columns
            # -------------------------

            if not validate_columns(df):

                bot.send_message(
                    message.chat.id,
                    """
❌ ساختار فایل صحیح نیست.

ستون‌های مورد نیاز:

نام
نام خانوادگی
موبایل
کد پیگیری
"""
                )

                return

            # -------------------------
            # Validate Rows
            # -------------------------

            valid_rows, invalid_rows = validate_rows(df)

            # -------------------------
            # Duplicate Tracking Codes
            # -------------------------

            
            final_rows = valid_rows
            duplicate_rows = []

            # -------------------------
            # Save State
            # -------------------------

            admin_states[user_id] = {
                "state": "waiting_for_shipment_date",
                "rows": final_rows
            }

            # -------------------------
            # Send Result
            # -------------------------

            bot.send_message(
                message.chat.id,
                f"""
✅ فایل بررسی شد.

📊 کل ردیف‌ها: {len(df)}

✅ ردیف‌های معتبر: {len(valid_rows)}

❌ ردیف‌های نامعتبر: {len(invalid_rows)}

🔁 کدهای تکراری: {len(duplicate_rows)}

📦 آماده ثبت: {len(final_rows)}

📅 لطفاً تاریخ این مرسولات را وارد کنید.

مثال:

1405/05/25
"""
            )

        except Exception as e:

            print(f"Excel Error: {e}")

            bot.send_message(
                message.chat.id,
                "❌ خطایی هنگام پردازش فایل رخ داد."
            )

        finally:

            if os.path.exists(file_path):

                os.remove(file_path)

    # =========================
    # Receive Shipment Date
    # =========================

    @bot.message_handler(
        func=lambda message:
        message.from_user.id == ADMIN_ID
        and admin_states.get(
            message.from_user.id,
            {}
        ).get("state") == "waiting_for_shipment_date"
    )
    def receive_shipment_date(message):

        user_id = message.from_user.id

        shipment_date = message.text.strip()

        state = admin_states.get(user_id)

        if not state:
            return

        rows = state["rows"]

        if not rows:

            bot.send_message(
                message.chat.id,
                "❌ هیچ مرسوله‌ای برای ثبت وجود ندارد."
            )

            admin_states.pop(user_id, None)

            return

        try:

            saved_count = 0

            for row in rows:

                add_shipment(
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    phone=row["phone"],
                    tracking_code=row["tracking_code"],
                    shipment_date=shipment_date,
                    city=row["city"]
                )

                saved_count += 1

            bot.send_message(
                message.chat.id,
                f"""
                ✅ ثبت مرسوله‌ها با موفقیت انجام شد.
                📦 تعداد ثبت شده: {saved_count}
                📅 تاریخ مرسولات:
                {shipment_date}
                """
            )

            # پاک کردن State
            admin_states.pop(user_id, None)

        except Exception as e:

            print(f"Database Error: {e}")

            bot.send_message(
                message.chat.id,
                "❌ هنگام ذخیره مرسوله‌ها مشکلی ایجاد شد."
            )