
import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message
import pygraphviz as pgv
load_dotenv()


machine = TocMachine(
    states=["user","food","show_fsm_pic","restaurant","breakfast","lunch","dinner","healthyfood","dessert","menu","choose", "eat","Asiaexchange","EAexchange","exchange_SGD", "exchange_JPY","exchange_CNY","exchange_else","exchange_CAD", "exchange_USD", "exchange_GBP","exchange_back"],
    transitions=[
        { #第1-1階段
            "trigger": "advance",
            "source": "user",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        { #第1-2階段選擇查詢匯率
            "trigger": "advance",
            "source": "menu",
            "dest": "choose",
            "conditions": "is_going_to_choose",
        },

        { #第1-3階段選擇今天吃什麼
            "trigger": "advance",
            "source": "menu",
            "dest": "eat",
            "conditions": "is_going_to_eat",
        },

        { #第2-1-查詢亞洲匯率
            "trigger": "advance",
            "source": "choose",
            "dest": "Asiaexchange",
            "conditions": "is_going_to_Asiaexchange",
        },
        { #第2-2-查詢歐美及其他匯率
            "trigger": "advance",
            "source": "choose",
            "dest": "EAexchange",
            "conditions": "is_going_to_EAexchange",
        },
        { #第3-1 新加坡幣
            "trigger": "advance",
            "source": "Asiaexchange",
            "dest": "exchange_SGD",
            "conditions": "is_going_to_exchange_SGD",
        },
        { #第3-2 人民幣
            "trigger": "advance",
            "source": "Asiaexchange",
            "dest": "exchange_CNY",
            "conditions": "is_going_to_exchange_CNY",
        },
        { #第3-3 日元
            "trigger": "advance",
            "source": "Asiaexchange",
            "dest": "exchange_JPY",
            "conditions": "is_going_to_exchange_JPY",
        },
        { #第3-4 其他
            "trigger": "advance",
            "source": "Asiaexchange",
            "dest": "exchange_else",
            "conditions": "is_going_to_exchange_else",
        },
        { #第4-1 美元
            "trigger": "advance",
            "source": "EAexchange",
            "dest": "exchange_USD",
            "conditions": "is_going_to_exchange_USD",
        },
        { #第4-2 英鎊
            "trigger": "advance",
            "source": "EAexchange",
            "dest": "exchange_GBP",
            "conditions": "is_going_to_exchange_GBP",
        },
        { #第4-3 加拿大幣
            "trigger": "advance",
            "source": "EAexchange",
            "dest": "exchange_CAD",
            "conditions": "is_going_to_exchange_CAD",
        },
        { #第4-4 其他
            "trigger": "advance",
            "source": "EAexchange",
            "dest": "exchange_back",
            "conditions": "is_going_to_exchange_back",
        },
        
        {#2-1按食物種類
            "trigger": "advance",
            "source": "eat",
            "dest": "food",
            "conditions": "is_going_to_food",
        },
        {#2-2餐廳推薦
            "trigger": "advance",
            "source": "eat",
            "dest": "restaurant",
            "conditions": "is_going_to_restaurant",
        },
        {#3-1早餐
            "trigger": "advance",
            "source": "food",
            "dest": "breakfast",
            "conditions": "is_going_to_breakfast",
        },
        {#3-2午餐
            "trigger": "advance",
            "source": "food",
            "dest": "lunch",
            "conditions": "is_going_to_lunch",
        },{#3-3晚餐
            "trigger": "advance",
            "source": "food",
            "dest": "dinner",
            "conditions": "is_going_to_dinner",
        },
        {#3-4健康食品
            "trigger": "advance",
            "source": "restaurant",
            "dest": "healthyfood",
            "conditions": "is_going_to_healthyfood",
        },
        {#3-5甜品等
            "trigger": "advance",
            "source": "restaurant",
            "dest": "dessert",
            "conditions": "is_going_to_dessert",
        },
        {#4-1查詢餐廳
            "trigger": "advance",
            "source": "eat",
            "dest": "restaurant",
            "conditions": "is_going_to_restaurant",
        },
         {
            "trigger": "advance",
            "source": "user",
            "dest": "show_fsm_pic",
            "conditions": "is_going_to_show_fsm_pic",
        },

        {"trigger": "go_back", "source": ["menu","show_fsm_pic","food","restaurant","breakfast","lunch","dinner","healthyfood","dessert","eat","choose","Asiaexchange","EAexchange","exchange_SGD", "exchange_CNY","exchange_JPY","exchange_else","exchange_USD", "exchange_CAD", "exchange_GBP","exchange_back"], "dest": "user"},
   

    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
