import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import numpy as np

# Importing cipher functions and analysis utilities
from analysis.utility import gcd
from analysis.frequency_data import letter_frequencies as exp_letter, bigram_frequencies as exp_bi, \
    trigram_frequencies as exp_tri
from ciphers.caesar import encode as encode_caesar, decode as decode_caesar, chi_cryptanalysis as cryptanalyse_caesar
from ciphers.hill import encode as encode_hill, decode as decode_hill
from ciphers.vigenere import encode as encode_vigenere, decode as decode_vigenere


def cryptanalyse_vigenere(text):
    """Placeholder function for Vigenère cipher cryptanalysis."""
    pass


def cryptanalyse_hill(text):
    """Placeholder function for Hill cipher cryptanalysis."""
    pass


def validate_and_convert_hill_key(key_str):
    """
    Validates and converts a Hill cipher key string into a matrix.

    Args:
        key_str (str): The key as a string, which can be numeric with spaces, purely numeric, or alphabetic.

    Returns:
        tuple: (bool, np.array or None) Indicates whether the key is valid and the key matrix or None if invalid.
    """
    # Numeric key with spaces, numeric keys without spaces, or alphabetic keys are handled differently
    if " " in key_str:
        key = [int(num) for num in key_str.split()]
    elif all(char.isdigit() for char in key_str):
        key = [int(char) for char in key_str]
    elif all(char.isalpha() for char in key_str):
        key = [ord(char.upper()) - ord('A') for char in key_str]
    else:
        return False, None  # Invalid key format

    # Check if key length forms a perfect square matrix
    n = int(np.sqrt(len(key)))
    if n ** 2 != len(key):
        return False, None

    # Create key matrix and validate its determinant
    key_matrix = np.array(key).reshape(n, n)
    determinant = int(round(np.linalg.det(key_matrix))) % 26
    if determinant == 0 or gcd(determinant, 26) != 1:
        return False, None

    return True, key_matrix


def perform_operation():
    """
    Performs the selected cipher operation (encode, decode, cryptanalyse) based on user input.
    """
    text = input_text.get("1.0", "end-1c")
    key_str = key_entry.get()
    cipher = cipher_choice.get()
    operation = operation_var.get()
    output_text.delete("1.0", "end")

    # Validate key and perform the selected operation
    if operation != 'Cryptanalyse':
        if cipher == 'Caesar':
            try:
                key = int(key_str)
            except ValueError:
                output_text.insert("1.0", "Invalid key for Caesar cipher: must be an integer")
                return
        elif cipher == 'Vigenere':
            if not key_str.isalpha():
                output_text.insert("1.0", "Invalid key for Vigenere cipher: must contain only letters")
                return
            key = key_str
        elif cipher == 'Hill':
            valid, key_matrix = validate_and_convert_hill_key(key_str)
            if not valid:
                output_text.insert("1.0", "Invalid key for Hill cipher: must be a valid matrix format")
                return
            key = key_matrix
        else:
            output_text.insert("1.0", "Cipher not supported.")
            return

    # Mapping GUI choices to cipher functions and performing the operation
    operations = {
        'Caesar': (encode_caesar, decode_caesar, cryptanalyse_caesar),
        'Vigenere': (encode_vigenere, decode_vigenere, cryptanalyse_vigenere),
        'Hill': (encode_hill, decode_hill, cryptanalyse_hill),
    }

    if operation == 'Encode':
        output = operations[cipher][0](text, key)
    elif operation == 'Decode':
        output = operations[cipher][1](text, key)
    else:  # Cryptanalyse is a separate path, potentially requiring different parameters
        output = operations[cipher][2](text, exp_letter, exp_bi, exp_tri, output_text)

    output_text.insert("1.0", output)


def update_key_format_example(*args):
    """
    Updates the key format example label based on the selected cipher type.
    """
    cipher = cipher_choice.get()
    if cipher == 'Caesar':
        key_format_label.configure(text="Example: 3 (Shift amount)")
    elif cipher == 'Vigenere':
        key_format_label.configure(text="Example: KEYWORD (Alphabetic)")
    elif cipher == 'Hill':
        key_format_label.configure(text="Example: Matrix size and values")
    else:
        key_format_label.configure(text="Select a cipher")


def print_to_gui_terminal(message):
    """
    Appends a message to the terminal_output_text Text widget.
    """
    terminal_output_text.insert(tk.END, message + "\n")
    terminal_output_text.see(tk.END)
    root.update_idletasks()


# GUI Setup
ctk.set_appearance_mode("dark")  # Set to "light" or "dark"
ctk.set_default_color_theme("dark-blue")  # Set color theme
root = ctk.CTk()  # Create a CTk window instead of Tk
root.title("Cipher GUI")

# Setting the initial size to a square of 800x800 pixels
root.geometry("1000x800")

# Main frame configuration (without padding argument)
mainframe = ctk.CTkFrame(root)
mainframe.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  # Manage padding here

# Left frame for options (without padding argument, manage padding during packing)
left_frame = ctk.CTkFrame(mainframe)
left_frame.pack(side=tk.LEFT, padx=(10, 5), pady=10, fill=tk.BOTH, expand=True)

# Right frame for input/output areas (without padding argument, manage padding during packing)
right_frame = ctk.CTkFrame(mainframe)
right_frame.pack(side=tk.RIGHT, padx=(5, 10), pady=10, fill=tk.BOTH, expand=True)

# Left side components: Key entry and cipher selection
ctk.CTkLabel(left_frame, text="Key:").pack(anchor=tk.W)
key_entry = ctk.CTkEntry(left_frame)
key_entry.pack(padx=5, pady=5, fill=tk.X)

key_format_label = ctk.CTkLabel(left_frame, text="Example: 3 (Shift amount)")
key_format_label.pack(anchor=tk.W)

cipher_choice = tk.StringVar()
cipher_dropdown = ctk.CTkOptionMenu(left_frame, variable=cipher_choice, values=('Caesar', 'Vigenere', 'Hill'))
cipher_dropdown.pack(padx=5, pady=5, fill=tk.X)
cipher_choice.set("Caesar")
cipher_choice.trace('w', update_key_format_example)

operation_var = tk.StringVar(value="Encode")
ctk.CTkRadioButton(left_frame, text="Encode", variable=operation_var, value="Encode").pack(anchor=tk.W, padx=5, pady=5)
ctk.CTkRadioButton(left_frame, text="Decode", variable=operation_var, value="Decode").pack(anchor=tk.W, padx=5, pady=5)
ctk.CTkRadioButton(left_frame, text="Cryptanalyse", variable=operation_var, value="Cryptanalyse").pack(anchor=tk.W, padx=5, pady=5)

# Right side components: Input and output areas
ctk.CTkLabel(right_frame, text="Plaintext/Ciphertext:").pack(anchor=tk.W)
input_text = ctk.CTkTextbox(right_frame, height=10, width=50)
input_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

ctk.CTkButton(right_frame, text="Perform Operation", command=perform_operation).pack(padx=5, pady=5, fill=tk.X)

ctk.CTkLabel(right_frame, text="Output:").pack(anchor=tk.W)
output_text = ctk.CTkTextbox(right_frame, height=10, width=50)
output_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

ctk.CTkLabel(right_frame, text="Cryptanalysis Process:").pack(anchor=tk.W)
terminal_output_text = ctk.CTkTextbox(right_frame, height=10, width=50)
terminal_output_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()
