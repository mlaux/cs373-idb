from flask import Flask, Blueprint, render_template, request
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, select
from sqlalchemy import create_engine
from os import getenv
import json
from app.models import my_family, my_type, my_subtype, my_cards
import subprocess

STAGING_HOST = '45.55.237.77'
PRODUCTION_HOST = '104.236.244.154'

USERNAME = 'postgres'
PASSWORD = 'yugioh'
DB_NAME = 'its-time-to-duel'

engine = create_engine("postgresql://%s:%s@%s/%s" % (USERNAME, PASSWORD, STAGING_HOST, DB_NAME))

app = Flask(__name__)

conn = engine.connect()

#get cards from database
result2 = conn.execute(select([my_cards]))
result=[]
result_id=[]
result2=list(result2)
for row in result2:
    n=0
    row=list(row)
    result_id.append(row[0])
    for i in row:
        n+=1
        if i == None:
            row[n-1]=""
    result.append(row)

#get family from database
families = conn.execute(select([my_family]))
mylist=[]
for row in families:
    row=list(row)
    n=0
    for i in row:
        n += 1
        if i == None:
            row[n - 1] = ""
    mylist.append(row)

#get type from database
types = conn.execute(select([my_type]))
tlist=[]
for row in types:
    row=list(row)
    n=0
    for i in row:
        n += 1
        if i == None:
            row[n - 1] = ""
    tlist.append(row)

#get subtype from database
subtype = conn.execute(select([my_subtype]))
sublist=[]
for row in subtype:
    row=list(row)
    n=0
    for i in row:
        n += 1
        if i == None:
            row[n - 1] = ""
    sublist.append(row)

@app.route("/")
def home_page():
    return render_template('home.html')

@app.route("/about")
def about_page():
    return render_template('about.html')

@app.route("/card_types")
def card_types_page():
    return render_template('card_types.html', tlist=tlist)

@app.route("/cards")
def cards_page():
    return render_template('cards.html',result=result, result_id=result_id)

@app.route("/subtypes")
def subtypes_page():
    return render_template('subtypes.html', sublist=sublist)

@app.route("/families")
def families_page():
    return render_template('families.html',mylist=mylist)

@app.route("/cards/<card_id>")
def cardsTemplate_page(card_id):
    card_id = int(card_id)
    card_data = result[card_id-1]

    return render_template('cardsTemplate.html', card_data=card_data, result=result)

@app.route("/typeTemplate/<type_name>")
def typeTemplate_page(type_name):
    type_name = str(type_name)
    if(type_name=='monster'):
        type_data = tlist[1]
    elif(type_name=='spell'):
        type_data = tlist[2]
    else:
        type_data = tlist[7]

    # get cards of type from database
    cards_st = conn.execute(select([my_cards]).where(my_cards.c.cardType == type_name))
    s_cards = format_list(cards_st)

    return render_template('typeTemplate.html', type_data=type_data, tlist=s_cards)

@app.route("/familyTemplate/<family_id>")
def familyTemplate_page(family_id):
    family_id = int(family_id)
    family_data = mylist[family_id - 1]

    # get cards of family from database
    cards_st = conn.execute(select([my_cards]).where(my_cards.c.family_id == family_id))
    s_cards = format_list(cards_st)

    return render_template('familyTemplate.html', family_data=family_data, flist=s_cards)

@app.route("/subTypeTemplate/<subtype_id>")
def subTypeTemplate_page(subtype_id):
    subtype_id = int(subtype_id)
    sub_data = sublist[subtype_id - 1]

    # get cards of subtype from database
    cards_st = conn.execute(select([my_cards]).where(my_cards.c.subType_id==subtype_id))
    s_cards = format_list(cards_st)

    return render_template('subTypeTemplate.html',sub_data=sub_data, sublist=s_cards)

@app.route("/apiv1/cards")
def get_all_cards():
    return json.dumps(result)

@app.route("/apiv1/cards/<card_id>")
def get_one_card(card_id):
    return json.dumps(result[int(card_id)-1])

@app.route("/run_tests")
def run_test():
    t = subprocess.getoutput("pwd") + "/"
    return subprocess.getoutput("python3 " + t + "tests.py")

def format_list(cards_st):
    s_cards = []
    for row in cards_st:
        row = list(row)
        n = 0
        for i in row:
            n += 1
            if i == None:
                row[n - 1] = ""
        s_cards.append(row)

    return  s_cards
	
@app.route("/search/<table>")
def search(table):
    return json.dumps(table)

if __name__ == "__main__":
    app.run()
