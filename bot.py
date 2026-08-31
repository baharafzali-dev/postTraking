from bot_instance import bot

from Handlers.start import register_start_handler
from Handlers.admin import register_admin_handlers
from Handlers.customer import register_customer_handlers


import flask
from flask import request

from schema import create_tables

app = flask.Flask(__name__)

create_tables()

register_start_handler()
register_admin_handlers()
register_customer_handlers()

 
print("Bot Started...")

@app.route(f"/{bot}",metthods = ["POST"])
def webhook():
    raw = request.get_data().decode("utf-8")
    print(f"raw update : {raw}")
    update = type.update.de_json(raw)
    print(f"parsed update : {update}")
    bot.process_new_updates([update])
    return "OK" , 200

@app.route("/")
def index():
    return "bot is running!" , 200

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port=8080)