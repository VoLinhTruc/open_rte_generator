import sys, os
import json
from lxml import etree
import glob
import shutil
import copy


current_path = os.getcwd()

etree_namespace = {'ar': 'http://autosar.org/schema/r4.0'}
etree.register_namespace('ar', 'http://autosar.org/schema/r4.0')

GEN_SWC_INCLUDE_FILE_PATH = "output/_gen/swb/includes/rtegen/swc/"
GEN_SWC_SOURCE_FILE_PATH = "output/_gen/swb/src_files/rtegen/swc/"
APPL_SWC_PATH = "application"
ARXML_INPUT_PATH = "input/arxml"
OUTPUT_JSON_PATH = "output\json"
OUTPUT_JSON_EXTRACT_PATH = "output\json\object_extract"
RTOS_STACK_DEPTH = 5000

rte_port_api = {
    "Rte_Send": "Rte_Send",
    "Rte_Write": "Rte_Write",
    "Rte_Switch": "Rte_Switch",
    "Rte_Invalidate": "Rte_Invalidate",
    "Rte_Feedback": "Rte_Feedback",
    "Rte_SwitchAck": "Rte_Send",
    "Rte_Read": "Rte_Read",
    "Rte_DRead": "Rte_DRead",
    "Rte_Receive": "Rte_Receive",
    "Rte_Call": "Rte_Call",
    "Rte_Result": "Rte_Result",
    "Rte_Prm": "Rte_Prm",
    "Rte_Mode": "Rte_Mode",
    "Rte_Trigger": "Rte_Trigger",
    "Rte_IsUpdated": "Rte_IsUpdated"
}

    
data_point_api = {
    "port_api_type": "port_api_type",
    "port_api_header": "port_api_header",
    "port_api_p": "port_api_p",
    "port_api_o": "port_api_o",
    "port_api_arg_type": "port_api_arg_type",
    "port_api_arg_value": "port_api_arg_value"
}

receive_data_point_by_value_api_list = []
send_data_point_by_value_api_list = []
connector_list = []
event_to_task_mapping_list = []
task_info_list = []



latest_def_ref = ""



def writeToLogFile(content):
    with open('std_out.json', 'a') as f:
        f.write("%s\n" % content)

def getFilesByExtension(root_path, extension):
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
    global latest_def_ref
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

            # additional process to get connector correctly
            if("CONTEXT-COMPONENT-REF" in json_obj):
                if (json_obj["CONTEXT-COMPONENT-REF"]["outter_element_tag"] == "/PROVIDER-IREF"):
                    json_obj["CONTEXT-COMPONENT-REF-PROVIDER"] = json_obj["CONTEXT-COMPONENT-REF"]
                    del json_obj["CONTEXT-COMPONENT-REF"]
                elif (json_obj["CONTEXT-COMPONENT-REF"]["outter_element_tag"] == "/REQUESTER-IREF"):
                    json_obj["CONTEXT-COMPONENT-REF-REQUESTER"] = json_obj["CONTEXT-COMPONENT-REF"]
                    del json_obj["CONTEXT-COMPONENT-REF"]
                    
            genJsonFromXml(child_ele, json_obj, json_object_path, outter_element_tag)
            outter_element_tag = backup_outter_element_tag
    else:
        if (getElementTagWithoutNameSpace(xml_ele) != "SHORT-NAME"):
            # Additional process to get DEFINITION-REF and VALUE corresponse to the cofiguration correctly   
            additional_element_tag = ""
            if getElementTagWithoutNameSpace(xml_ele) == "DEFINITION-REF":
                additional_element_tag = "-" + xml_ele.text.split("/")[-1]
                latest_def_ref = xml_ele.text.split("/")[-1]
            if getElementTagWithoutNameSpace(xml_ele) == "VALUE-REF":
                additional_element_tag = "-" + latest_def_ref
            if getElementTagWithoutNameSpace(xml_ele) == "VALUE":
                additional_element_tag = "-" + latest_def_ref
                
            json_obj[getElementTagWithoutNameSpace(xml_ele) + additional_element_tag] = {}
            json_obj = json_obj[getElementTagWithoutNameSpace(xml_ele) + additional_element_tag]
            json_obj["value"] = xml_ele.text
            json_obj["object_type"] = getElementTagWithoutNameSpace(xml_ele)
            json_obj["outter_element_tag"] = outter_element_tag
            addAttributesToObject(xml_ele, json_obj)
    
    
def getElementTagWithoutNameSpace(element):
    return element.tag[element.tag.find('}')+1:] if '}' in element.tag else element.tag
    
    
def getJsonObjectFromRefPath(root_obj, path):
    splited_path = path.split("/")
    for i in range(1, len(splited_path), 1):
        if (splited_path[i] in root_obj):
            root_obj = root_obj[splited_path[i]]
        else:
            root_obj = None
            break
    return root_obj


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


def fullArxmlToJsonParsing(input_arxml_path, output_json_path):
    arxml_files = getFilesByExtension(input_arxml_path, 'arxml')
    for arxml_file in arxml_files:
        # create json file name base on arxml file base name
        json_file_name = os.path.basename(arxml_file).split('.')[0] + ".json"
        json_file_path = output_json_path + "/" + json_file_name
        if not os.path.exists(output_json_path):
            os.makedirs(output_json_path)
        arxmlToJsonParsing(arxml_file, json_file_path)
    if os.path.exists(output_json_path + "/root.json"):
        os.remove(output_json_path + "/root.json")
    root_json_obj = {}
    json_files = getFilesByExtension(output_json_path, 'json')
    for json_file in json_files:
        json_obj = None
        with open(json_file, 'r') as f:
            json_obj = json.load(f)
        mergeJsonData(root_json_obj, json_obj)
        
    if not os.path.exists(output_json_path):
        os.makedirs(output_json_path)
    exportJsonObjectToFile(root_json_obj, output_json_path + "/root.json")

# -------------------------------------------------------------------------------

def getObjName(obj):
    object_name = ""
    if "object_path" in obj:
        splitted_path = obj["object_path"].split('/')
        object_name = splitted_path[len(splitted_path) - 1]
    return object_name

def getObjNameFromPath(path):
    object_name = ""
    splitted_path = path.split('/')
    object_name = splitted_path[len(splitted_path) - 1]
    return object_name
    

def getObjectByType(obj, key, objects={}):
    if isinstance(obj, dict):
        if "object_type" in obj:
            if obj["object_type"] == key:
                objects[getObjName(obj)] = obj
        for value in obj.values():
            getObjectByType(value, key, objects)
    elif isinstance(obj, list):
        for item in obj:
            getObjectByType(item, key, objects)
            
    return objects

def getSWComponents(obj):
    x = getObjectByType(obj, "APPLICATION-SW-COMPONENT-TYPE", {})
    return x

def getClientServerInterfaces(obj):
    return getObjectByType(obj, "CLIENT-SERVER-INTERFACE", {})

def getSenderReceiverInterfaces(obj):
    return getObjectByType(obj, "SENDER-RECEIVER-INTERFACE", {})

def getInterfacesMappingSets(obj):
    return getObjectByType(obj, "PORT-INTERFACE-MAPPING-SET", {})

def getApplicationDataType(obj):
    return getObjectByType(obj, "APPLICATION-PRIMITIVE-DATA-TYPE", {})

def getImplementationDataType(obj):
    return getObjectByType(obj, "IMPLEMENTATION-DATA-TYPE", {})

def getDataTypeMappingSet(obj):
    return getObjectByType(obj, "DATA-TYPE-MAPPING-SET", {})

def getComponentPrototype(obj):
    return getObjectByType(obj, "SW-COMPONENT-PROTOTYPE", {})

def getConnector(obj):
    return getObjectByType(obj, "ASSEMBLY-SW-CONNECTOR", {})

def extractRteObject(root_rte_obj):  
    if not os.path.exists("output/json/object_extract"):
        os.makedirs("output/json/object_extract")
    sw_components = getSWComponents(root_json)
    with open('output/json/object_extract/sw_components.json', 'w') as f:
        json_string = json.dumps(sw_components, indent=4)
        f.write("%s\n" % json_string)

    client_server_interfaces = getClientServerInterfaces(root_json)
    with open('output/json/object_extract/client_server_interfaces.json', 'w') as f:
        json_string = json.dumps(client_server_interfaces, indent=4)
        f.write("%s\n" % json_string)

    sender_receiver_interfaces = getSenderReceiverInterfaces(root_json)
    with open('output/json/object_extract/sender_receiver_interfaces.json', 'w') as f:
        json_string = json.dumps(sender_receiver_interfaces, indent=4)
        f.write("%s\n" % json_string)

    interface_mapping_sets = getInterfacesMappingSets(root_json)
    with open('output/json/object_extract/interface_mapping_sets.json', 'w') as f:
        json_string = json.dumps(interface_mapping_sets, indent=4)
        f.write("%s\n" % json_string)

    application_datatypes = getApplicationDataType(root_json)
    with open('output/json/object_extract/application_datatypes.json', 'w') as f:
        json_string = json.dumps(application_datatypes, indent=4)
        f.write("%s\n" % json_string)

    datatypes_mapping_sets = getDataTypeMappingSet(root_json)
    with open('output/json/object_extract/datatypes_mapping_sets.json', 'w') as f:
        json_string = json.dumps(datatypes_mapping_sets, indent=4)
        f.write("%s\n" % json_string)   

    connectors = getConnector(root_json)
    with open('output/json/object_extract/connector.json', 'w') as f:
        json_string = json.dumps(connectors, indent=4)
        f.write("%s\n" % json_string)

    component_prototype = getComponentPrototype(root_json)
    with open('output/json/object_extract/component_prototype.json', 'w') as f:
        json_string = json.dumps(component_prototype, indent=4)
        f.write("%s\n" % json_string)

# -------------------------------------------------------------------------------

def writeToHdrFileTheAntiReIncludeWrapperStart(h_file):
    macro  = os.path.splitext(os.path.basename(h_file.name))[0].upper() + "_H"
    h_file.write("\n")
    h_file.write("#ifndef " + macro)
    h_file.write("\n")
    h_file.write("#define " + macro)
    h_file.write("\n\n")
    

def writeToHdrFileIncludeBlock(h_file):
    h_file.write('#include "Rte_Type.h"')
    h_file.write('\n\n')
    
    
def writeToHdrFileTheAntiReIncludeWrapperEnd(h_file):
    macro  = os.path.splitext(os.path.basename(h_file.name))[0].upper()
    h_file.write("\n")
    h_file.write("#endif // " + macro)  

def generateStdTypeHeaderFile():
    if not os.path.exists(GEN_SWC_INCLUDE_FILE_PATH):
        os.makedirs(GEN_SWC_INCLUDE_FILE_PATH)

    file_obj = open(GEN_SWC_INCLUDE_FILE_PATH + "Std_Types.h", 'w')
    writeToHdrFileTheAntiReIncludeWrapperStart(file_obj)
    file_obj.write("typedef unsigned char   uint8;")
    file_obj.write("\n")
    file_obj.write("typedef unsigned long   uint32;")
    file_obj.write("\n")
    file_obj.write("typedef uint8           Std_ReturnType;")
    file_obj.write("\n\n")    
    writeToHdrFileTheAntiReIncludeWrapperEnd(file_obj)

    file_obj.close()
    
    
def generateRteHeaderFileForComponent(root_json):
    component_container_obj = getSWComponents(root_json)
    if isinstance(component_container_obj, dict):
        for obj in component_container_obj.items():
            obj_key = obj[0]
            obj_value = obj[1]
            obj_name = obj_key
            header_file_name = "Rte_" + obj_name + ".h"
            if not os.path.exists(GEN_SWC_INCLUDE_FILE_PATH):
                os.makedirs(GEN_SWC_INCLUDE_FILE_PATH)
            with open(GEN_SWC_INCLUDE_FILE_PATH + header_file_name, 'w') as f:
                writeToHdrFileTheAntiReIncludeWrapperStart(f)
                writeToHdrFileIncludeBlock(f)
                
                writExternStart(f)
                for receive_data in receive_data_point_by_value_api_list:
                    if receive_data["component_name"] == obj_name:
                        f.write("extern " + receive_data["port_api_type"] + " " + \
                                receive_data["port_api_header"] + "_" + \
                                receive_data["port_api_p"] + "_" + \
                                receive_data["port_api_o"] + \
                                "(" + receive_data["port_api_arg_type"] + " " + \
                                receive_data["port_api_arg_value"] + "); " + \
                                "\n" \
                        )
                for send_data in send_data_point_by_value_api_list:
                    if send_data["component_name"] == obj_name:
                        f.write("extern " + "Std_ReturnType" + " " + \
                                send_data["port_api_header"] + "_" + \
                                send_data["port_api_p"] + "_" + \
                                send_data["port_api_o"] + \
                                "(" + send_data["port_api_arg_type"] + " " + \
                                send_data["port_api_arg_value"] + "); " + \
                                "\n" \
                        )
                writExternEnd(f)
                
                for receive_data in receive_data_point_by_value_api_list:
                    if receive_data["component_name"] == obj_name:
                        f.write(\
                            "#define " + 
                            receive_data["port_api_header"] + "_" + \
                            receive_data["port_name"] + "_" + \
                            receive_data["port_api_o"] + \
                            "(" + receive_data["port_api_arg_value"] + ") " + \
                            receive_data["port_api_header"] + "_" + \
                            receive_data["port_api_p"] + "_" + \
                            receive_data["port_api_o"] + \
                            "(" + receive_data["port_api_arg_value"] + ") " + \
                            "\n" \
                        )
                for send_data in send_data_point_by_value_api_list:
                    if send_data["component_name"] == obj_name:
                        f.write(\
                            "#define " + 
                            send_data["port_api_header"] + "_" + \
                            send_data["port_name"] + "_" + \
                            send_data["port_api_o"] + \
                            "(" + send_data["port_api_arg_value"] + ") " + \
                            send_data["port_api_header"] + "_" + \
                            send_data["port_api_p"] + "_" + \
                            send_data["port_api_o"] + \
                            "(" + send_data["port_api_arg_value"] + ") " + \
                            "\n" \
                        )
                        
                writeToHdrFileTheAntiReIncludeWrapperEnd(f)     

# -------------------------------------------------------------------------------

def getRPorts(swcomponent_obj):
    rports = getObjectByType(swcomponent_obj, "R-PORT-PROTOTYPE", {})
    return rports

def getPPorts(swcomponent_obj):
    pports = getObjectByType(swcomponent_obj, "P-PORT-PROTOTYPE", {})
    return pports

def getPorts(swcomponent_obj):
    rports = getObjectByType(swcomponent_obj, "R-PORT-PROTOTYPE", {})
    pports = getObjectByType(swcomponent_obj, "P-PORT-PROTOTYPE", {})
    port = rports.copy()
    port.update(pports)
    return port

def getInterfaceType(interface_ojb):
    interface_type = interface_ojb["object_type"]
    return interface_type

def getDataPointByPortRefPath(swcomponent, port_path):
    data_points_match_port_path = {}
    data_points = getObjectByType(swcomponent, "VARIABLE-ACCESS", {})
    for data_point in data_points.items():
        data_point_key = data_point[0]
        data_point_value = data_point[1]
        if data_point_value["PORT-PROTOTYPE-REF"]["value"] == port_path:
            data_points_match_port_path[data_point_key] = data_point_value
    return data_points_match_port_path

def getDataMappings(root_obj):
    data_mapping_sets = getDataTypeMappingSet(root_obj)
    
def getDataReceivePointByValueApi(data_point_value, rte_root_obj, component_value, port_key):
    data_element_path = data_point_value["TARGET-DATA-PROTOTYPE-REF"]["value"]
    data_element = getJsonObjectFromRefPath(rte_root_obj, data_element_path)
    data_element_name = getObjName(data_element)
    application_data_type_name = getObjNameFromPath(data_element["TYPE-TREF"]["value"])
    data_mappings = getDataTypeMappingSet(rte_root_obj)
    mapped_implementation_data_type_name = ""
    for data_mapping in data_mappings.items():
        data_mapping_key = data_mapping[0]
        data_mapping_value = data_mapping[1]
        mapped_application_data_type_name = getObjNameFromPath(data_mapping_value["APPLICATION-DATA-TYPE-REF"]["value"])
        if mapped_application_data_type_name == application_data_type_name:
            mapped_implementation_data_type_name = getObjNameFromPath(data_mapping_value["IMPLEMENTATION-DATA-TYPE-REF"]["value"])
    port_api_type = mapped_implementation_data_type_name
    port_api_header = rte_port_api["Rte_DRead"]
    port_api_p = getObjName(component_value) + "_" + port_key
    port_api_o = data_element_name
    port_api_arg_type = "void"
    port_api_arg_value = ""
    api = port_api_type + " " + port_api_header + "_" + port_api_p + "_" + port_api_o + "(" + port_api_arg_type + " " + port_api_arg_value + ")"
    receive_data_point_by_value_api_list.append( \
        {data_point_api["port_api_type"]: port_api_type, \
            data_point_api["port_api_header"]: port_api_header, \
            data_point_api["port_api_p"]: port_api_p, \
            data_point_api["port_api_o"]: port_api_o, \
            data_point_api["port_api_arg_type"]: port_api_arg_type, \
            data_point_api["port_api_arg_value"]: port_api_arg_value, \
            "component_name": getObjName(component_value), \
            "port_name": port_key, \
            "api": api, \
            "final_variable_name": port_api_p + "_"  + port_api_o \
        })
    return api + ";"
    
def generateDataSendPointApi(data_point_value, rte_root_obj, component_value, port_key):
    data_element_path = data_point_value["TARGET-DATA-PROTOTYPE-REF"]["value"]
    data_element = getJsonObjectFromRefPath(rte_root_obj, data_element_path)
    data_element_name = getObjName(data_element)
    application_data_type_name = getObjNameFromPath(data_element["TYPE-TREF"]["value"])
    data_mappings = getDataTypeMappingSet(rte_root_obj)
    mapped_implementation_data_type_name = ""
    for data_mapping in data_mappings.items():
        data_mapping_key = data_mapping[0]
        data_mapping_value = data_mapping[1]
        mapped_application_data_type_name = getObjNameFromPath(data_mapping_value["APPLICATION-DATA-TYPE-REF"]["value"])
        if mapped_application_data_type_name == application_data_type_name:
            mapped_implementation_data_type_name = getObjNameFromPath(data_mapping_value["IMPLEMENTATION-DATA-TYPE-REF"]["value"])
    port_api_type = "Std_ReturnType"
    port_api_header = rte_port_api["Rte_Write"]
    port_api_p = getObjName(component_value) + "_" + port_key
    port_api_o = data_element_name
    port_api_arg_type = mapped_implementation_data_type_name
    port_api_arg_value = "data"
    api = port_api_type + " " + port_api_header + "_" + port_api_p + "_" + port_api_o + "(" + port_api_arg_type + " " + port_api_arg_value + ")"
    send_data_point_by_value_api_list.append(\
        {data_point_api["port_api_type"]: port_api_type, \
            data_point_api["port_api_header"]: port_api_header, \
            data_point_api["port_api_p"]: port_api_p, \
            data_point_api["port_api_o"]: port_api_o, \
            data_point_api["port_api_arg_type"]: port_api_arg_type, \
            data_point_api["port_api_arg_value"]: port_api_arg_value, \
            "component_name": getObjName(component_value), \
            "port_name": port_key, \
            "api": api, \
            "final_variable_name": port_api_p + "_"  + port_api_o \
        })
    return api + ";"
    
def getPortApiFromPortList(component_value, port_list, rte_root_obj):
    ret = []
    port_api_type = ""
    port_api_header = ""
    port_api_p = ""
    port_api_o = ""
    port_api_arg = "" 
    data_receive_point_by_value_api_list = []
    data_send_point_api_list = []
    for port in port_list.items():       
        port_key = port[0]
        port_value = port[1]
        port_path = port_value["object_path"]
        data_points = getDataPointByPortRefPath(component_value, port_path)
        for data_point in data_points.items():
            data_point_key = data_point[0]
            data_point_value = data_point[1]
            if data_point_value["outter_element_tag"] == "/DATA-RECEIVE-POINT-BY-VALUES":
                api = getDataReceivePointByValueApi(data_point_value, rte_root_obj, component_value, port_key)
                data_receive_point_by_value_api_list.append(api)
            elif data_point_value["outter_element_tag"] == "/DATA-SEND-POINTS":
                api = generateDataSendPointApi(data_point_value, rte_root_obj, component_value, port_key)
                data_send_point_api_list.append(api)
    for api in data_receive_point_by_value_api_list:
        ret.append(api)
    for api in data_send_point_api_list:
        ret.append(api)
    return ret

    
    
def getPortApiFromComponent(rte_root_obj):
    ret = []
    swcomponents = getSWComponents(rte_root_obj)
    for component in swcomponents.items(): 
        component_key = component[0]
        component_value = component[1]
        ports = getPorts(component_value)
        ret = ret + getPortApiFromPortList(component_value, ports, rte_root_obj)
    return ret
    

def updateConnectorList(rte_root_obj):
    connectors = getConnector(rte_root_obj)
    component_prototype = getComponentPrototype(rte_root_obj)
    for connector in connectors.items():
        connector_name = connector[0]
        connector_value = connector[1]
        
        provider_component_prototype_name = getObjNameFromPath(connector_value["CONTEXT-COMPONENT-REF-PROVIDER"]["value"])
        provider_component_name = getObjNameFromPath(component_prototype[provider_component_prototype_name]["TYPE-TREF"]["value"])
        provider_port_name = getObjNameFromPath(connector_value["TARGET-P-PORT-REF"]["value"])
        
        requester_component_prototype_name = getObjNameFromPath(connector_value["CONTEXT-COMPONENT-REF-REQUESTER"]["value"])
        requester_component_name = getObjNameFromPath(component_prototype[requester_component_prototype_name]["TYPE-TREF"]["value"])
        requester_port_name = getObjNameFromPath(connector_value["TARGET-R-PORT-REF"]["value"])
        
        connector_list.append(\
            {\
              "provider_component_name": provider_component_name, \
              "provider_port_name": provider_port_name, \
              "requester_component_name": requester_component_name, \
              "requester_port_name": requester_port_name, \
            }\
        )

def updateEventToTaskMappingList(rte_root_obj):
    ecuc_containter_value_list = getObjectByType(rte_root_obj, "ECUC-CONTAINER-VALUE", {})
    for ecuc_containter_value in ecuc_containter_value_list.items():
        ecuc_containter_value_key = ecuc_containter_value[0]
        ecuc_containter_value_value = ecuc_containter_value[1]
        if "DEFINITION-REF-RteEventToTaskMapping" in ecuc_containter_value_value:
            event_to_task_mapping_name = getObjNameFromPath(ecuc_containter_value_value["object_path"])
            event = getJsonObjectFromRefPath(rte_root_obj, ecuc_containter_value_value["VALUE-REF-RteEventRef"]["value"])
            runnable = getJsonObjectFromRefPath(rte_root_obj, event["START-ON-EVENT-REF"]["value"])
            function_name = runnable["SYMBOL"]["value"]
            os_task = getObjNameFromPath(ecuc_containter_value_value["VALUE-REF-RteMappedToTaskRef"]["value"])
            event_position_in_task = ecuc_containter_value_value["VALUE-RtePositionInTask"]["value"]
            
            event_to_task_mapping_list.append({ \
                "event_to_task_mapping_name": event_to_task_mapping_name, \
                "event": event, \
                "runnable": runnable, \
                "function_name": function_name, \
                "os_task": os_task, \
                "event_position_in_task": event_position_in_task
            })
        
def updateTaskInfoList(rte_root_obj):
    task_info = {}
    task_table = getJsonObjectFromRefPath(rte_root_obj, "/RB/UBK/Project/EcucModuleConfigurationValuess/CanTrcv/esc_stack_cfg/esc_stackDTtable")
    for task in task_table.items():
        task_key = task[0]
        task_value = task[1]
        os_task_name = ""
        task_name = ""
        cycle_time = 0
        if type(task_value) is dict and "object_path" in task_value:
            os_task_name = task_key
            if "VALUE-esc_TaskCycle" in task_value:
                cycle_time = task_value["VALUE-esc_TaskCycle"]["value"]
            if type(task_value) is dict:
                for task_properties in task_value.items():
                    task_properties_key = task_properties[0]
                    task_properties_value = task_properties[1]
                    if "VALUE-esc_stack_taskname" in task_properties_value:
                        task_name = task_properties_value["VALUE-esc_stack_taskname"]["value"]
            
            if os_task_name != "" and task_name != "" and cycle_time != 0:
                task_info["os_task_name"] = os_task_name
                task_info["task_name"] = task_name
                task_info["cycle_time"] = cycle_time
                task_info_list.append(task_info.copy())
                
    os = getJsonObjectFromRefPath(rte_root_obj, "/RB/UBK/Project/EcucModuleConfigurationValuess/Os")
    for task in os.items():
        task_key = task[0]
        task_value = task[1]
        for task_info in task_info_list:
            if task_key == task_info["task_name"]:
                task_info["priority"] = task_value["VALUE-OsTaskPriority"]["value"]


def writExternStart(c_file):
    # c_file.write('#ifdef __cplusplus\n')
    # c_file.write('extern "C" {\n')
    # c_file.write('#endif')
    # c_file.write("\n\n")
    pass

def writExternEnd(c_file):
    # c_file.write("\n")
    # c_file.write('#ifdef __cplusplus\n')
    # c_file.write('}\n')
    # c_file.write('#endif')
    # c_file.write("\n\n")
    pass


def writeToScrFileIncludeBlock(c_file):
    # include_files = getFilesByExtension(GEN_SWC_INCLUDE_FILE_PATH, 'h')
    # for include_file in include_files:
    #     file_base_name = os.path.basename(include_file)
    #     c_file.write('#include "' + file_base_name + '"')
    #     c_file.write("\n")
    c_file.write('#include "Rte.h"')
    c_file.write("\n")
    c_file.write('#include "Rte_Type.h"')
    c_file.write("\n\n")
   
    
def writeToScrFilePortApi(c_file, port_apis):
    for port_api in port_apis:
        c_file.write(port_api)
        c_file.write("\n")
    c_file.write("\n")

    
def writeToScrDateApi(c_file, rte_root_obj, connector_list, receive_data_list, send_data_list):
    updateConnectorList(rte_root_obj)
    provide_request_pair = []
    for connector in connector_list:
        for send_data in send_data_list:
            if (send_data["component_name"] == connector["provider_component_name"]) and (send_data["port_name"] == connector["provider_port_name"]):
                for receive_data in receive_data_list:
                    if (receive_data["component_name"] == connector["requester_component_name"]) and (receive_data["port_name"] == connector["requester_port_name"]):
                        provide_request_pair.append(\
                            {
                                "provider": send_data, \
                                "requester": receive_data \
                            }
                        )
    
    for send_data in send_data_list:
        code_for_assigning_data_to_requester_data_point = ""
        for data_pair in provide_request_pair:
            if data_pair["provider"] == send_data:
                code_for_assigning_data_to_requester_data_point = code_for_assigning_data_to_requester_data_point + \
                    data_pair["requester"]["final_variable_name"] + " = " + send_data["final_variable_name"] + ";\n"        
        funciton_definition = \
        """""" + send_data["api"] + """
        {
            Std_ReturnType rtn;
            
            rtn = RTE_E_OK;
            
            """ + send_data["final_variable_name"] + """ = data;\n
            """ + code_for_assigning_data_to_requester_data_point + """
            return rtn;
        }
                """ + "\n"
        c_file.write(funciton_definition)
    
    for receive_data in receive_data_list:
        funciton_definition = \
        """""" + receive_data["api"] + """
        {
            """ + receive_data["port_api_type"] + """ rtn;

            rtn = """ + receive_data["final_variable_name"] + """;

            return rtn;
        }
                """ + "\n"
        c_file.write(funciton_definition)
        
    
def writeToHdrFileDataDefinition(c_file, receive_data_list, send_data_list):
    for receive_data in receive_data_list:
        data_definition = receive_data["port_api_type"] + " " +  receive_data["final_variable_name"] + ";"
        c_file.write(data_definition)
        c_file.write("\n")
    for send_data in send_data_list:
        data_definition = send_data["port_api_arg_type"] + " " +  send_data["final_variable_name"] + ";"
        c_file.write(data_definition)
        c_file.write("\n")
    c_file.write("\n")
   
    
def writeToRteMainHdrFileDefineMacroBlock(file):
    file.write("#ifndef RTE_E_OK\n")
    file.write("#define RTE_E_OK ((Std_ReturnType)0x01)\n")
    file.write("#endif // RTE_E_OK\n")
    file.write("\n")
    file.write("#ifndef RTE_E_NOT_OK\n")
    file.write("#define RTE_E_NOT_OK ((Std_ReturnType)0x00)\n")
    file.write("#endif // RTE_E_NOT_OK\n\n")
    
    
def writeToRteMainHdrFileDefineTypedefBlock(file_obj, rte_root_obj):
    impl_type_list = getImplementationDataType(rte_root_obj)
    for impl_type in impl_type_list.items():
        impl_type_key = impl_type[0]
        impl_type_value = impl_type[1]
        impl_type_name = impl_type_key
        impl_base_type = getObjNameFromPath(impl_type_value["IMPLEMENTATION-DATA-TYPE-REF"]["value"])
        file_obj.write("typedef " + impl_base_type + " " + impl_type_name + ";")
        file_obj.write("\n")
        
    
def generateRteTypeHeaderFile(rte_root_obj):
    if not os.path.exists(GEN_SWC_INCLUDE_FILE_PATH):
        os.makedirs(GEN_SWC_INCLUDE_FILE_PATH)

    file_obj = open(GEN_SWC_INCLUDE_FILE_PATH + "Rte_Type.h", 'w')
    
    writeToHdrFileTheAntiReIncludeWrapperStart(file_obj)
    file_obj.write('#include "Std_Types.h"')
    file_obj.write("\n\n")
    writeToRteMainHdrFileDefineTypedefBlock(file_obj, rte_root_obj)
    writeToHdrFileTheAntiReIncludeWrapperEnd(file_obj)

    file_obj.close()
    

def generateRteMainHeaderFile(port_apis):
    if not os.path.exists(GEN_SWC_INCLUDE_FILE_PATH):
        os.makedirs(GEN_SWC_INCLUDE_FILE_PATH)

    file_obj = open(GEN_SWC_INCLUDE_FILE_PATH + "Rte.h", 'w')
    
    writeToHdrFileTheAntiReIncludeWrapperStart(file_obj)
    writeToHdrFileIncludeBlock(file_obj)
    writeToRteMainHdrFileDefineMacroBlock(file_obj)
    writeToHdrFileDataDefinition(file_obj, receive_data_point_by_value_api_list, send_data_point_by_value_api_list)
    writeToScrFilePortApi(file_obj, port_apis)
    writeToHdrFileTheAntiReIncludeWrapperEnd(file_obj)

    file_obj.close()


def generateRteMainSourceFile(rte_root_obj):
    if not os.path.exists(GEN_SWC_SOURCE_FILE_PATH):
        os.makedirs(GEN_SWC_SOURCE_FILE_PATH)

    file_obj = open(GEN_SWC_SOURCE_FILE_PATH + "Rte.cpp", 'w')

    writeToScrFileIncludeBlock(file_obj)
    writExternStart(file_obj)
    writeToScrDateApi(file_obj, rte_root_obj, connector_list, receive_data_point_by_value_api_list, send_data_point_by_value_api_list)
    writExternEnd(file_obj)
    
    file_obj.close()


def generateRteEventToTaskMappingSourceFile(rte_root_obj):
    updateEventToTaskMappingList(rte_root_obj)
    os_tasks = {}
    for mapping in event_to_task_mapping_list:
        if mapping["os_task"] not in os_tasks:
            os_tasks[mapping["os_task"]] = []
            os_tasks[mapping["os_task"]].append({"function_name": mapping["function_name"], "position": mapping["event_position_in_task"]})
        else:
            os_tasks[mapping["os_task"]].append({"function_name": mapping["function_name"], "position": mapping["event_position_in_task"]})
        sorted_list = sorted(os_tasks[mapping["os_task"]], key=lambda x: int(x["position"]))
        os_tasks[mapping["os_task"]] = sorted_list
    
    if not os.path.exists(GEN_SWC_SOURCE_FILE_PATH):
        os.makedirs(GEN_SWC_SOURCE_FILE_PATH)

    file_obj = open(GEN_SWC_SOURCE_FILE_PATH + "RTE_Event_To_Task_Mapping.cpp", 'w')
    
    writExternStart(file_obj)

    for os_task in os_tasks.items():
        for funciton in os_task[1]:
            function_name = funciton["function_name"]
            file_obj.write("extern void " + function_name + "();")
            file_obj.write("\n")
    file_obj.write("\n")
        
    for os_task in os_tasks.items():
        os_task_name = os_task[0]
        file_obj.write("void " + os_task_name + "()")
        file_obj.write("{")
        file_obj.write("\n")
        
        for funciton in os_task[1]:
            function_name = funciton["function_name"]
            file_obj.write("\t(void) " + function_name + "();")
            file_obj.write("\n")
        file_obj.write("}")
        file_obj.write("\n\n")
    
    writExternEnd(file_obj)
    file_obj.close()
    
    
def generateRteOsTaskDefinition(rte_root_obj):
    updateTaskInfoList(root_json)
    
    if not os.path.exists(GEN_SWC_SOURCE_FILE_PATH):
        os.makedirs(GEN_SWC_SOURCE_FILE_PATH)

    file_obj = open(GEN_SWC_SOURCE_FILE_PATH + "main.cpp", 'w')
    
    file_obj.write('#include "Arduino.h"\n')
    file_obj.write('#include "freertos/FreeRTOS.h"\n')
    file_obj.write("\n\n")
    
    writExternStart(file_obj)
    for task_info in task_info_list:
        task_name = task_info["task_name"]
        file_obj.write("extern void " + task_name + "();")
        file_obj.write("\n")
    file_obj.write("\n")
    writExternEnd(file_obj)
    
    for task_info in task_info_list:
        file_obj.write("void " + task_info["os_task_name"] + "( void * pvParameters )\n")
        file_obj.write("{")
        file_obj.write("\n")
        file_obj.write("\tTickType_t xLastWakeTime;\n")
        file_obj.write("\tconst TickType_t xFrequency = " + str(int(int(task_info["cycle_time"]))) + ";\n")
        file_obj.write("\n")
        file_obj.write("\tfor(;;)")
        file_obj.write("\n")
        file_obj.write("\t{")
        file_obj.write("\n")
        file_obj.write("\t\t(void) " + task_info["task_name"] + "();")
        file_obj.write("\n")
        file_obj.write("\n")
        file_obj.write("\t\tvTaskDelayUntil( &xLastWakeTime, xFrequency );")
        file_obj.write("\n")
        file_obj.write("\t}")
        file_obj.write("\n")
        file_obj.write("}")
        file_obj.write("\n")
    file_obj.write("\n")
        
    setup_create_task = ""
    for task_info in task_info_list:
        setup_create_task = setup_create_task + '\txTaskCreate(' + task_info["os_task_name"] + ', "' + task_info["os_task_name"] + '", ' + str(RTOS_STACK_DEPTH) + ', NULL, ' + task_info["priority"] + ', NULL);\n'
        pass
    file_obj.write("\n")
    
    file_obj.write(""" 
void setup() {
  // put your setup code here, to run once:
  """ + setup_create_task + """
}

void loop() {
  // put your main code here, to run repeatedly:
}   
""")
    file_obj.close()

def copyFilesWithExtension(source_folder, destination_folder, extension):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for root, _, files in os.walk(source_folder):
        for file in files:
            source_file_path = os.path.join(root, file)
            # Check if the file is a regular file and has the desired extension
            if os.path.isfile(source_file_path) and file.endswith(extension):
                destination_file_path = os.path.join(destination_folder, file)
                shutil.copy2(source_file_path, destination_file_path)
                

def deleteFilesInFolder(folder_path):
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        # Check if the file is a regular file and then delete it
        if os.path.isfile(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    
    if not os.path.exists(ARXML_INPUT_PATH):
        os.makedirs(ARXML_INPUT_PATH)
    deleteFilesInFolder(ARXML_INPUT_PATH)
    deleteFilesInFolder(OUTPUT_JSON_PATH)
    deleteFilesInFolder(OUTPUT_JSON_EXTRACT_PATH)
    copyFilesWithExtension(APPL_SWC_PATH, ARXML_INPUT_PATH, "arxml")
    
    input_arxml_path = current_path + "\\input\\arxml"
    output_json_path = current_path + "/output/json"

    fullArxmlToJsonParsing(input_arxml_path, output_json_path)
    
    root_json = None
    with open(output_json_path + "\\root.json", 'r') as f:
        root_json = json.load(f)
    
    extractRteObject(root_json)
    
    # run getPortApiFromComponent to update value for receive_data_point_by_value_api_list and send_data_point_by_value_api_list 
    # getPortApiFromComponent must be run once
    port_apis = getPortApiFromComponent(root_json)

    generateStdTypeHeaderFile()
    generateRteHeaderFileForComponent(root_json)
    generateRteTypeHeaderFile(root_json)
    generateRteMainHeaderFile(port_apis)
    generateRteMainSourceFile(root_json)
    generateRteEventToTaskMappingSourceFile(root_json)
    generateRteOsTaskDefinition(root_json)
    
    
    if not os.path.exists("include"):
        os.makedirs("include")
    if not os.path.exists("src"):
        os.makedirs("src")
    deleteFilesInFolder("include")
    deleteFilesInFolder("src")
    copyFilesWithExtension(APPL_SWC_PATH, "include", "h")
    copyFilesWithExtension(APPL_SWC_PATH, "src", "cpp")
    copyFilesWithExtension(GEN_SWC_INCLUDE_FILE_PATH, "include", "h")
    # copyFilesWithExtension(GEN_SWC_SOURCE_FILE_PATH, "src", "c")
    copyFilesWithExtension(GEN_SWC_SOURCE_FILE_PATH, "src", "cpp")
    
    # for item in receive_data_point_by_value_api_list:
    # writeToLogFile(json.dumps(receive_data_point_by_value_api_list, indent=4))