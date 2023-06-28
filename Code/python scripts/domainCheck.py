# File that reads a indexjs file and looks if it contains eth_signTypedData_v4
# If it does, it will print the file name and the line number
# Usage: python3 test.py

import os
import json
import re

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail

def get_types(input):
    values_temp = ["\"domain\":","\"primaryType\":","\"message\":"]
    for value in values_temp:
        check = input.split("\"types\":")[1].split(value)[0]
        if (values_temp[0] not in check) and (values_temp[1] not in check) and (values_temp[2] not in check):
                temp = replace_last(check,"},","}")
                temp = replace_last(temp,"],","]")
                temp = replace_last(temp,"},","}")
                return temp.replace("\"address\" },","\"address\" }")
    
def get_primaryType(input):
    return input.split("\"primaryType\":")[1].split(",")[0]

def get_domain(input):
    values_temp = ["\"types\":","\"primaryType\":","\"message\":"]
    for value in values_temp:
        check = input.split("\"domain\":")[1].split(value)[0]
        if (values_temp[0] not in check) and (values_temp[1] not in check) and (values_temp[2] not in check):
                return replace_last(replace_last(check,"},","}"),"\",","\"")

def get_message(input):
    values_temp = ["\"types\":","\"primaryType\":","\"types\":"]
    for value in values_temp:
        check = input.split("\"message\":")[1].split(value)[0]
        if (values_temp[0] not in check) and (values_temp[1] not in check) and (values_temp[2] not in check):
            check = re.sub(r'("wallet":\s*"[^"]*"),\s*', r'\1', check)
            return replace_last(replace_last(check,"\",","\""),"}","")
            
        
def fix_types(input):
    return input.replace("types:","\"types\":") \
        .replace("domain:","\"domain\":")\
        .replace("primaryType:","\"primaryType\":")\
        .replace("message:","\"message\":")\
        .replace("name:","\"name\":")\
        .replace("type:","\"type\":")\
        .replace("Person:","\"Person\":")\
        .replace("Mail:","\"Mail\":")\
        .replace("version:","\"version\":")\
        .replace("verifyingContract:","\"verifyingContract\":")\
        .replace("salt:","\"salt\":")\
        .replace("chainId,","\"chainId\": '1',")\
        .replace("from:","\"from\":")\
        .replace("to:","\"to\":")\
        .replace("value:","\"value\":")\
        .replace("data:","\"data\":")\
        .replace("value:","\"value\":")\
        .replace("wallet:","\"wallet\":") \
        .replace("contents:","\"contents\":") \
        .replace("EIP712Domain:","\"EIP712Domain\":") \
        .replace("'","\"")

def check_domain(domain, types):
    errors = ""
    check = True
    values_defined = []
    for value in domain.keys():
        values_defined.append(value)
        if value not in domain_values:
            errors.append(value + " not in domain.")
        if value == "verifyingContract":
            check = False
    if check == True:
        errors.append("verifyingContract not in domain.")
    for value in types['EIP712Domain']:
        if value['type'] not in domain_types:
            errors.append(value['type'] + " not in domain.")
        if value['name'] not in values_defined:
            errors.append(value['name'] + " is defined in types but not used.")
    if errors == "":
        errors = "No errors found."
    return errors

def check_methods(types, primaryType, domain, message):
    errors = ""
    EIP =[]
    MSG = []
    inTypes = []
    nested = []
    if primaryType not in str(types.keys()):
        errors.append("primaryType not in types.")
    if "EIP712Domain" not in str(types.keys()):
        errors.append("EIP712Domain not in types.")
    for value in types['EIP712Domain']:
        EIP.append(value['name'])
    for value in EIP:
        if value not in str(domain.keys()):
            errors.append(value + " not in domain.")
    for value in types.keys():
        for value2 in types[value]:
            if value2['type'] in str(types.keys()):
                nested.append(value2['name'])
                inTypes.append(value2['type'])
                inTypes.append(value)
    for value in types[inTypes[1]]:
        MSG.append(value['name'])
    for value in MSG:
        if value not in str(message.keys()):
            errors.append(value + " not in message.")
        if value in nested:
            for value2 in types[inTypes[0]]:
                if value2['name'] not in nested:
                    pass
                else:
                    errors.append(value2['name'] + " not in message.")

    if errors == "":
        errors = "No errors found."
    return errors


# path of the file
path = "C:/Users/oleob/Downloads/test-dapp-main/src/index.js"

check = False
definition_check = False
values = ["types","domain","primaryType","message"]
domain_values =["name","version","chainId","verifyingContract","salt"]
domain_types = ["string","string","uint256","address","bytes32"]

# open the file
with open(path, "r") as file:
    # read the file
    data = file.read()
    # find all the lines that contain eth_signTypedData_v4
    for match in re.finditer("eth_signTypedData_v4", data):
        # print the file name and the line number
        check = True
        print("Found eth_signTypedData_v4 in file: " + path + " at line: " + str(data.count("\n", 0, match.start()) + 1))
        #read specific line
        next_line = data.splitlines()[data.count("\n", 0, match.start()) + 1]
        
        # check for content of the line
        if "JSON.stringify" in next_line:
            # get the content of JSON.stringify
            content = next_line.split("JSON.stringify(")[1].split(")")[0]
            if ' ' in content:
                definition_check = True
            else:
                pattern = r'const '+content+' = {'

if not definition_check:
    struct = find_between( data, pattern, "};" )
    struct_fix = "{"+replace_last(fix_types(struct),'},','}')+"}"
    # TODO: check if the struct is correct
else:
    struct = pattern
#print(struct_fix)
#structured = json.loads(struct_fix)
#print(structured)

print(get_primaryType(struct_fix))
formated_domain = json.loads(get_domain(struct_fix))
print(formated_domain.keys())
formated_types = json.loads(get_types(struct_fix))
print(formated_types.keys())
#print(get_message(struct_fix))
formated_message = json.loads(get_message(struct_fix))
print(formated_message.keys())
print(check_domain(formated_domain, formated_types))
#out = check_methods(formated_types, get_primaryType(struct_fix).replace("\"","'"), formated_domain, formated_message)
#print(out)
