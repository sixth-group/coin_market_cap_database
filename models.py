from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    create_engine,
    Column,
    Boolean,
    String,
    DateTime,
    Integer,
    ForeignKey,
)

DB_STRING = "postgresql://postgres:1234@localhost:5432/coinmarketcap_db"

db = create_engine(DB_STRING)
base = declarative_base()

Session = sessionmaker(bind=db)


class Currency(base):
    __tablename__ = "currency"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    name = Column(String)
    symbol = Column(String, unique=True)
    main_link = Column(String)
    historical_link = Column(String)
    github_link = Column(String)

    # Relationships
    currency_date = relationship("CurrencyDate")
    tag = relationship("Tag")


class Date(base):
    __tablename__ = "date"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    timestamp = Column(DateTime)

    # Relationships
    currency_date = relationship("CurrencyDate")


class Market(base):
    __tablename__ = "market"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    market_cap = Column(Integer)
    currency_date = Column(Integer, ForeignKey("currency_date.id"))


class Trade(base):
    __tablename__ = "trade"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    volume = Column(Integer)
    currency_date = Column(Integer, ForeignKey("currency_date.id"))


class Price(base):
    __tablename__ = "price"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    open_price = Column(Integer)
    close_price = Column(Integer)
    high_price = Column(Integer)
    low_price = Column(Integer)
    currency_date = Column(Integer, ForeignKey("currency_date.id"))


class Time(base):
    __tablename__ = "time"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    open_time = Column(Integer)
    close_time = Column(Integer)
    high_time = Column(Integer)
    low_time = Column(Integer)
    currency_date = Column(Integer, ForeignKey("currency_date.id"))


class Tag(base):
    __tablename__ = "tag"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    tag = Column(String)
    currency = Column(Integer, ForeignKey("currency.id"))


class CurrencyDate(base):
    __tablename__ = "currency_date"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)

    # Relationships:
    currency = Column(Integer, ForeignKey("currency.id"))
    date = Column(Integer, ForeignKey("date.id"))

    market = relationship("Market")
    trade = relationship("Trade")
    price = relationship("Price")
    time = relationship("Time")


if __name__ == "__main__":
    base.metadata.create_all(db)
