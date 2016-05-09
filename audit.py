"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import unicodedata as ud

OSMFILE = "beijing_china.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Alley", "Hutong","Dajie", 'JingAnLi','LangJiaYuan']


# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Rd": "Road",
            "Rd.": "Road",
            "road": "Road",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "ave.": "Avenue"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def audit_chinese_keys(chinese_keys, key, value):
    chinese_keys[key].add(value)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_chinese(elem):
    key = elem.attrib['k']
    for n in key:
        try:
            letter_name = ud.name(unicode(n,'utf-8'))
            if letter_name.startswith('CJK UNIFIED'):
                return True
        except UnicodeDecodeError:
            return True
        except TypeError:
            return True
    return False

def is_phone(elem):
    return (elem.attrib['k'] == "phone")

def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def is_capacity(elem):
    return (elem.attrib['k'] == "capacity")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    chinese_keys = defaultdict(set)
    phone_numbers = []
    post_code = []
    capacity_data = []
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                # # audit chinese characters as keys
                # if is_chinese(tag):
                #     audit_chinese_keys(chinese_keys, tag.attrib['k'], tag.attrib['v'])
                # #audit street name
                # if is_street_name(tag):
                #     audit_street_type(street_types, tag.attrib['v'])
                # # audit phone number
                # if is_phone(tag):
                #     phone_numbers.append(tag.attrib['v'])
                # # audit postcode
                # if is_postcode(tag):
                #     post_code.append(tag.attrib['v'])
                if is_capacity(tag):
                    capacity_data.append(tag.attrib['v'])

    osm_file.close()
    # return street_types, chinese_keys, phone_numbers,post_code
    return capacity_data


def test():
    # st_types,chinese_keys, phone_numbers, post_code = audit(OSMFILE)
    capacity = audit(OSMFILE)
    # pprint.pprint(dict(st_types))
    # pprint.pprint(dict(chinese_keys))
    print capacity


if __name__ == '__main__':
    test()
