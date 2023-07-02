import sys, os
import json
from lxml import etree
import glob


current_path = os.getcwd()

etree_namespace = {'ar': 'http://autosar.org/schema/r4.0'}
etree.register_namespace('ar', 'http://autosar.org/schema/r4.0')

GEN_SWC_INCLUDE_FILE_PATH = "output/_gen/swb/includes/rtegen/swc/"
GEN_SWC_SOURCE_FILE_PATH = "output/_gen/swb/src_files/rtegen/swc/"

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
        arxmlToJsonParsing(arxml_file, json_file_path)
    root_json_obj = {}
    json_files = getFilesByExtension(output_json_path, 'json')
    for json_file in json_files:
        json_obj = None
        with open(json_file, 'r') as f:
            json_obj = json.load(f)
        mergeJsonData(root_json_obj, json_obj)
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
    return getObjectByType(obj, "APPLICATION-SW-COMPONENT-TYPE", {})

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

def extractRteObject(root_rte_obj):  
    if not os.path.exists("output/object_extract"):
        os.makedirs("output/object_extract")
    sw_components = getSWComponents(root_json)
    with open('output/object_extract/sw_components.json', 'w') as f:
        json_string = json.dumps(sw_components, indent=4)
        f.write("%s\n" % json_string)

    client_server_interfaces = getClientServerInterfaces(root_json)
    with open('output/object_extract/client_server_interfaces.json', 'w') as f:
        json_string = json.dumps(client_server_interfaces, indent=4)
        f.write("%s\n" % json_string)

    sender_receiver_interfaces = getSenderReceiverInterfaces(root_json)
    with open('output/object_extract/sender_receiver_interfaces.json', 'w') as f:
        json_string = json.dumps(sender_receiver_interfaces, indent=4)
        f.write("%s\n" % json_string)

    interface_mapping_sets = getInterfacesMappingSets(root_json)
    with open('output/object_extract/interface_mapping_sets.json', 'w') as f:
        json_string = json.dumps(interface_mapping_sets, indent=4)
        f.write("%s\n" % json_string)

    application_datatypes = getApplicationDataType(root_json)
    with open('output/object_extract/application_datatypes.json', 'w') as f:
        json_string = json.dumps(application_datatypes, indent=4)
        f.write("%s\n" % json_string)

    datatypes_mapping_sets = getDataTypeMappingSet(root_json)
    with open('output/object_extract/datatypes_mapping_sets.json', 'w') as f:
        json_string = json.dumps(datatypes_mapping_sets, indent=4)
        f.write("%s\n" % json_string)   

# -------------------------------------------------------------------------------

def writeToHdrFileTheAntiReIncludeWrapperStart(h_file):
    macro  = os.path.splitext(os.path.basename(h_file.name))[0].upper() + "_H"
    h_file.write("\n")
    h_file.write("#ifndef " + macro)
    h_file.write("\n")
    h_file.write("#define " + macro)
    h_file.write("\n\n")
    
def writeToHdrFileTheAntiReIncludeWrapperEnd(h_file):
    macro  = os.path.splitext(os.path.basename(h_file.name))[0].upper()
    h_file.write("\n")
    h_file.write("#endif // " + macro)  

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
                # ...
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
    
def getDataReceivePointByValueAPI(data_point_value, rte_root_obj, component_value, file, port_key):
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
    receive_data_point_by_value_api_list.append({data_point_api["port_api_type"]: port_api_type, data_point_api["port_api_header"]: port_api_header, data_point_api["port_api_p"]: port_api_p, data_point_api["port_api_o"]: port_api_o, data_point_api["port_api_arg_type"]: port_api_arg_type, data_point_api["port_api_arg_value"]: port_api_arg_value})
    return api + ";"
    
def generateDataSendPointAPI(data_point_value, rte_root_obj, component_value, file, port_key):
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
    send_data_point_by_value_api_list.append({data_point_api["port_api_type"]: port_api_type, data_point_api["port_api_header"]: port_api_header, data_point_api["port_api_p"]: port_api_p, data_point_api["port_api_o"]: port_api_o, data_point_api["port_api_arg_type"]: port_api_arg_type, data_point_api["port_api_arg_value"]: port_api_arg_value})
    return api + ";"
    
def getPortAPIFromPortList(component_value, port_list, rte_root_obj, file):
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
                api = getDataReceivePointByValueAPI(data_point_value, rte_root_obj, component_value, file, port_key)
                data_receive_point_by_value_api_list.append(api)
            elif data_point_value["outter_element_tag"] == "/DATA-SEND-POINTS":
                api = generateDataSendPointAPI(data_point_value, rte_root_obj, component_value, file, port_key)
                data_send_point_api_list.append(api)
    for api in data_receive_point_by_value_api_list:
        ret.append(api)
    for api in data_send_point_api_list:
        ret.append(api)
    return ret

    
    
def getPortAPIFromComponent(rte_root_obj, file):
    ret = []
    swcomponents = getSWComponents(rte_root_obj)
    for component in swcomponents.items(): 
        component_key = component[0]
        component_value = component[1]
        ports = getPorts(component_value)
        ret = ret + getPortAPIFromPortList(component_value, ports, rte_root_obj, file)
    return ret

def writeToScrFileIncludeBlock(c_file):
    c_file.write("\n")
    include_files = getFilesByExtension(GEN_SWC_INCLUDE_FILE_PATH, 'h')
    for include_file in include_files:
        file_base_name = os.path.basename(include_file)
        c_file.write('#include "' + file_base_name + '"')
        c_file.write("\n")
    c_file.write("\n")
   
    
def writeToScrPortApi(c_file, port_apis):
    for port_api in port_apis:
        c_file.write(port_api)
        c_file.write("\n")
   
    
def writeToRteMainHdrFileDefineMacroBlock(file):
    file.write("#ifndef RTE_E_OK\n")
    file.write("#ifndef RTE_E_OK ((Std_ReturnType)0x01)\n")
    file.write("#endif // RTE_E_OK\n")
    file.write("\n")
    file.write("#ifndef RTE_E_NOT_OK\n")
    file.write("#ifndef RTE_E_NOT_OK ((Std_ReturnType)0x00)\n")
    file.write("#endif // RTE_E_NOT_OK\n")
    
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
    writeToRteMainHdrFileDefineTypedefBlock(file_obj, rte_root_obj)
    writeToHdrFileTheAntiReIncludeWrapperEnd(file_obj)

    file_obj.close()
    
    
def generateRteMainHeaderFile(rte_root_obj):
    if not os.path.exists(GEN_SWC_INCLUDE_FILE_PATH):
        os.makedirs(GEN_SWC_INCLUDE_FILE_PATH)

    file_obj = open(GEN_SWC_INCLUDE_FILE_PATH + "Rte.h", 'w')
    writeToHdrFileTheAntiReIncludeWrapperStart(file_obj)
    writeToRteMainHdrFileDefineMacroBlock(file_obj)
    writeToHdrFileTheAntiReIncludeWrapperEnd(file_obj)

    file_obj.close()


def generateRteMainSourceFile(rte_root_obj):
    if not os.path.exists(GEN_SWC_SOURCE_FILE_PATH):
        os.makedirs(GEN_SWC_SOURCE_FILE_PATH)

    file_obj = open(GEN_SWC_SOURCE_FILE_PATH + "Rte.c", 'w')

    writeToScrFileIncludeBlock(file_obj)
    port_api = getPortAPIFromComponent(rte_root_obj, file_obj)
    
    # data element information is gotten after getPortAPIFromComponent, they are stored in receive_data_point_by_value_api_list and send_data_point_by_value_api_list
    # define C variable represent those data elements here
    # print(receive_data_point_by_value_api_list)
    # writeToLogFile(receive_data_point_by_value_api_list)
    writeToLogFile(send_data_point_by_value_api_list)
        
    # port API prototype will be write after variable definition
    print(port_api)
    writeToScrPortApi(file_obj, port_api)

    file_obj.close()


if __name__ == "__main__":
    input_arxml_path = current_path + "\\input\\arxml"
    output_json_path = current_path + "/output/json"

    fullArxmlToJsonParsing(input_arxml_path, output_json_path)
    
    root_json = None
    with open(output_json_path + "\\root.json", 'r') as f:
        root_json = json.load(f)
    
    extractRteObject(root_json)
        
    generateRteHeaderFileForComponent(root_json)
    generateRteTypeHeaderFile(root_json)
    generateRteMainHeaderFile(root_json)
    generateRteMainSourceFile(root_json)