# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "ithacaRegion.osm"

phone_re = re.compile(r'((\(\d{3}\) ?)|(\d{3}-))?\d{3}-\d{4}')

def audit_tag_type(tag_Key_values, value):
    m = phone_re.search(value) #Search for match with regular expression
        
    if not m: #if not a match then add the key value in dictionary
        tag_Key_values['Phone'].add(value)
   
        


def audit(osmfile,tagKey):
    osm_file = open(osmfile, "r")
    tag_Key_values = defaultdict(set) #Dictionary to store unexpected values
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if tag.attrib['k'] == tagKey:
                    #tag_Key_values[tagKey] = tag.attrib['v']
                    audit_tag_type(tag_Key_values, (tag.attrib['v']))

    osm_file.close()
    return tag_Key_values
    
def correctPhone(val):
    m = phone_re.search(val) #Search for match with regular expression
    if not m: #if val is not a match with valid format
        splitVal = val.split()
        if len(splitVal) == 4: # do if phoen number has ISD code
            return (splitVal[1]+'-'+splitVal[2]+'-'+splitVal[3])
        elif len(splitVal) == 3: # if phoen number does not have ISD code but but numbers are separated by some delimiter
            return (splitVal[0]+'-'+splitVal[1]+'-'+splitVal[2])
        elif len(splitVal) == 1: # if disits do not have any other kinds of delimiter
            phVal = splitVal[0]
            if len(phVal)==12: # 
                if '.' in phVal:
                    splitPhVal = phVal.split('.')
                    return (splitPhVal[0]+'-'+splitPhVal[1]+'-'+splitPhVal[2])
                else:
                    return (phVal[2:5]+'-'+phVal[5:8]+'-'+phVal[8:12])
            elif len(phVal)==10: # if there are no delimiter
                return (phVal[0:3]+'-'+phVal[3:6]+'-'+phVal[6:10])
            else:
                return('') #return empty if invalid
        else:
            return('') #return empty if invalid
    else:
        return val

def test():    
    tag_Key_values = audit(OSMFILE,"phone")   
    pprint.pprint(dict(tag_Key_values))
    
    for val in tag_Key_values['Phone']:
        print val, "=>", correctPhone(val)
#    return
#    correct phone
#==============================================================================
#     for val in tag_Key_values['Phone']:
#         splitVal = val.split()
#         if len(splitVal) == 4:
#             tag_Key_values[val].add(splitVal[1]+'-'+splitVal[2]+'-'+splitVal[3])
#         elif len(splitVal) == 3:
#             tag_Key_values[val].add(splitVal[0]+'-'+splitVal[1]+'-'+splitVal[2])
#         elif len(splitVal) == 1:
#             phVal = splitVal[0]
#             if len(phVal)==12:
#                 if '.' in phVal:
#                     splitPhVal = phVal.split('.')
#                     tag_Key_values[val].add(splitPhVal[0]+'-'+splitPhVal[1]+'-'+splitPhVal[2])
#                 else:
#                     tag_Key_values[val].add(phVal[2:5]+'-'+phVal[5:8]+'-'+phVal[8:12])
#             elif len(phVal)==10:
#                 tag_Key_values[val].add(phVal[0:3]+'-'+phVal[3:6]+'-'+phVal[6:10])
#             else:
#                 tag_Key_values[val].add('Wrong')
#         else:
#             tag_Key_values[val].add('Wrong')
#==============================================================================
                
           
if __name__ == '__main__':
    test()   
    