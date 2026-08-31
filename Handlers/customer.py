from bot_instance import bot

from keyboards import(
    customer_menu,
    selection_menu,
    follow_menu
)

from Services.customer_service import(
    find_customer_shipments,
    get_customer_shipment,
    format_shipment_message
)

from Services.excel_service import(
    validate_phone,
    normalize_digits
)


customer_states = {}


def register_customer_handlers():
    
    @bot.message_handler(commands=["customer"])
    def customer_panel(message):
        
        customer_states[message.from_user.id] = {
            "state" : "waiting_for_first_name"
        }
        
        bot.send_message(
            message.chat.id,
            "👤 لطفاً نام خود را وارد کنید:"
        )
        
        
    @bot.message_handler(
    func=lambda message:
    message.text == "🔎 جستجوی کد پیگیری"
    )
    def search_tracking_button(message):

        customer_states[message.from_user.id] = {
            "state": "waiting_for_first_name"
        }

        bot.send_message(
            message.chat.id,
            "👤 لطفاً نام خود را وارد کنید:"
        ) 
            
         
            
    @bot.message_handler(
        func=lambda message:
        customer_states.get(
            message.from_user.id,
            {}
        ).get("state") == "waiting_for_first_name"
    )
    def receive_first_name(message):

        first_name = message.text.strip()

        customer_states[message.from_user.id] = {
            "state": "waiting_for_last_name",
            "first_name": first_name
        }

        bot.send_message(
            message.chat.id,
            "👤 لطفاً نام خانوادگی خود را وارد کنید:"
        )
        
        
        
    @bot.message_handler(
        func=lambda message:
        customer_states.get(
            message.from_user.id,
            {}
        ).get("state") == "waiting_for_last_name"
    )
    def receive_last_name(message):

        last_name = message.text.strip()

        state = customer_states[
            message.from_user.id
        ]

        state["last_name"] = last_name

        state["state"] = "waiting_for_phone"

        bot.send_message(
            message.chat.id,
            "📱 لطفاً شماره موبایل خود را وارد کنید:"
        ) 
        
        
    @bot.message_handler(
        func=lambda message:
        customer_states.get(
            message.from_user.id,
            {}
        ).get("state") == "waiting_for_phone"
    )
    def receive_phone(message):

        phone = normalize_digits(message.text.strip())
        
        if not validate_phone(phone):
            bot.send_message(
                message.chat.id,
                "❌ شماره تماس صحیح نیست.\n\n"
                "لطفاً شماره موبایل خود را به صورت "
                "11 رقمی وارد کنید.\n\n"
            )
        
            return

        state = customer_states[
            message.from_user.id
        ]

        first_name = state["first_name"]
        last_name = state["last_name"]

        results = find_customer_shipments(
            first_name,
            last_name,
            phone
        )

        if not results:

            bot.send_message(
                message.chat.id,
                "❌ مرسوله‌ای با این مشخصات پیدا نشد.",
                reply_markup=customer_menu()
            )

            customer_states.pop(
                message.from_user.id,
                None
            )

            return
        
        if len(results) == 1:
            shipment = results[0]
            
            bot.send_message(
                message.chat.id,
                format_shipment_message(shipment),
                parse_mode="Markdown",
                reply_markup=follow_menu(
                    shipment["tracking_code"]
                )
            )
            return

        keyboard = selection_menu(results)
        
        
        bot.send_message(
            message.chat.id,
            (
                    f"📦 {len(results)} مرسوله برای شما پیدا شد.\n\n"
                    f"👤 {results[0]['first_name']} "
                    f"{results[0]['last_name']}\n"
                    f"📱 {results[0]['phone']}\n\n"
                    "👇 لطفاً مرسوله موردنظر خود را انتخاب کنید:"
            ),
            reply_markup=keyboard
        )

        customer_states.pop(
            message.from_user.id,
            None
        )  
        
    
    @bot.callback_query_handler(
        func=lambda call:
        call.data.startswith("shipment_")
    )
    def show_select(call):
        shipment_id = int(
            call.data.split("_")[1]
        )
        
        shipment = get_customer_shipment(
            shipment_id
        )
        
        if not shipment:
            bot.answer_callback_query(
                call.id,
                "❌ مرسوله پیدا نشد."
            )
            return
        
        response = format_shipment_message(shipment)
        
        bot.answer_callback_query(call.id)
        
        bot.send_message(
            call.message.chat.id,
            response,
            parse_mode="Markdown",
            reply_markup=follow_menu(
                shipment["tracking_code"]
            )
        )
        
        
        
        
    
    