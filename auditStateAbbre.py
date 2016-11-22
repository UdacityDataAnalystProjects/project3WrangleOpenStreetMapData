# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint

OSMFILE = "ithacaRegion.osm"

expected = ["NY"]

def audit_tag_type(tag_Key_values, value):
    if value not in expected: # if not in expected dictionary
        tag_Key_values[value].add(value)
            

def audit(osmfile,tagKey):
    osm_file = open(osmfile, "r")
    tag_Key_values = defaultdict(set) #Dictionary to store unexpected values
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == tagKey:
                    #tag_Key_values[tagKey] = tag.attrib['v']
                    audit_tag_type(tag_Key_values, tag.attrib['v'])

    osm_file.close()
    return tag_Key_values
    


def test():    
    tag_Key_values = audit(OSMFILE,"addr:state")   
    pprint.pprint(dict(tag_Key_values))

           
if __name__ == '__main__':
    test()   
    