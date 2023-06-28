import os

def search_files_for_string(path, string):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('.js', '.ts', '.json')):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    if string in f.read():
                        print(f"Found '{string}' in {os.path.join(root, file)}")

search_files_for_string('C:/Users/oleob/Downloads/test-dapp-main', 'eth_signTypedData_v4')