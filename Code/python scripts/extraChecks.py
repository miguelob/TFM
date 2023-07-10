from domainCheck import start

def check_js_file(file_path):
    error = ""
    with open(file_path, 'r') as f:
        file_contents = f.read()
        if 'eth_signTypedData_v3' in file_contents :
            error += "\nDapp Vulnerable due to the presence of eth_signTypedData_v3."
        if 'eth_signTypedData' in file_contents:
            error += "\nDapp Vulnerable due to the presence of eth_signTypedData."
        if error == "":
            error = "Dapp has no presence of eth_signTypedData or eth_signTypedData_v3."
    return error
        
def check(name):
    error = ""
    if name == "test":
        error += check_js_file("./index.js")
        error += start("./index.js")
    elif name == "test2":
        error += check_js_file("./index2.js")
        error += start("./index2.js")
    return error