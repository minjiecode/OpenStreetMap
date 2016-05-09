#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
FILE = "beijing_china.osm"

#clean/reformat the phone value
def clean_phone(number):
	numberlist = re.findall("\d",number)
	new_number = "".join(numberlist)
	if len(new_number) == 8:
		new_number = "010" + new_number
	new_number = new_number[-11:]
	if new_number.startswith('1'):
		new_number = "+86-" + new_number
	else:
		new_number = "+86-10-" + new_number[-8:]
	return new_number


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # Geo Data
        pos = [0,0]
        has_pos = False
        created = {}
        node['type'] = element.tag
        for key,value in element.attrib.iteritems():
            if key in CREATED:
                created[key] = value
            elif key in ['lat','lon']:
                has_pos = True
                if key == 'lat':
                    pos[0] = float(value)
                else:
                    pos[1] = float(value)
            else:
                node[key] = value
        address = {}
        has_address = False
        for tag in element.iter('tag'):
            if problemchars.search(tag.get('k')) is not None:
                continue
            elif 'addr:' in tag.get('k'):
                has_address = True
                addr_list = tag.get('k').split(":")
                address["".join(addr_list[1:])] = tag.get('v')
            elif 'phone' in tag.get('k'):
            	# clean the phone data
            	node[tag.get('k')] = clean_phone(tag.get('v'))
            else:
                node[tag.get('k')] = tag.get('v')
        node_refs = []
        has_node_refs = False
        for tag in element.iter('nd'):
            has_node_refs = True
            node_refs.append(tag.get('ref'))
        if has_node_refs:
            node['node_refs'] = node_refs
        node['created'] = created
        if has_pos:
            node['pos'] = pos
        if has_address:
            node['address'] = address
        return node
    else:
        return None



def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


if __name__ == "__main__":
    process_map(FILE)

