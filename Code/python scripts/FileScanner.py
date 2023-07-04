import os

vulnerabilities = []
def search_files_for_strings(path, strings):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('.js', '.ts', '.json')):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    file_contents = f.read()
                    for string in strings:
                        if string in file_contents:
                            #print(f"Found '{string}' in {os.path.join(root, file)}")
                            vulnerabilities.append("The app is vulnerable because it uses the following method:"+ string)
                            
    return vulnerabilities

search_strings = ['eth_signTypedData_v4', 'eth_signTypedData_v3', 'eth_signTypedData', 'personal_sign', 'eth_sign']
vul = set(search_files_for_strings('C:/Users/oleob/Downloads/test-dapp-main', search_strings))
print(vul)