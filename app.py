from flask import Flask, request
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from stock import get_stock_price
from stock import report_watchlist
app = Flask(__name__)
CHANNEL_SECRET = "eff61e65b8b788cf861aa0449464d133"
CHANNEL_ACCESS_TOKEN = "joqleacwwZM0GSgthvivD8utdps84j4urkCIuOusNVCzEC1F0Z2mfKo+rSrTDpyASsHSAYF3aqTDqEe6PewCaTjKmSXU5h+AypfmzLztpWTy/v32paTZDfv5aHftR/DsT+f6lJlFm8S6uE9lsaUOMAdB04t89/1O/w1cDnyilFU="

configuration = Configuration(
    access_token=CHANNEL_ACCESS_TOKEN
)

handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/")
def home():
    return "Stock Bot Running"

@app.route("/callback", methods=["POST"])
def callback():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        handler.handle(body, signature)

        return "OK", 200

    except Exception as e:
        print("callback 錯誤：", e)
        return "OK", 200

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text.strip()
    msg = text.lower()

    if msg == "watchlist":
        reply_text = report_watchlist()

    else:
        result = get_stock_price(text)

        if result:
            reply_text = (
                f"{text}\n"
                f"股價：{result['price']}\n"
                f"漲跌幅：{result['percent']}%"
            )
        else:
            reply_text = "查無資料，請輸入股票代碼，例如：2330，或輸入 watchlist"

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=reply_text)
                ]
            )
        )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

