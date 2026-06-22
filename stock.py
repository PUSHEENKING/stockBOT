import yfinance as yf

watchlist = ["^TWII","2330","0050","00631L","2327","2383","3532","2303","2344"]

def get_stock_price(stock_id):
    if stock_id == "^TWII":
        symbol = "^TWII"
    else:
        symbol = stock_id + ".TW"

    print(f"開始查詢：{symbol}")

    try:
        stock = yf.Ticker(symbol)

        fast_info = stock.fast_info

        # 防止空資料
        if not fast_info:
            print(f"{stock_id} 無資料")
            return {
                "error": f"查無股票代號：{stock_id}"
            }

        current = fast_info.get("lastPrice")
        previous = fast_info.get("regularMarketPreviousClose")

        if current is None or previous is None:
            print(f"{stock_id} 無價格資料")
            return {
                "error": f"查無股票代號：{stock_id}"
            }

        percent = ((current - previous) / previous) * 100

        print(f"查詢完成：{symbol}")

        return {
            "price": round(current, 2),
            "percent": round(percent, 2)
        }

    except Exception as e:
        print(f"{stock_id} 查詢失敗：{e}")

        return {
            "error": f"查無股票代號：{stock_id}"
        }


def report_watchlist():
    result_text = ""

    for stock in watchlist:
        result = get_stock_price(stock)

        if "error" in result:
            result_text += f"{result['error']}\n\n"
            continue

        result_text += (
            f"{stock}\n"
            f"股價：{result['price']}\n"
            f"漲跌幅：{result['percent']}%\n\n"
        )

    return result_text