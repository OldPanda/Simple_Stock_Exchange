import urllib2
import json


def get_stock_info(symbol):
    request = "http://careers-data.benzinga.com/rest/richquote?symbols=" + symbol
    return json.loads(urllib2.urlopen(request).read())[symbol]


def buy_stock(session, quantity):
    total = session["cur_stock"]["askPrice"] * quantity
    if total > session["cash"]:
        return False, session, "Cash is not enough. "
    else:
        session["cash"] -= total
        session = add_stock_in_session(session, quantity)
        return True, session, "Success. "


def add_stock_in_session(session, quantity):
    for i in xrange(len(session["portfolio"])):
        if session["portfolio"][i]["symbol"] == session["cur_stock"]["symbol"]:
            session["portfolio"][i]["num"] += quantity
            break
    else:
        session["portfolio"].append(
                {
                    "symbol": session["cur_stock"]["symbol"],
                    "name": session["cur_stock"]["name"],
                    "num": quantity,
                    "price": session["cur_stock"]["askPrice"]
                }
            )
    return session


def sell_stock(session, quantity):
    for i in xrange(len(session["portfolio"])):
        if session["portfolio"][i]["symbol"] == session["cur_stock"]["symbol"]:
            if session["portfolio"][i]["num"] < quantity:
                return False, session, "The stock in you portfolio is not enough. "
            elif session["portfolio"][i]["num"] == quantity:
                session["cash"] += quantity * session["cur_stock"]["bidPrice"]
                del session["portfolio"][i]
            else:
                session["cash"] += quantity * session["cur_stock"]["bidPrice"]
                session["portfolio"][i]["num"] -= quantity
            return True, session, "Success. "
    else:
        return False, session, "You don't have this stock. "
