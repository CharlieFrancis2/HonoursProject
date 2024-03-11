import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

# Import cipher functions and analysis utilities
from analysis.utility import gcd
from analysis.frequency_data import letter_frequencies as exp_letter, bigram_frequencies as exp_bi, \
    trigram_frequencies as exp_tri
from ciphers.caesar import encode as encode_caesar, decode as decode_caesar, chi_cryptanalysis as cryptanalyse_caesar
from ciphers.hill import encode as encode_hill, decode as decode_hill
from ciphers.vigenere import encode as encode_vigenere, decode as decode_vigenere, cryptanalyse as cryptanalyse_vigenere

# TODO:
#   Flesh out Caesar information
#   Flesh out Vigenere information
#   Implement Vigenere AutoKey
#   Implement Hill Cryptanalysis
#   Implement Enigma encoding/decoding
#   Multiple Language Support
#   File Format compatability
#   Continue refining gui


def cryptanalyse_hill(text):
    """Placeholder function for Hill cipher cryptanalysis."""
    pass


def upload_file():
    filepath = filedialog.askopenfilename(title="Open a text file",
                                          filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, text)


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
    text = input_text.get("1.0", "end-1c").strip()  # Adjust widget variable name as necessary
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
        print_to_gui_terminal(f"Encoding with key:\n{key}")
        output = operations[cipher][0](text, key, print_to_gui_terminal)
    elif operation == 'Decode':
        print_to_gui_terminal(f"Decoding with key:\n{key}")
        output = operations[cipher][1](text, key, print_to_gui_terminal)
    else:  # Cryptanalyse is a separate path, potentially requiring different parameters
        if cipher == 'Caesar':
            output = operations[cipher][2](text, exp_letter, exp_bi, exp_tri, output_text, print_to_gui_terminal)
        elif cipher == 'Vigenere':
            output_text.delete("1.0", tk.END)  # Clear existing text
            max_key_length = int(max_key_length_entry.get())
            output = operations[cipher][2](text, max_key_length, print_to_gui_terminal, output_text,
                                           update_status_callback)

    output_text.insert("1.0", output)


def print_to_gui_terminal(message):
    cipher_info_text.insert(tk.END, message + "\n")
    cipher_info_text.see(tk.END)


def update_output(result):
    output_text.delete("1.0", "end")
    output_text.insert("1.0", result)


def update_status_callback(message):
    status_label.config(text=message)


def update_key_format_example():
    cipher = cipher_choice.get()
    if cipher == 'Caesar':
        key_format_label.config(text="Example: 3 (Shift amount)")
    elif cipher == 'Vigenere':
        key_format_label.config(text="Example: KEYWORD (Alphabetic)")
    elif cipher == 'Hill':
        key_format_label.config(text="Example: 5 17 4 15 (Matrix format)")
    elif cipher == 'Enigma':  # Assuming 'Enigma' is part of your ciphers for demonstration
        key_format_label.config(text="Example: Enigma settings")
    else:
        key_format_label.config(text="Select a cipher")


def clear_input():
    input_text.delete("1.0", tk.END)


def clear_output():
    output_text.delete("1.0", tk.END)


def swap_io_content():
    input_content = input_text.get("1.0", tk.END)
    output_content = output_text.get("1.0", tk.END)
    clear_input()
    clear_output()
    input_text.insert(tk.END, output_content)
    output_text.insert(tk.END, input_content)


# Initialize main application window
root = tk.Tk()
root.title("Cipher GUI")
root.geometry("1920x1080")
background_color = '#262626'
foreground_color = '#FFFFFF'
button_color = '#032f42'
text_color = '#FFFFFF'
input_bg = '#23272A'
text_widget_bg = '#23272A'
root.configure(bg=background_color)

# Main frame configuration
mainframe = tk.Frame(root, bg=background_color)
mainframe.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Widget Styles
font_style = ('Arial', 10)
mono_font_style = ('Courier', 10)
button_style = {'font': font_style, 'bg': button_color, 'fg': text_color, 'activebackground': button_color,
                'activeforeground': text_color}
label_style = {'font': font_style, 'bg': background_color, 'fg': foreground_color}
entry_style = {'font': font_style, 'bg': input_bg, 'fg': text_color, 'insertbackground': text_color}
entry_style2 = {'font': mono_font_style, 'bg': input_bg, 'fg': text_color, 'insertbackground': text_color}
text_style = {'font': font_style, 'bg': text_widget_bg, 'fg': text_color}

# Cipher selection
cipher_choice = tk.StringVar(value="Caesar")
operation_var = tk.StringVar(value="Encode")
cipher_buttons = {}
ciphers = ["Caesar", "Vigenere", "Hill", "Enigma"]
text_buttons = ["Clear Input", "Clear Output", "Swap I/O"]

# Layout Configuration
cipher_buttons_frame = tk.Frame(mainframe, bg=background_color)
cipher_buttons_frame.pack(side=tk.TOP, fill=tk.X)

options_frame = tk.Frame(mainframe, bg=background_color, width=250)
options_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10)
options_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its contents

io_frame = tk.Frame(mainframe, bg=background_color)
io_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

cipher_info_frame = tk.Frame(mainframe, bg=background_color)
cipher_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10)

# Ensure cipher_buttons span the width of the window
for cipher in ciphers:
    # Assuming 'ciphers' is a list of cipher names and 'cipher_buttons_frame' is the parent widget
    btn = tk.Button(cipher_buttons_frame, text=cipher, command=lambda c=cipher: select_cipher(c), **button_style)
    btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    cipher_buttons[cipher] = btn

# Operation radio buttons
for operation in ["Encode", "Decode", "Cryptanalyse"]:
    tk.Radiobutton(options_frame, text=operation, variable=operation_var, value=operation, **label_style,
                   selectcolor=background_color).pack(anchor=tk.W, padx=5, pady=2)

# Key entry
tk.Label(options_frame, text="Key:", **label_style).pack(anchor=tk.W)
key_entry = tk.Entry(options_frame, **entry_style)
key_entry.pack(padx=5, pady=5, fill=tk.X)

# Define label for key format example
key_format_label = tk.Label(options_frame, bg=background_color, fg=foreground_color)
key_format_label.pack(anchor=tk.W)
key_format_label.config(font=font_style)
update_key_format_example()  # Initialize with the default cipher's key format

# Max key length for Vigenere cipher - initially hidden
max_key_length_label = tk.Label(options_frame, text="Max Key Length (Vigenere only):", **label_style)
max_key_length_entry = tk.Entry(options_frame, **entry_style)

# Status label and cipher info text box
status_label = tk.Label(cipher_info_frame, text="Status updates appear here", **label_style)
status_label.pack(padx=5, pady=0)

cipher_info_text = tk.Text(cipher_info_frame, height=10, width=50, **entry_style2)
cipher_info_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

# Now, create and pack the file upload button at the bottom of the options_frame
upload_button = tk.Button(options_frame, text="Upload File", command=upload_file, **button_style)
upload_button.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=0)

# Input and output text boxes
tk.Label(io_frame, text="Plaintext/Ciphertext:", **label_style).pack(anchor=tk.W)
input_text = tk.Text(io_frame, height=10, width=50, **text_style)
input_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

perform_button = tk.Button(io_frame, text="Perform Operation", command=perform_operation, **button_style)
perform_button.pack(padx=5, pady=5, fill=tk.X)

output_text = tk.Text(io_frame, height=10, width=50, **text_style)
output_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

text_buttons_frame = tk.Frame(io_frame, bg=background_color)
text_buttons_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, padx=10)

clear_input_button = tk.Button(text_buttons_frame, text="Clear Input", command=clear_input, **button_style)
clear_input_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

clear_output_button = tk.Button(text_buttons_frame, text="Clear Output", command=clear_output, **button_style)
clear_output_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

swap_button = tk.Button(text_buttons_frame, text="Swap I/O", command=swap_io_content, **button_style)
swap_button.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)


def select_cipher(cipher_name):
    cipher_choice.set(cipher_name)
    # Logic for showing/hiding Vigenere max key length entry
    if cipher_name == "Vigenere":
        max_key_length_label.pack(anchor=tk.W)
        max_key_length_entry.pack(padx=5, pady=5, fill=tk.X)
    else:
        max_key_length_label.pack_forget()
        max_key_length_entry.pack_forget()

    # Define a color for the pressed button
    pressed_button_color = '#0a4f67'  # A darker shade, adjust this color as needed

    # Update button styles for all buttons, showing the selected one as 'pressed'
    for cipher, btn in cipher_buttons.items():
        if cipher == cipher_name:
            btn.config(relief=tk.SUNKEN, bg=pressed_button_color)  # Selected button looks 'pressed' with a unique color
        else:
            btn.config(relief=tk.RAISED, bg=button_color)  # Other buttons revert to their original color

    update_key_format_example()


select_cipher("Caesar")  # Example: Select 'Caesar' cipher by default

root.mainloop()
