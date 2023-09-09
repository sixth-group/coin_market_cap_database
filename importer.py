import ast
import pandas as pd

from models import Currency, CurrenciesHistory, Session, Tag


Session = Session()


class Importer:
    def __init__(self):
        self.currencies_history = pd.read_csv("year_details_update/full_data.csv")
        self.currency_df = pd.read_csv("detailed_coins.csv")

    def currency_importer(self):
        for i in self.currency_df.to_dict(orient="records"):
            tags = ast.literal_eval(i.pop("tags"))

            currency = Currency(**i)
            Session.add(currency)
            Session.commit()

            for tag in tags:
                existing_tag = Session.query(Tag).filter_by(tag=tag["tag"]).first()
                if existing_tag:
                    tag = existing_tag
                else:
                    tag = Tag(**tag)
                    Session.add(tag)
                    Session.commit()

                currency.tags.append(tag)

    def currencies_history_importer(self):
        currency_rows = Session.query(Currency).all()
        currency_name_id_mapping = {currency.Name: currency.id for currency in currency_rows}

        for currency_history in self.currencies_history.to_dict(orient='records'):
            currency_name = currency_history.pop('Name')
            currency_id = currency_name_id_mapping.get(currency_name)
            currency_history['currency_id'] = currency_id
            currency_history = CurrenciesHistory(**currency_history)
            Session.add(currency_history)
            Session.commit()


importer = Importer()
importer.currency_importer()
importer.currencies_history_importer()
