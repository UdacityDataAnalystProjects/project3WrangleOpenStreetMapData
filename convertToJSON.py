#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import improveStreetNames 
import improvePhoneKeyValue

#regex to find different kinds of attriute keys
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        if element.tag == "node":
            node['type']='node'
        else:
            node['type']='way'
        
        #formating code as instructed in the case study quiz
        #atrribute formating
#        print '----------------------'
        createdFlag = 0
        posFlag = 0
        for attr in element.attrib:
            if attr in CREATED:
                if not createdFlag:
                    createdFlag = 1
                    createdDict = {}
                    createdDict[attr] = element.attrib[attr]
                else:
                    createdDict[attr] = element.attrib[attr]
            elif attr in ['lon','lat']:
                if not posFlag:
                    pos = [0,0]
                    posFlag = 1
                    if attr=='lat':
                        pos[0] = float(element.attrib[attr])
                    else:
                        pos[1] = float(element.attrib[attr])
                else:
                    if attr=='lat':
                        pos[0] = float(element.attrib[attr])
                    else:
                        pos[1] = float(element.attrib[attr])
            else:
                node[attr] = element.attrib[attr]
                        
                
        if posFlag:
            node['pos']=pos
        if  createdFlag:
            node['created'] = createdDict    
        
        #tag formatiing
        addrFlag = 0
        for tag in element.iter("tag"):
            if problemchars.search(tag.attrib['k']):
                #ignore
                continue
            tag_attr = tag.attrib['k'].split(':') 
            if len(tag_attr)==1: #tags which do not contain : n thier attribute
                if tag.attrib['k'] == 'phone':
                    #imporve phone numbers using correct function of  improvePhoneKeyValue.py
                    tag.attrib['v'] = improvePhoneKeyValue.correctPhone(tag.attrib['v'])
                node[tag_attr[0]]=tag.attrib['v']
            elif len(tag_attr)==2: #tags with : in their attribute
                if tag_attr[0] == 'addr':
                    if improveStreetNames.is_street_name(tag):
                        #imporve street names with mapping dictionary
                        tag.attrib['v']  = improveStreetNames.update_street_name(tag.attrib['v'], improveStreetNames.mapping)
                    
                    if tag.attrib['k'] == "addr:state" and tag.attrib['v'] not in ["NY","PA"]:
                        tag.attrib['v'] = 'NY'

                    if not addrFlag: #for first tag with addr: attribute
                        addr={}
                        addrFlag=1
                        addr[tag_attr[1]]=tag.attrib['v']
                    else: #for restof tags with addr: attribute
                        addr[tag_attr[1]]=tag.attrib['v'] 
                else: #other tags with : in their attribute
                    node[tag_attr[0]+'_'+tag_attr[1]]=tag.attrib['v'] 
            elif len(tag_attr)==3:
                #ignore
                continue
        if addrFlag: # add to dict
            node["address"] = addr
            
        #specific way of formatting to list nodes as list in node_refs document
        ndFlag=0
        if element.tag == "way":
            nd = []
            for tag in element.iter("nd"):
                ndFlag=1
                nd.append(tag.attrib['ref'])
        
        if ndFlag:        
            node["node_refs"] = nd
                
#        print node
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # reads input osm file and writes json file
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

def test():
    # NOTE: if you are running this code on your computer, with a larger dataset, 
    # call the process_map procedure with pretty=False. The pretty=True option adds 
    # additional spaces to the output, making it significantly larger.
    data = process_map('fingerLakeBinghamtonRegion.osm', False)
#    pprint.pprint(data)


if __name__ == "__main__":
    test()