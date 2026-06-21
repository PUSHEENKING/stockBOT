import yfinance as yf

watchlist = ["^TWII","2330","0050","00631L","2327","2383","3532","2303","2344"]

def get_stock_price(stock_id):
    if stock_id == "^TWII":
        symbol = "^TWII"
    else:
        symbol = stock_id + ".TW"

    try:
        stock = yf.Ticker(symbol)
        current = float(stock.fast_info["lastPrice"])
        previous = float(stock.fast_info["regularMarketPreviousClose"])
        percent = ((current - previous) / previous) * 100

        return {
            "price": round(current, 2),
            "percent": round(percent, 2)
        }

    except Exception as e:
        print(f"{stock_id} 查詢失敗：{e}")
        return None


def report_watchlist():
    result_text = ""

    for stock in watchlist:
        result = get_stock_price(stock)

        if result is None:
            result_text += f"{stock}\n查詢失敗\n\n"
            continue

        result_text += (
            f"{stock}\n"
            f"股價：{result['price']}\n"
            f"漲跌幅：{result['percent']}%\n\n"
        )
    return result_text