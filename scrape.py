# scrapes all the data from http://yugiohprices.com/api/ and inserts into
# our DB

import json
import urllib.request

from app import models

CARD_SETS_ENDPOINT = 'http://yugiohprices.com/api/card_sets'
SET_DATA_ENDPOINT = 'http://yugiohprices.com/api/set_data/%s'
CARD_DATA_ENDPOINT = 'http://yugiohprices.com/api/card_data/%s'
CARD_IMAGE_ENDPOINT = 'http://yugiohprices.com/api/card_image/%s'

def scrape_card(card_name):
    print('    ' + card_name)
    with urllib.request.urlopen(CARD_DATA_ENDPOINT % card_name) as fd:
        val = json.loads(fd.read().decode('utf-8'))
        print(val)

    with urllib.request.urlopen(CARD_IMAGE_ENDPOINT % card_name) as fd:
        out = open('%s.jpg' % card_name, 'wb')
        out.write(fd.read())
        out.close()

def scrape_set(set_name):
    print('SET: %s' % set_name)
    with urllib.request.urlopen(SET_DATA_ENDPOINT % set_name) as fd:
        val = json.loads(fd.read().decode('utf-8'))
        for card in val['data']['cards']:
            name = card['name']
            scrape_card(name)
            break

def scrape():
    with urllib.request.urlopen(CARD_SETS_ENDPOINT) as fd:
        all_sets = json.loads(fd.read().decode('utf-8'))
        for set_name in all_sets:
            scrape_set(set_name)
            break

if __name__ == '__main__':
    scrape()
