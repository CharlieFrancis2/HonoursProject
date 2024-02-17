import tkinter as tk
from tkinter import ttk

import numpy as np

from analysis.utility import gcd as gcd
from ciphers.caesar import encode as encode_caesar, decode as decode_caesar
from ciphers.hill import encode as encode_hill, decode as decode_hill
from ciphers.vigenere import encode as encode_vigenere, decode as decode_vigenere


def cryptanalyse_caesar(text):
    pass


def cryptanalyse_vigenere(text):
    pass


def cryptanalyse_hill(text):
    pass


def validate_and_convert_hill_key(key_str):
    if " " in key_str:  # Numeric key with spaces
        key = [int(num) for num in key_str.split()]
    elif all(char.isdigit() for char in key_str):  # Handle numeric keys without spaces
        # This path might be less common if you expect spaces between numbers
        key = [int(char) for char in key_str]
    elif all(char.isalpha() for char in key_str):  # Alphabetic key
        key = [ord(char.upper()) - ord('A') for char in key_str]
    else:
        return False, None  # Invalid key format

    n = int(np.sqrt(len(key)))
    if n ** 2 != len(key):
        return False, None  # Key length doesn't form a perfect square matrix

    key_matrix = np.array(key).reshape(n, n)
    determinant = int(round(np.linalg.det(key_matrix))) % 26
    if determinant == 0 or gcd(determinant, 26) != 1:
        return False, None  # Determinant has no inverse modulo 26

    return True, key_matrix


def perform_operation():
    text = input_text.get("1.0", "end-1c")
    key_str = key_entry.get()  # This is the key as a string
    cipher = cipher_choice.get()
    operation = operation_var.get()
    output_text.delete("1.0", "end")

    # Different key validation and conversion for each cipher type
    if cipher == 'Caesar':
        try:
            key = int(key_str)  # Caesar cipher expects an integer key
        except ValueError:
            output_text.insert("1.0", "Invalid key for Caesar cipher: must be an integer")
            return
    elif cipher == 'Vigenere':
        if not key_str.isalpha():  # Vigenere cipher expects a string of alphabets
            output_text.insert("1.0", "Invalid key for Vigenere cipher: must contain only letters")
            return
        key = key_str  # Use the string directly
    elif cipher == 'Hill':
        valid, key_matrix = validate_and_convert_hill_key(key_str)
        if not valid:
            output_text.insert("1.0", "Invalid key for Hill cipher: must be a valid matrix format")
            return
        key = key_matrix  # Use the validated and converted matrix
    else:
        output_text.insert("1.0", "Cipher not supported.")
        return

    # Mapping GUI choices to cipher functions
    operations = {
        'Caesar': (encode_caesar, decode_caesar, cryptanalyse_caesar),
        'Vigenere': (encode_vigenere, decode_vigenere, cryptanalyse_vigenere),
        'Hill': (encode_hill, decode_hill, cryptanalyse_hill),
    }

    if operation == 'Encode':
        output = operations[cipher][0](text, key)
    elif operation == 'Decode':
        output = operations[cipher][1](text, key)
    else:
        output = operations[cipher][2](text)

    output_text.insert("1.0", output)


root = tk.Tk()
root.title("Cipher GUI")

# Setup GUI layout
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Key:").grid(column=0, row=0, sticky=tk.W)
key_entry = ttk.Entry(mainframe)
key_entry.grid(column=2, row=0, sticky=(tk.W, tk.E))

key_format_label = ttk.Label(mainframe, text="")
key_format_label.grid(column=0, row=1, sticky=(tk.W, tk.E), columnspan=3)

cipher_choice = tk.StringVar()
cipher_dropdown = ttk.Combobox(mainframe, textvariable=cipher_choice, state="readonly",
                               values=('Caesar', 'Vigenere', 'Hill'))
cipher_dropdown.grid(column=0, row=2, sticky=(tk.W, tk.E))
cipher_choice.set("Caesar")  # default value

operation_var = tk.StringVar(value="Encode")
ttk.Radiobutton(mainframe, text="Encode", variable=operation_var, value="Encode").grid(column=2, row=1, sticky=tk.W)
ttk.Radiobutton(mainframe, text="Decode", variable=operation_var, value="Decode").grid(column=2, row=2, sticky=tk.W)
ttk.Radiobutton(mainframe, text="Cryptanalyse", variable=operation_var, value="Cryptanalyse").grid(column=2, row=3,
                                                                                                   sticky=tk.W)

input_text = tk.Text(mainframe, height=10, width=50)
input_text.grid(column=0, row=3, columnspan=3, sticky=(tk.W, tk.E))

ttk.Button(mainframe, text="Perform Operation", command=perform_operation).grid(column=1, row=4, sticky=(tk.W, tk.E))

output_text = tk.Text(mainframe, height=10, width=50)
output_text.grid(column=0, row=6, columnspan=3, sticky=(tk.W, tk.E))

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)


def update_key_format_example(*args):
    cipher = cipher_choice.get()
    if cipher == 'Caesar':
        key_format_label.config(text="Example Key: 3")
    elif cipher == 'Vigenere':
        key_format_label.config(text="Example Key: KEYWORD")
    elif cipher == 'Hill':
        key_format_label.config(text="Example Key: 5 17 8 3 or BALL")
    else:
        key_format_label.config(text="")


cipher_choice.trace('w', update_key_format_example)

root.mainloop()
