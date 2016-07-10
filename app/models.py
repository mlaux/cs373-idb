# pylint: disable = unused-wildcard-import
# pylint: disable = bad-continuation
# pylint: disable = invalid-name

'''Creates tables for each of the 4 models with its attributes'''

from sqlalchemy import *
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True)
metadata = MetaData()

def get_cards_table():
    '''This function creates and returns table for cards'''
    my_cards = Table('cards', metadata,
        Column('card_id', Integer, primary_key=True),
        Column('subType_id', Integer),
        Column('cardType_id', Integer),
        Column('family_id', Integer, nullable=True),
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

def get_subtype_table():
    '''This function creates and returns table for card subType'''
    my_subtype = Table("subType", metadata,
        Column('subType_id', Integer, primary_key=True),
        Column('cardType_id', Integer),
        Column('subType_name', String(100)),
        Column('cards_in_subType', Integer),
        Column('avg_price_subtype', Float, nullable=True),
        Column('cardType', String(100)),)

    my_subtype.create(engine, checkfirst=True)
    return my_subtype

def get_family_table():
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

def get_cardType_table():
    '''This function creates and returns table for cardType'''
    my_cardType = Table("cardType", metadata,
        Column('cardType_id', Integer, primary_key=True),
        Column('cardType_name', String(100)),
        Column('cards_in_cardType', Integer),
        Column('url', String(100), nullable=True),
        Column('number_of_subtypes', Integer),)

    my_cardType.create(engine, checkfirst=True)
    return my_cardType

'''
conn = engine.connect()
my_cards=get_cards_table()
ins = my_cards.insert().values(subType_id=2, cardType_id=3, family_id=4, name="", text="", cardType="",
                               subType="", family="", attack="", defense="", level="", price=1.9, url="")
result1= conn.execute(ins)
result2= conn.execute(select([my_cards]))

print(list(result2))
'''

