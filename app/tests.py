# pylint: disable = bad-continuation
# pylint: disable = invalid-name
# pylint: disable = line-too-long
# pylint: disable = unused-wildcard-import
# pylint: disable = no-value-for-parameter
# pylint: disable = deprecated-method

from unittest import main, TestCase
from sqlalchemy import *
from sqlalchemy import create_engine
from models import my_cards_table, my_family_table, my_cardType_table, my_subtype_table

engine = create_engine('sqlite:///:memory:', echo=True)
metadata = MetaData()
conn = engine.connect()

def insert_dummy_family(my_family):
    ins = my_family.insert().values(family_id=3, family_name="", cards_in_family=1, types_in_family=1, avg_attack=1, avg_defence=1)
    conn.execute(ins)

def insert_dummy_cardType(my_cardType):
    ins = my_cardType.insert().values(cardType_id=2, cardType_name="", cards_in_cardType=1, url="", number_of_subtypes=1)
    conn.execute(ins)

def insert_dummy_subtype(my_subType):
    ins = my_subType.insert().values(subType_id=5, cardType_id=1, subType_name="", cards_in_subType=1, avg_price_subtype=1, cardType="")
    conn.execute(ins)

my_family = my_family_table(metadata, engine)
insert_dummy_family(my_family)
my_cardType = my_cardType_table(metadata, engine)
insert_dummy_cardType(my_cardType)
my_subtype = my_subtype_table(metadata, engine)
insert_dummy_subtype(my_subtype)
my_cards = my_cards_table(metadata, engine)

class TestModels(TestCase):
    """Test Cases for tables in models.py"""

    def test_my_cards_table(self):
        """test cases for my_cards_tables"""

        # testcase 1
        ins = my_cards.insert().values(subType_id=1, cardType_id=2, family_id=3, name="blak", text="", cardType="",
                                       subType="", family="", attack=1, defense=1, level=1, price=1, url="")
        conn.execute(ins)
        result2 = conn.execute(select([my_cards]))

        self.assertEquals([(1, 1, 2, 3, "blak","", "", "", "", 1, 1, 1, 1.0, "")], list(result2))


        ins = my_cards.insert().values(subType_id=2, cardType_id=3, family_id=4, name="Blue-Eyes White Dragon",
                                       text="legendary dragon", cardType="monster",
                                       subType="Dragon", family="light", attack=3000, defense=2500, level=8, price=1.9,
                                       url="http://static.api3.studiobebop.net/ygo_data/card_images/Blue_Eyes_White_Dragon.jpg")

        conn.execute(ins)
        result2 = conn.execute(select([my_cards]))

        self.assertEquals(
            [(1, 1, 2, 3, "blak","", "", "", "", 1, 1, 1, 1.0, ""),(2, 2, 3, 4, "Blue-Eyes White Dragon", "legendary dragon", "monster", "Dragon", "light", 3000,
              2500, 8, 1.9,
              "http://static.api3.studiobebop.net/ygo_data/card_images/Blue_Eyes_White_Dragon.jpg")],
            list(result2))


        ins = my_cards.insert().values(subType_id=2, cardType_id=3, name="", text="", cardType="", subType="")
        conn.execute(ins)
        result2 = conn.execute(select([my_cards]))

        self.assertEquals([(1, 1, 2, 3, "blak","", "", "", "", 1, 1, 1, 1.0, ""),(2, 2, 3, 4, "Blue-Eyes White Dragon", "legendary dragon", "monster", "Dragon", "light", 3000,
          2500, 8, 1.9,
          "http://static.api3.studiobebop.net/ygo_data/card_images/Blue_Eyes_White_Dragon.jpg"),(3, 2, 3, None, '', '', '', '', None, None, None, None, None, None)], list(result2))


    def test_my_subtype(self):
        """test cases for my_subtype_table"""

        # testcase1
        ins = my_subtype.insert().values(subType_id = 1, cardType_id=3, subType_name="", cards_in_subType="",
                                       avg_price_subtype=1.9, cardType="")
        conn.execute(ins)
        result2 = conn.execute(select([my_subtype]))

        self.assertEquals([(1, 3, "", "", 1.9, ""), (5, 1, '', 1, 1.0, '')], list(result2))

        # testcase2
        conn.execute(my_cards.delete())
        result2 = conn.execute(select([my_cards]))

        self.assertEquals([], list(result2))

        # testcase 3

        ins = my_cards.insert().values(subType_id=1, cardType_id=2, family_id=3, name="blak", text="", cardType="",
                                       subType="", family="", attack=1, defense=1, level=1, price=1, url="")
        conn.execute(ins)
        result2 = conn.execute(select([my_cards]))

        self.assertEquals([(1, 1, 2, 3, 'blak', '', '', '', '', 1, 1, 1, 1.0, '')], list(result2))

    def test_my_family(self):
        """test cases for my_family_table"""

        # testcase 1
        ins = my_family.insert().values(family_id = 1, family_name="", cards_in_family="", types_in_family="", avg_attack=1000,
                                       avg_defence=1100)
        conn.execute(ins)
        result2 = conn.execute(select([my_family]))

        self.assertEquals([(1, "", "", "", 1000.0, 1100.0), (3, '', 1, 1, 1.0, 1.0)], list(result2))

        # testcase 2
        conn.execute(my_family.delete())
        result2 = conn.execute(select([my_family]))
        insert_dummy_family(my_family)

        self.assertEquals([], list(result2))

        # testcase 3
        ins = my_family.insert().values(family_id = 1, family_name="light", cards_in_family="1504", types_in_family="42",
                                       avg_attack=2401.1,
                                       avg_defence=1942.3)
        conn.execute(ins)
        result2 = conn.execute(select([my_family]))

        self.assertEquals([(1, "light", 1504, 42, 2401.1, 1942.3), (3, '', 1, 1, 1.0, 1.0)], list(result2))

    def test_my_cardType(self):
        """test cases for my_cardType_tables"""

        # testcase 1
        ins = my_cardType.insert().values(cardType_id = 1, cardType_name="", cards_in_cardType="", url="", number_of_subtypes="")
        conn.execute(ins)
        result2 = conn.execute(select([my_cardType]))

        self.assertEquals([(1, "", "", "", ""), (2, '', 1, '', 1)], list(result2))

        # testcase 2
        conn.execute(my_cardType.delete())
        result2 = conn.execute(select([my_cardType]))
        insert_dummy_cardType(my_cardType)

        self.assertEquals([], list(result2))

        # testcase 3
        ins = my_cardType.insert().values(cardType_id = 1, cardType_name="Monster", cards_in_cardType=4556, number_of_subtypes=36)
        conn.execute(ins)
        result2 = conn.execute(select([my_cardType]))

        self.assertEquals([(1, "Monster", 4556, None, 36), (2, '', 1, '', 1)], list(result2))

# ----
# main
# ----

if __name__ == "__main__":
    main()
