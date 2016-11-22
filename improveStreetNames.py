import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "ithacaRegion.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
state_route_re = re.compile(r'(State Route)', re.IGNORECASE)


#expected stree last name
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Landing", "Knoll", "Plaza","Circle", "East", "Highway",
            "Morris","Terrace","Way","West", "North"]

# correction mapping dict
mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Rd.": "Road",
            "Rd": "Road",
            "St.": "Street",
            "St": "Street",
            "Dr.": "Drive",
            "Dr": "Drive",
            "Drv": "Drive",
            "Ext": "Extension",
            "Ln":"Lane"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name) #Search for match with regular expression
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set) #Dictionary to store unexpected values
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_street_name(name, mapping):

    m = street_type_re.search(name) 
    if m:
        street_type = m.group()
        if street_type in mapping.keys(): #if correction in mapping dict
            name = street_type_re.sub(mapping[street_type],name)
        else: # correction for state and county roads
            street_str = name.split()
            if street_str[0]=='State' and len(street_str)==3:
                name = street_str[0] + ' Highway ' + street_str[2]
            elif street_str[0]=='County' and len(street_str)==3:
                name = street_str[0] + ' Road ' + street_str[2]

    return name

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
    
def test():
    st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_street_name(name, mapping)
            
            if name.split()[0] in ["State","County"]:
                print name, "=>", better_name
            


if __name__ == '__main__':
    test()