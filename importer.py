from models import (
    Currency,
    Session,
    Tag,
    Market,
    Trade,
    Date,
    CurrencyDate,
    Time,
    Price,
)

import pandas as pd

Session = Session()


class Importer:
    def __init__(self):
        self.full_data = pd.read_csv("year_details_update/full_data.csv")
        self.currency_df = pd.read_csv("detailed_coins.csv")

    def curency_importer(self):
        for i in self.currency_df.to_dict(orient="records"):
            i.pop("tags")
            currency = Currency(**i)
            Session.add(currency)
            currency_date = CurrencyDate()
            currency_date.currency_id = currency.id
            Session.add(currency_date)
            Session.commit()

    # def tag_importer(self):
    #     for i in self.currency_df.to_dict(orient="records"):
    #         i = i.pop("tags")
    #         res = i_list.strip('][').split(', ')
    #         print(i)
    #         for j in i:
    #             tag = Tag(**j)
    #             Session.add(tag)
    #             Session.commit()

    def date_importer(self):
        self.full_data["timeOpen"] = pd.to_datetime(
            self.full_data["timeOpen"]
        ).dt.date.unique()
        for i in self.full_data["timeOpen"].to_dict(orient="records"):
            date = Date(**i)
            Session.add(date)
            currency_date = CurrencyDate()
            currency_date.date_id = date.id
            Session.add(currency_date)
            Session.commit()

    def currency_date_importer(self):
        for i in self.full_data.to_dict(orient="records"):
            i = self.full_data["marketCap"]
            market = Market(**i)
            Session.add(market)
            Session.commit()

    def market_importer(self):
        for i in self.full_data.to_dict(orient="records"):
            i = self.full_data["marketCap"]
            market = Market(**i)
            Session.add(market)
            Session.commit()

    def trade_importer(self):
        for i in self.full_data.to_dict(orient="records"):
            i = self.full_data["volume"]
            trade = Trade(**i)
            Session.add(trade)
            Session.commit()

    def price_importer(self):
        for i in self.full_data.to_dict(orient="records"):
            i = self.full_data["open", "close", "high", "low"]
            price = Price(**i)
            Session.add(price)
            Session.commit()

    def time_importer(self):
        for i in self.full_data.to_dict(orient="records"):
            i = self.full_data["timeOpen", "timeClose", "timeHigh", "timeLow"]
            time = Time(**i)
            Session.add(time)
            Session.commit()


importer = Importer()

importer.curency_importer()
importer.date_importer()
importer.currency_date_importer()
importer.market_importer()
importer.trade_importer()
importer.time_importer()
importer.price_importer()
