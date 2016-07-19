from flask import Flask, Blueprint, render_template, request
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, select
from sqlalchemy import create_engine
from os import getenv
import json
from models import my_family, my_type, my_subtype, my_cards
import subprocess
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy import func
from sqlalchemy.sql import and_, or_

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

def bubble_sort():
    """ Implementation of bubble sort """
    temp=result
    for i in range(len(temp)):
        for j in range(len(temp) - 1 - i):
            if temp[j][0] > temp[j+1][0]:
                temp[j], temp[j + 1] = temp[j + 1], temp[j]
    return temp

result=bubble_sort()

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
tlist=[[1, 'monster', 0, '', 0], [2, 'monster', 742, '', 0], [3, 'spell', 188, '', 0], [4, 'monster', 0, '', 0], [5, 'spell', 0, '', 0], [6, 'monster', 0, '', 0], [7, 'spell', 0, '', 0], [8, 'trap', 150, '', 0]]

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

@app.route("/tunes")
def tunes_page():
    return render_template('tunes.html')

@app.route("/cards/<card_id>")
def cardsTemplate_page(card_id):
    card_id = int(card_id)
    card_data = result[card_id-1]

	#morphing jar id is 1082 but its in result[1080]
    if card_id == 1082:
        card_id=1080
    if card_data[9]=="":
        card_data[8]="N/A"
        card_data[9] = "N/A"
        card_data[10] = "N/A"
        card_data[11] = "N/A"
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

    #gets family name
    get_fam = conn.execute(select([my_family]).where(my_family.c.family_id == family_id))
    get_fam = format_list(get_fam)
    fam_name = get_fam[0][1]

    # get cards of family from database where family name is the same
    cards_st = conn.execute(select([my_cards]).where(my_cards.c.family == fam_name))
    s_cards = format_list(cards_st)

    return render_template('familyTemplate.html', family_data=family_data, flist=s_cards)

@app.route("/subTypeTemplate/<subtype_id>")
def subTypeTemplate_page(subtype_id):
    subtype_id = int(subtype_id)
    sub_data = sublist[subtype_id - 1]

    #gets subtype name
    get_subtype = conn.execute(select([my_subtype]).where(my_subtype.c.subType_id == subtype_id))
    get_subtype=format_list(get_subtype)
    subtype_name=get_subtype[0][2]

    # get cards of subtype from database where subtype name is the same
    cards_st = conn.execute(select([my_cards]).where(my_cards.c.subType==subtype_name))
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
    t = "/var/www/cs373-idb/app/tests.py"
    return subprocess.getoutput("python3 " + t)

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

@app.route("/search")
def search():
    search_res= request.args.get('query')
    search_res=search_res.replace("'","")
    search_res=search_res.replace("!","")
    search_res=search_res.replace("(","")
    search_res=search_res.replace(")","")
    search_res=search_res.replace(":","")
    temp_val = search_res.split(" ")
    search_list=[]
    for search in temp_val:
        if search.isdigit():
            search_data = conn.execute(select([my_cards]).where(or_(
                func.to_tsvector('english', my_cards.c.text).match(search, postgresql_regconfig='english'),
                func.to_tsvector('english', my_cards.c.name).match(search, postgresql_regconfig='english'),
                func.to_tsvector('english', my_cards.c.cardType).match(search, postgresql_regconfig='english'),
                func.to_tsvector('english', my_cards.c.subType).match(search, postgresql_regconfig='english'),
                func.to_tsvector('english', my_cards.c.family).match(search, postgresql_regconfig='english'),
                my_cards.c.attack==int(search),
                my_cards.c.defense==int(search))))
        else:
            search_data = conn.execute(select([my_cards]).where(or_(
                func.to_tsvector('english', my_cards.c.text).match(search, postgresql_regconfig='english'),
                func.to_tsvector('english', my_cards.c.name).match(search, postgresql_regconfig='english'),
                func.to_tsvector('english', my_cards.c.cardType).match(search, postgresql_regconfig='english'),
                func.to_tsvector('english', my_cards.c.subType).match(search, postgresql_regconfig='english'),
                func.to_tsvector('english', my_cards.c.family).match(search, postgresql_regconfig='english'))))

        search_list+=format_list(search_data)
    return render_template('searchTemplate.html',search_data=search_list)

if __name__ == "__main__":
    app.run()
