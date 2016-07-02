from flask import Flask
from sqlalchemy import *
from sqlalchemy import schema


#db= create_engine('')

#db.echo = False  # Try changing this to True and see what happens

metadata = schema.MetaData()

my_cards = Table('cards', metadata,
    Column('card_id', Integer, primary_key=True),
    Column('subType_id', Integer),
    Column('cardType_id', Integer),
    Column('family_id', Integer),
    Column('name', String(100)),
    Column('text', String(1000)),
    Column('cardType', String(100)),
    Column('subType', String(100)),
    Column('family', String(100)),
    Column('attack', String(100)),
    Column('defense', String(100)),
    Column('level', Integer),
    Column('url', String(100)),)

my_cards.create()

my_subtype = Table("subType", metadata,
    Column('subType_id', Integer, primary_key=True),
    Column('cardType_id', Integer),
    Column('subType_name', String(100)),
    Column('cards_in_subType', Integer),
    Column(' ', Integer),
    Column('cardType', String(100)),)

my_subtype.create()

my_family = Table("family", metadata,
    Column('family_id', Integer, primary_key=True),
    Column('family_name', String(100)),
    Column('cards_in_family', Integer),
    Column('types_in_family', Integer),
    Column('avg_attack', Integer),
    Column('avg_defence', Integer),)

my_family.create()

my_cardType = Table("cardType", metadata,
    Column('cardType_id', Integer, primary_key=True),
    Column('cardType_name', String(100)),
    Column('cards_in_cardType', Integer),
    Column('url', String(100)),
    Column('number_of_subtypes', Integer),)

my_cardType.create()

