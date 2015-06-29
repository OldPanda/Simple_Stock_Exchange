import tornado.web
import time
import cPickle as pickle
from operations import *

class MainPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/portfolio')


class PortfolioHandler(tornado.web.RequestHandler):
    def get(self):
        serilized_session = self.get_secure_cookie("Benzinga")
        if serilized_session:
            session = pickle.loads(serilized_session)
        else:
            session = {}
            session["cash"] = 100000.00
            session["portfolio"] = []
            session["cur_stock"] = None
            self.set_secure_cookie("Benzinga", pickle.dumps(session), expires=time.time()+900)
        symbol = self.get_argument('lookupKeyword', None)
        if not symbol:
            self.render('portfolio.html',
                        stock=session["cur_stock"],
                        err_notice=None,
                        suc_notice=None,
                        cash=session["cash"],
                        portfolio=session["portfolio"])
        else:
            session["cur_stock"] = get_stock_info(symbol)
            if "error" in session["cur_stock"]:
                err_notice = "Code {}: {}".format(
                    session["cur_stock"]["error"]["code"],
                    session["cur_stock"]["error"]["message"]
                )
                suc_notice = None
                session["cur_stock"] = None
            else:
                err_notice = None
                suc_notice = None

            self.set_secure_cookie("Benzinga", pickle.dumps(session), expires=time.time()+900)
            self.render('portfolio.html',
                        stock=session["cur_stock"],
                        err_notice=err_notice,
                        suc_notice=suc_notice,
                        cash=session["cash"],
                        portfolio=session["portfolio"])

    def post(self):
        serilized_session = self.get_secure_cookie("Benzinga")
        session = pickle.loads(serilized_session)
        buy = self.get_argument("buy", None)
        sell = self.get_argument("sell", None)
        quantity = self.get_argument("quantity")

        if not len(quantity):
            # if user didn't input the quantity
            err_notice = "Please input the amount of stocks you want to buy/sell. "
            self.render('portfolio.html',
                        stock=session["cur_stock"],
                        err_notice=err_notice,
                        suc_notice=None,
                        cash=session["cash"],
                        portfolio=session["portfolio"])

        if buy != None:
            # if buy button is clicked
            res, session, msg = buy_stock(session, int(quantity))
            err_notice = None
            suc_notice = None
            if res:
                self.set_secure_cookie("Benzinga", pickle.dumps(session), expires=time.time()+900)
                suc_notice = msg
            else:
                err_notice = msg
            self.render('portfolio.html',
                        stock=session["cur_stock"],
                        err_notice=err_notice,
                        suc_notice=suc_notice,
                        cash=session["cash"],
                        portfolio=session["portfolio"])
        elif sell != None:
            # if sell button is clicked
            res, session, msg = sell_stock(session, int(quantity))
            err_notice = None
            suc_notice = None
            if res:
                self.set_secure_cookie("Benzinga", pickle.dumps(session), expires=time.time()+900)
                suc_notice = msg
            else:
                err_notice = msg
            self.render('portfolio.html',
                        stock=session["cur_stock"],
                        err_notice=err_notice,
                        suc_notice=suc_notice,
                        cash=session["cash"],
                        portfolio=session["portfolio"])

