# scrapes all the data from http://yugiohprices.com/api/ and inserts into
# our DB

import json
import time
import urllib.request

from app import models
from app.models import engine, my_family, my_type, my_subtype, my_cards

CARD_SETS_ENDPOINT = 'http://yugiohprices.com/api/card_sets'
SET_DATA_ENDPOINT = 'http://yugiohprices.com/api/set_data/%s'
CARD_DATA_ENDPOINT = 'http://yugiohprices.com/api/card_data/%s'
CARD_IMAGE_ENDPOINT = 'http://yugiohprices.com/api/card_image/%s'

added_card_types = {}
added_card_subtypes = {}
added_card_families = {}

def scrape_card(card_name):
    print('    ' + card_name)
    with urllib.request.urlopen(CARD_DATA_ENDPOINT % card_name) as fd:
        val = json.loads(fd.read().decode('utf-8'))
        card_data = val['data']

        card_name = card_data['name']
        card_text = card_data['text']
        card_attack = card_data['atk']
        card_defense = card_data['def']
        card_level = card_data['level']
        card_price = 0
        card_url = ""

        card_type = card_data['card_type']

        if card_type == 'trap' or card_type == 'spell':
            card_subtype = card_data['property']
        else:
            card_subtype = card_data['type']

        card_family = card_data['family']

        # satisfy foreign key constraints first
        conn = engine.connect()

        if card_type not in added_card_types:
            ins = my_type.insert().values(cardType_name=card_type, cards_in_cardType=0,
                                                      url="", number_of_subtypes=0)
            res = conn.execute(ins)
            card_type_id = res.inserted_primary_key[0]
            added_card_types[card_type] = card_type_id
        else:
            card_type_id = added_card_types[card_type]

        if card_subtype not in added_card_subtypes:
            ins = my_subtype.insert().values(cardType_id=card_type_id,
                                                     subType_name=card_subtype,
                                                     cards_in_subType=0,
                                                     avg_price_subtype=0,
                                                     cardType=card_type)
            res = conn.execute(ins)
            subtype_id = res.inserted_primary_key[0]
            added_card_subtypes[card_subtype] = subtype_id
        else:
            subtype_id = added_card_subtypes[card_subtype]

        if card_family not in added_card_families:
            ins = my_family.insert().values(family_name=card_family, cards_in_family=0,
                                                    types_in_family=0, avg_attack=0, avg_defence=0)
            res = conn.execute(ins)
            family_id = res.inserted_primary_key[0]
            added_card_families[card_family] = family_id
        else:
            family_id = added_card_families[card_family]

        ins = my_cards.insert().values(subType_id=subtype_id, cardType_id=card_type_id,
                                               family_id=family_id, name=card_name, text=card_text,
                                               cardType=card_type, subType=card_subtype, 
                                               family=card_family, attack=card_attack,
                                               defense=card_defense, level=card_level,
                                               price=card_price, url=card_url)
        res = conn.execute(ins)

    with urllib.request.urlopen(CARD_IMAGE_ENDPOINT % card_name) as fd:
        out = open('app/static/card_images/%s.jpg' % card_name, 'wb')
        out.write(fd.read())
        out.close()

def scrape_set(set_name):
    print('SET: %s' % set_name)
    with urllib.request.urlopen(SET_DATA_ENDPOINT % set_name) as fd:
        val = json.loads(fd.read().decode('utf-8'))
        for card in val['data']['cards']:
            name = card['name']
            try:
                scrape_card(name)
            except:
                print('Error scraping %s' % name)

def scrape():
    with urllib.request.urlopen(CARD_SETS_ENDPOINT) as fd:
        all_sets = json.loads(fd.read().decode('utf-8'))
        for set_name in all_sets:
            scrape_set(set_name)

if __name__ == '__main__':
    scrape()
