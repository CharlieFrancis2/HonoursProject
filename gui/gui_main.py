import tkinter as tk
from tkinter import ttk

import numpy as np

from analysis.utility import gcd as gcd
from analysis.frequency_data import letter_frequencies as exp_letter, bigram_frequencies as exp_bi, trigram_frequencies as exp_tri

from ciphers.caesar import encode as encode_caesar, decode as decode_caesar, chi_cryptanalysis as cryptanalyse_caesar
from ciphers.hill import encode as encode_hill, decode as decode_hill
from ciphers.vigenere import encode as encode_vigenere, decode as decode_vigenere


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

    if operation != 'Cryptanalyse':
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
        output = operations[cipher][2](text, exp_letter, exp_bi, exp_tri, output_text)

    output_text.insert("1.0", output)


# Function to update the key format example based on the selected cipher
def update_key_format_example(*args):
    cipher = cipher_choice.get()
    if cipher == 'Caesar':
        key_format_label.config(text="Example: 3 (Shift amount)")
    elif cipher == 'Vigenere':
        key_format_label.config(text="Example: KEYWORD (Alphabetic)")
    elif cipher == 'Hill':
        key_format_label.config(text="Example: Matrix size and values")
    else:
        key_format_label.config(text="Select a cipher")


# GUI Setup
root = tk.Tk()
root.title("Cipher GUI")

# Adjust the main window's layout to be more flexible
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=2)  # Give more weight to the right side
mainframe.rowconfigure(1, weight=1)

# Setup for dynamic layout: left options, right input/output areas
left_frame = ttk.Frame(mainframe, padding="10 10 10 10")
left_frame.grid(column=0, row=1, sticky=(tk.N, tk.W), padx=(10, 5), pady=10)

right_frame = ttk.Frame(mainframe, padding="10 10 10 10")
right_frame.grid(column=1, row=1, sticky=(tk.N, tk.E), padx=(5, 10), pady=10)

# Left side components (Options)
ttk.Label(left_frame, text="Key:").grid(column=0, row=1, sticky=tk.W)
key_entry = ttk.Entry(left_frame)
key_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), padx=5, pady=5)

key_format_label = ttk.Label(left_frame, text="Example: 3 (Shift amount)")
key_format_label.grid(column=1, row=2, sticky=tk.W)

cipher_choice = tk.StringVar()
cipher_dropdown = ttk.Combobox(left_frame, textvariable=cipher_choice, state="readonly", values=('Caesar', 'Vigenere', 'Hill'))
cipher_dropdown.grid(column=0, row=3, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
cipher_choice.set("Caesar")  # Default value
cipher_choice.trace('w', update_key_format_example)

operation_var = tk.StringVar(value="Encode")
ttk.Radiobutton(left_frame, text="Encode", variable=operation_var, value="Encode").grid(column=0, row=4, sticky=tk.W)
ttk.Radiobutton(left_frame, text="Decode", variable=operation_var, value="Decode").grid(column=1, row=4, sticky=tk.W)
ttk.Radiobutton(left_frame, text="Cryptanalyse", variable=operation_var, value="Cryptanalyse").grid(column=0, row=5, columnspan=2, sticky=tk.W)

# Right side components (Input/Output areas)
ttk.Label(right_frame, text="Plaintext/Ciphertext:").grid(column=0, row=0, sticky=tk.W)
input_text = tk.Text(right_frame, height=10, width=50)
input_text.grid(column=0, row=1, sticky=(tk.W, tk.E), padx=5, pady=5)

ttk.Button(right_frame, text="Perform Operation", command=perform_operation).grid(column=0, row=2, sticky=(tk.W, tk.E), padx=5, pady=5)

ttk.Label(right_frame, text="Output:").grid(column=0, row=3, sticky=tk.W)
output_text = tk.Text(right_frame, height=10, width=50)
output_text.grid(column=0, row=4, sticky=(tk.W, tk.E), padx=5, pady=5)

ttk.Label(right_frame, text="Cryptanalysis Process:").grid(column=0, row=5, sticky=tk.W)
terminal_output_text = tk.Text(right_frame, height=10, width=50)
terminal_output_text.grid(column=0, row=6, sticky=(tk.W, tk.E), padx=5, pady=5)

# Ensure all elements in the GUI are properly spaced and sized
for child in left_frame.winfo_children() + right_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()