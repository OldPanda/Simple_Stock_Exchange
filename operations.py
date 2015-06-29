import urllib2
import json


def get_stock_info(symbol):
    """Get stock info from Benzinga API given symbol
    Args:
        symbol (str): a string(uppercase) used to do stock info query
    Returns:
        dict: a key-value info structure parsed from server response
    """
    request = "http://careers-data.benzinga.com/rest/richquote?symbols=" + symbol
    return json.loads(urllib2.urlopen(request).read())[symbol]


def buy_stock(session, quantity):
    """Buy "quantity" number of stock that user just queried
    Args:
        session (dict): current stock info and user's stock portfolio
        quantity (int): number of stocks to be bought
    Returns:
        bool: if this transaction succeed
        dict: updated session
        str: message which tells user the result of the transaction
    """
    total = session["cur_stock"]["askPrice"] * quantity
    if total > session["cash"]:
        # if money to be cost is more than how much user have
        return False, session, "Cash is not enough. "
    else:
        session["cash"] -= total
        session = add_stock_in_session(session, quantity)
        return True, session, "Success. "


def add_stock_in_session(session, quantity):
    """Update session when doing "buy stock"
    Args:
        session (dict): current stock info and user's portfolio
        quantity (int): number of stocks to be purchased
    Returns:
        dict: updated session
    """
    for i in xrange(len(session["portfolio"])):
        if session["portfolio"][i]["symbol"] == session["cur_stock"]["symbol"]:
            session["portfolio"][i]["num"] += quantity
            break
    else:
        # the stock doesn't exist in user's portfolio
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
    """Sell "quantity" number of stocks
    Args:
        session (dict): current stock info and user's portfolio
        quantity (int): number of stocks to be sold
    Returns:
        bool: if this transaction succeed
        dict: updated session
        str: message which tells user the result of the transaction
    """
    for i in xrange(len(session["portfolio"])):
        if session["portfolio"][i]["symbol"] == session["cur_stock"]["symbol"]:
            if session["portfolio"][i]["num"] < quantity:
                # the number of stock in portfolio is less than quantity
                return False, session, "You don't have enough stocks. "
            elif session["portfolio"][i]["num"] == quantity:
                # equal to quantity
                session["cash"] += quantity * session["cur_stock"]["bidPrice"]
                del session["portfolio"][i]
            else:
                # more than quantity
                session["cash"] += quantity * session["cur_stock"]["bidPrice"]
                session["portfolio"][i]["num"] -= quantity
            return True, session, "Success. "
    else:
        return False, session, "You don't have this stock. "
