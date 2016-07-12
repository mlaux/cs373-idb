# pylint: disable = unused-wildcard-import
# pylint: disable = bad-continuation
# pylint: disable = invalid-name

'''Creates tables for each of the 4 models with its attributes'''

from os import getenv
from sqlalchemy import *
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

STAGING_HOST = '45.55.237.77'
PRODUCTION_HOST = '104.236.244.154'

USERNAME = 'postgres'
PASSWORD = 'yugioh'
DB_NAME = 'its-time-to-duel'

#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine("postgresql://%s:%s@%s/%s" % (USERNAME, PASSWORD, STAGING_HOST, DB_NAME))
metadata = MetaData()

def my_cards_table():
    '''This function creates and returns table for cards'''
    my_cards = Table('cards', metadata,
        Column('card_id', Integer, primary_key=True),
        Column('subType_id', Integer, ForeignKey('subType.subType_id')),
        Column('cardType_id', Integer, ForeignKey('cardType.cardType_id')),
        Column('family_id', Integer, ForeignKey('family.family_id'),nullable=True),
        Column('name', String(100)),
        Column('text', String(1000)),
        Column('cardType', String(100)),
        Column('subType', String(100)),
        Column('family', String(100), nullable=True),
        Column('attack', Integer, nullable=True),
        Column('defense', Integer, nullable=True),
        Column('level', Integer, nullable=True),
        Column('price', Float, nullable=True),
        Column('url', String(100), nullable=True),)

    my_cards.create(engine, checkfirst=True)
    return my_cards

def my_subtype_table():
    '''This function creates and returns table for card subType'''
    my_subtype = Table("subType", metadata,
        Column('subType_id', Integer, primary_key=True),
        Column('cardType_id', Integer, ForeignKey('cardType.cardType_id')),
        Column('subType_name', String(100)),
        Column('cards_in_subType', Integer),
        Column('avg_price_subtype', Float, nullable=True),
        Column('cardType', String(100)),)

    my_subtype.create(engine, checkfirst=True)
    return my_subtype

def my_family_table():
    '''This function creates and returns table for card family'''
    my_family = Table("family", metadata,
        Column('family_id', Integer, primary_key=True),
        Column('family_name', String(100)),
        Column('cards_in_family', Integer),
        Column('types_in_family', Integer),
        Column('avg_attack', Float),
        Column('avg_defence', Float),)

    my_family.create(engine, checkfirst=True)
    return my_family

def my_cardType_table():
    '''This function creates and returns table for cardType'''
    my_cardType = Table("cardType", metadata,
        Column('cardType_id', Integer, primary_key=True),
        Column('cardType_name', String(100)),
        Column('cards_in_cardType', Integer),
        Column('url', String(100), nullable=True),
        Column('number_of_subtypes', Integer),)

    my_cardType.create(engine, checkfirst=True)
    return my_cardType

my_family=my_family_table()
my_type=my_cardType_table()
my_subtype=my_subtype_table()
my_cards=my_cards_table()
'''
conn = engine.connect()

ins = my_type.insert().values(cardType_id=2, cardType_name="Effect Monster", cards_in_cardType=2220, url="", number_of_subtypes=11)
conn.execute(ins)
ins = my_subtype.insert().values(subType_id=3, cardType_id=2,subType_name="Fiend/Effect", cards_in_subType=112, avg_price_subtype=.9, cardType="Effect Monster")
conn.execute(ins)
ins = my_family.insert().values(family_id=2, family_name="Dark", cards_in_family=1130, types_in_family=23, avg_attack=2100,
                              avg_defence=3000)
conn.execute(ins)
ins = my_cards.insert().values(card_id=3, subType_id=3, cardType_id=2, family_id=2, name="Kuriboh", text="Its Kuriboh", cardType="Effect Monster",
                               subType="Fiend/Effect", family="Dark", attack=1000, defense=1000, level=3, price=.7, url="")
conn.execute(ins)
result2= conn.execute(select([my_cards]))

'''
