# File that reads a indexjs file and looks if it contains eth_signTypedData_v4
# If it does, it will print the file name and the line number
# Usage: python3 test.py

import os
import json
import re
import ast

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
    


# path of the file
path = "C:/Users/oleob/Downloads/test-dapp-main/src/index.js"

check = False
values = ["types","domain","primaryType","message"]

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
            pattern = r'const msgProg = {'

struct = find_between( data, "const msgParams = {", "};" )
print(struct)
retorno = json.dumps(struct)
