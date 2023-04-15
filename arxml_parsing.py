import sys, os
current_path = os.getcwd()

import json
from lxml import etree
import glob

etree_namespace = {'ar': 'http://autosar.org/schema/r4.0'}
etree.register_namespace('ar', 'http://autosar.org/schema/r4.0')

def get_files_by_extension(root_path, extension):
    pattern = root_path + '/**/*.' + extension
    matches = glob.glob(pattern, recursive=True)
    matches = [f.replace('\\', '/') for f in matches]
    return matches


def arxmlToJsonParsing(arxml_file_path, json_file_path):
    xml_tree = etree.parse(arxml_file_path)
    xml_element = xml_tree.getroot()
    json_object = json.loads('{}')
    genJsonFromXml(xml_element, json_object)
    exportJsonObjectToFile(json_object, json_file_path)
    
    
def genJsonFromXml(xml_ele, json_obj, json_object_path = '', outter_element_tag = ''):
    if (getElementTagWithoutNameSpace(xml_ele) == "AUTOSAR"):
        json_obj["xmlns"] = xml_ele.nsmap.get(None)
        json_obj["xsi"] = xml_ele.nsmap.get('xsi')
        json_obj["schemaLocation"] = xml_ele.attrib.get('{%s}schemaLocation' % json_obj["xsi"]) 
    if ((len(xml_ele) > 0)): 
        short_name = getShortName(xml_ele)
        if (short_name != None):
            json_object_path = json_object_path + "/" + short_name
            json_obj[short_name] = {}
            json_obj = json_obj[short_name]
            json_obj["object_path"] = json_object_path
            json_obj["object_type"] = getElementTagWithoutNameSpace(xml_ele)
            json_obj["outter_element_tag"] = outter_element_tag
        for child_ele in xml_ele:
            backup_outter_element_tag = outter_element_tag
            if (short_name != None):
                outter_element_tag = ""
            elif (getElementTagWithoutNameSpace(xml_ele) != "AUTOSAR"):
                    outter_element_tag = outter_element_tag + "/" + getElementTagWithoutNameSpace(xml_ele)
            genJsonFromXml(child_ele, json_obj, json_object_path, outter_element_tag)
            outter_element_tag = backup_outter_element_tag
    else:
        if (getElementTagWithoutNameSpace(xml_ele) != "SHORT-NAME"):
            json_obj[getElementTagWithoutNameSpace(xml_ele)] = {}
            json_obj = json_obj[getElementTagWithoutNameSpace(xml_ele)]
            json_obj["value"] = xml_ele.text
            json_obj["object_type"] = getElementTagWithoutNameSpace(xml_ele)
            json_obj["outter_element_tag"] = outter_element_tag
            addAttributesToObject(xml_ele, json_obj)
    
    
def getElementTagWithoutNameSpace(element):
    return element.tag[element.tag.find('}')+1:] if '}' in element.tag else element.tag


def getShortName(xml_ele):
    short_name_list = xml_ele.xpath('ar:SHORT-NAME', namespaces = etree_namespace)
    if not(len(short_name_list) > 0):
        return None
    else:
        return short_name_list[0].text
    
    
def addAttributesToObject(xml_ele, json_obj):
    if xml_ele.attrib.items() != []:
        json_obj["attributes"] = []
        for attr_key, attr_value in xml_ele.attrib.items():
            json_obj["attributes"].append({attr_key: attr_value})
            

def exportJsonObjectToFile(json_object, file_path):
    json_string = json.dumps(json_object, indent=4)
    with open(file_path, 'w') as f:
        f.write(json_string)
    f.close()
    

def mergeJsonData(base_json_obj, json_obj):
    if isinstance(json_obj, dict):
        for obj in json_obj.items():
            obj_key = obj[0]
            obj_value = obj[1]
            if obj_key not in base_json_obj:
                base_json_obj[obj_key] = obj_value
            else:
                mergeJsonData(base_json_obj[obj_key], obj_value)  


def fullArxmlToJsonParsing(arxml_path, json_path):
    arxml_files = get_files_by_extension(arxml_path, 'arxml')
    for arxml_file in arxml_files:
        # create json file name base on arxml file base name
        json_file_name = os.path.basename(arxml_file).split('.')[0] + ".json"
        json_file_path = json_path + "/" + json_file_name
        arxmlToJsonParsing(arxml_file, json_file_path)
    root_json_obj = {}
    json_files = get_files_by_extension(json_path, 'json')
    for json_file in json_files:
        json_obj = None
        with open(json_file, 'r') as f:
            json_obj = json.load(f)
        mergeJsonData(root_json_obj, json_obj)
    exportJsonObjectToFile(root_json_obj, json_path + "/root.json")


if __name__ == "__main__":
    arxml_path = current_path + "/arxml"
    json_path = current_path + "/json"

    fullArxmlToJsonParsing(arxml_path, json_path)