import tkinter as tk
from readDatabase import returnNames, returnValues


# Create the main window
root = tk.Tk()
root.geometry('400x300')
root.title('DApp Vulnerability Checker')

# Create a list of options for the dropdown
options = returnNames()

# Create a variable to store the selected option
selected_option = tk.StringVar()

# Create the dropdown widget
dropdown = tk.OptionMenu(root, selected_option, *options)
dropdown.config(width=20)
dropdown.pack(pady=20)

# Create the button widget
button = tk.Button(root, text='Submit', width=20, height=2)
button.pack()

def vul(input):
    check = "red"
    flag = False
    error = ""
    checks = ["Not Found", "Wrong link", "Link not working", "Not found", "Unknown"]
    if input[3] not in checks:
        flag = True
        error.append("Dapp Vulnerable due to the presence of eth_sign.")
    if input[4] not in checks:
        flag = True
        error.append("Dapp Vulnerable due to the presence of personal_sign.")
    if flag == False:
        error = "Dapp not vulnerable."
        check = "green"

    return [error, check]
    

# Define a function to create a new window with the results
def show_results():
    # Get the values for the selected option
    values = returnValues(selected_option.get())

    # Create a new window
    results_window = tk.Toplevel(root)
    results_window.geometry('400x300')

    # Create labels to display the results
    name_label = tk.Label(results_window, text=f"DApp Name: {selected_option.get()}")
    name_label.pack()

    url_label = tk.Label(results_window, text=f"URL: {values[0]}")
    url_label.pack()

    lang_label = tk.Label(results_window, text=f"Language: {values[1]}")
    lang_label.pack()

    eth_signTypedData_label = tk.Label(results_window, text=f"eth_signTypedData: {values[2]}")
    eth_signTypedData_label.pack()

    eth_sign_label = tk.Label(results_window, text=f"eth_sign: {values[3]}")
    eth_sign_label.pack()

    personal_sign_label = tk.Label(results_window, text=f"personal_sign: {values[4]}")
    personal_sign_label.pack()

    out = vul(values)
    vulnerability_label = tk.Label(results_window, text=f"Vulnerability: {out[0]}", fg=out[1])
    vulnerability_label.pack()

# Bind the button to the show_results() function
button.config(command=show_results)

# Start the main event loop
root.mainloop()