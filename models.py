from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    ForeignKey,
    TIMESTAMP,
    DateTime,
    BigInteger,
    Float,
    Table
)

DB_STRING = "postgresql://postgres:1234@localhost:5432/coinmarketcap_db"

db = create_engine(DB_STRING)
base = declarative_base()

Session = sessionmaker(bind=db)


class Currency(base):
    __tablename__ = "currency"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    Name = Column(String)
    Rank = Column(Integer)
    Symbol = Column(String, unique=True)
    MainLink = Column(String)
    HistoricalLink = Column(String)
    github_url = Column(String)

    tags = relationship('Tag', secondary='currency_tags')


class CurrenciesHistory(base):
    __tablename__ = "currencies_history"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    timeOpen = Column(DateTime)
    timeClose = Column(DateTime)
    timeHigh = Column(DateTime)
    timeLow = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    marketCap = Column(BigInteger)
    timestamp = Column(TIMESTAMP)
    currency_id = Column(Integer, ForeignKey("currency.id"))

    currency = relationship('Currency')


class Tag(base):
    __tablename__ = "tag"

    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    tag = Column(String, unique=True)
    url = Column(String)


currency_tags = Table(
    'currency_tags',
    base.metadata,
    Column('currency_id', Integer, ForeignKey('currency.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

if __name__ == "__main__":
    base.metadata.create_all(db)
