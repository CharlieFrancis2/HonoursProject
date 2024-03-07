import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import numpy as np
from tkinter import filedialog

# Importing cipher functions and analysis utilities
from analysis.utility import gcd
from analysis.frequency_data import letter_frequencies as exp_letter, bigram_frequencies as exp_bi, \
    trigram_frequencies as exp_tri
from ciphers.caesar import encode as encode_caesar, decode as decode_caesar, chi_cryptanalysis as cryptanalyse_caesar
from ciphers.hill import encode as encode_hill, decode as decode_hill
from ciphers.vigenere import encode as encode_vigenere, decode as decode_vigenere, cryptanalyse as cryptanalyse_vigenere

def cryptanalyse_hill(text):
    """Placeholder function for Hill cipher cryptanalysis."""
    pass


def upload_file():
    """Open a file dialog to upload a text file and set its content to the input_text widget."""
    filepath = filedialog.askopenfilename(
        title="Open a text file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )

    if filepath:  # if a file was selected
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
            input_text.delete("1.0", tk.END)  # Clear the current content
            input_text.insert(tk.END, text)  # Insert the text from the file


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
    global output
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
        if cipher == 'Caesar':
            output = operations[cipher][2](text, exp_letter, exp_bi, exp_tri, output_text)
        elif cipher == 'Vigenere':
            max_key_length = int(max_key_length_entry.get())
            operations[cipher][2](text, max_key_length, print_to_gui_terminal, update_output, update_status_callback)

    output_text.insert("1.0", output)


# Function to print to the terminal_output_text in the cipher_info_frame
def print_to_gui_terminal(message):
    """
    Appends a message to the cipher_info_text Text widget.
    """
    cipher_info_text.insert(tk.END, message + "\n")
    cipher_info_text.see(tk.END)
    root.update_idletasks()

def update_output(result):
    output_text.delete("1.0", "end")
    output_text.insert("1.0", result)

# Update this status label with a message like so:
def update_status_callback(message):
    status_label.configure(text=message)
    status_label.update_idletasks()


# Function to select a cipher and update the GUI accordingly
def select_cipher(cipher_name):
    # Update selected cipher
    cipher_choice.set(cipher_name)
    # Update key format example based on selected cipher
    update_key_format_example()
    # Print selection to terminal
    print_to_gui_terminal(f"Cipher selected: {cipher_name}")
    # Show or hide max key length input for Vigenere cipher
    if cipher_name == "Vigenere":
        max_key_length_label.pack(anchor=tk.W)
        max_key_length_entry.pack(padx=5, pady=5, fill=tk.X)
    else:
        max_key_length_label.pack_forget()
        max_key_length_entry.pack_forget()

# Function to update key format example based on the selected cipher
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
    elif cipher == 'Enigma':
        key_format_label.configure(text="Example: Enigma settings")
    else:
        key_format_label.configure(text="Select a cipher")

# GUI Setup
ctk.set_appearance_mode("dark")  # Set to "light" or "dark"
ctk.set_default_color_theme("dark-blue")  # Set color theme
root = ctk.CTk()  # Create a CTk window instead of Tk
root.title("Cipher GUI")
root.geometry("1000x800")

# Main frame configuration
mainframe = ctk.CTkFrame(root)
mainframe.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Cipher buttons frame at the top
cipher_buttons_frame = ctk.CTkFrame(mainframe)
cipher_buttons_frame.pack(side=tk.TOP, fill=tk.X)

# Cipher info frame on the right
cipher_info_frame = ctk.CTkFrame(mainframe)
cipher_info_frame.pack(side=tk.RIGHT, padx=(5, 10), pady=10, fill=tk.BOTH, expand=True)

# Cipher info panel
cipher_info_text = ctk.CTkTextbox(cipher_info_frame, height=10, width=50)
cipher_info_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

# Options frame on the left
options_frame = ctk.CTkFrame(mainframe)
options_frame.pack(side=tk.LEFT, padx=(10, 5), pady=10, fill=tk.BOTH, expand=True)


# Input/Output frame in the middle
io_frame = ctk.CTkFrame(mainframe)
io_frame.pack(side=tk.LEFT, padx=(5, 5), pady=10, fill=tk.BOTH, expand=True)

# Create a status label in your GUI setup
status_label = ctk.CTkLabel(cipher_info_frame, text="")
status_label.pack(padx=5, pady=5)

# Cipher selection variable
cipher_choice = tk.StringVar()

# Cipher buttons
ciphers = ["Caesar", "Vigenere", "Hill", "Enigma"]
cipher_buttons = {}
for cipher in ciphers:
    cipher_buttons[cipher] = ctk.CTkButton(cipher_buttons_frame, text=cipher, command=lambda c=cipher: select_cipher(c))
    cipher_buttons[cipher].pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

# Options components
ctk.CTkLabel(options_frame, text="Key:").pack(anchor=tk.W)
key_entry = ctk.CTkEntry(options_frame)
key_entry.pack(padx=5, pady=5, fill=tk.X)

key_format_label = ctk.CTkLabel(options_frame, text="Example: 3 (Shift amount)")
key_format_label.pack(anchor=tk.W)

operation_var = tk.StringVar(value="Encode")
ctk.CTkRadioButton(options_frame, text="Encode", variable=operation_var, value="Encode").pack(anchor=tk.W, padx=5, pady=5)
ctk.CTkRadioButton(options_frame, text="Decode", variable=operation_var, value="Decode").pack(anchor=tk.W, padx=5, pady=5)
ctk.CTkRadioButton(options_frame, text="Cryptanalyse", variable=operation_var, value="Cryptanalyse").pack(anchor=tk.W, padx=5, pady=5)

# Add an Upload File button to the left options frame
upload_button = ctk.CTkButton(options_frame, text="Upload File", command=upload_file)
upload_button.pack(padx=5, pady=5, fill=tk.X)

# Input/Output components
ctk.CTkLabel(io_frame, text="Plaintext/Ciphertext:").pack(anchor=tk.W)
input_text = ctk.CTkTextbox(io_frame, height=10, width=50)
input_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

ctk.CTkButton(io_frame, text="Perform Operation", command=perform_operation).pack(padx=5, pady=5, fill=tk.X)

output_text = ctk.CTkTextbox(io_frame, height=10, width=50)
output_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

# Additional components for Vigenere cipher in the cipher_info_frame
max_key_length_label = ctk.CTkLabel(cipher_info_frame, text="Max Key Length:")
max_key_length_entry = ctk.CTkEntry(cipher_info_frame)

# Initial cipher selection update
select_cipher("Caesar")

root.mainloop()


