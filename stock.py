import yfinance as yf

if stock_id == "0000":
    symbol = "^TWII"
else:
    symbol = f"{stock_id}.TW"
watchlist = ["0000","2330","0050","00631L","2327","2383","3532","2303","2344"]

def get_stock_price(stock_id):
    stock = yf.Ticker(stock_id + ".TW")
    data = stock.history(period="2d")
    if len(data) < 2:
        return None
    current = float(data["Close"].iloc[-1])
    previous = float(data["Close"].iloc[-2])
    percent = ((current - previous) / previous) * 100
    return {
        "price": round(current, 2),
        "percent": round(percent, 2)
    }

def report_watchlist():
    result_text = ""
    for stock in watchlist:
        result = get_stock_price(stock)
        result_text += (
            f"{stock}\n"
            f"股價：{result['price']}\n"
            f"漲跌幅：{result['percent']}%\n\n"
        )
    return result_text