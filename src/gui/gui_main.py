import threading
import tkinter as tk
from tkinter import filedialog

# Import cipher functions and analysis utilities
import analysis.utility as util
from analysis.frequency_data import letter_frequencies as exp_letter, bigram_frequencies as exp_bi, \
    trigram_frequencies as exp_tri
from ciphers.caesar import encode as encode_caesar, decode as decode_caesar, chi_cryptanalysis as cryptanalyse_caesar
from ciphers.hill import (encode as encode_hill, decode as decode_hill, cryptanalyse as cryptanalyse_hill, \
                          generate_key as generate_hill, extract_and_trim as extract_known)
from ciphers.vigenere import encode as encode_vigenere, decode as decode_vigenere, cryptanalyse as cryptanalyse_vigenere


def upload_file():
    filepath = filedialog.askopenfilename(title="Open a text file",
                                          filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, text)


def start_operation_in_thread(operation, callback, *args):
    """
    Starts the specified operation in a separate thread and uses a callback function to handle the result.
    """

    def operation_wrapper():
        try:
            result = operation(*args)
            root.after(0, callback, result)
        except Exception as e:
            print(f"Error during operation: {e}")
            root.after(0, callback, f"Error: {e}")

    operation_thread = threading.Thread(target=operation_wrapper)
    operation_thread.daemon = True
    operation_thread.start()


def update_output_text(result):
    if result is None:
        result_str = "No results to display."
    elif isinstance(result, list):
        # Assuming the list might contain lists (matrices) or other elements
        result_str = "\n".join(' '.join(map(str, row)) if isinstance(row, list) else str(row) for row in result)
    else:
        result_str = str(result)

    output_text.delete("1.0", "end")
    output_text.insert("1.0", result_str)


def perform_operation():
    # Retrieve the user-inputted text from the GUI text field. Validate to ensure it is not empty.
    text = input_text.get("1.0", "end-1c").strip()
    if not text:
        output_text.insert("1.0", "Error: Input text cannot be empty. Please provide some text to proceed.")
        return

    # Retrieve the key from the GUI input field
    key_str = key_entry.get()
    # Retrieve the currently selected cipher and operation from the GUI
    cipher = cipher_choice.get()
    operation = operation_var.get()

    # Clear the output text area to prepare for new output
    output_text.delete("1.0", "end")

    # Perform input validation for the key based on the selected cipher
    if operation != 'Cryptanalyse':
        if cipher == 'Caesar':
            try:
                key = int(key_str)  # The key for Caesar cipher must be an integer
            except ValueError:
                output_text.insert("1.0", "Invalid key for Caesar cipher: must be an integer")
                return
        elif cipher == 'Vigenere':
            if not key_str.isalpha():  # The key for Vigenere cipher must only contain alphabetic characters
                output_text.insert("1.0", "Invalid key for Vigenere cipher: must contain only letters")
                return
            key = key_str
        elif cipher == 'Hill':
            # Validate the matrix key format for Hill cipher
            valid, key_matrix = util.validate_and_convert_hill_key(key_str)
            if not valid:
                output_text.insert("1.0", "Invalid key for Hill cipher: must be a valid matrix format")
                return
            key = key_matrix
        else:
            output_text.insert("1.0", "Cipher not supported.")  # Inform user if the selected cipher is not supported
            return

    # Mapping of cipher types to their corresponding encoding, decoding, and cryptanalysis functions
    operations = {
        'Caesar': (encode_caesar, decode_caesar, cryptanalyse_caesar),
        'Vigenere': (encode_vigenere, decode_vigenere, cryptanalyse_vigenere),
        'Hill': (encode_hill, decode_hill, cryptanalyse_hill),
    }

    # Execute the selected operation in a separate thread to keep UI responsive
    if operation == 'Encode':
        start_operation_in_thread(operations[cipher][0], update_output_text, text, key, update_terminal)
    elif operation == 'Decode':
        start_operation_in_thread(operations[cipher][1], update_output_text, text, key, update_terminal)
    elif operation == 'Cryptanalyse':
        if cipher == 'Caesar':
            start_operation_in_thread(operations[cipher][2], update_output_text, text, exp_letter, exp_bi, exp_tri)
        elif cipher == 'Vigenere':
            # Validate and retrieve additional inputs for Vigenere cipher cryptanalysis
            try:
                max_key_length = int(max_key_length_entry.get().strip())
                key_length_guesses = int(key_length_guesses_entry.get().strip())
                shift_guesses = int(shift_guesses_entry.get().strip())
                if max_key_length <= 0 or key_length_guesses <= 0 or shift_guesses <= 0:
                    output_text.insert("1.0", "Error: Key length and shift guesses must be positive integers.")
                    return
            except ValueError:
                output_text.insert("1.0", "Invalid input: Max key length, key length guesses, and shift guesses must be integers.")
                return
            additional_args = (max_key_length, key_length_guesses, shift_guesses)
            start_operation_in_thread(operations[cipher][2], update_output_text, text, *additional_args,
                                      update_terminal, update_output_text, update_status_callback)
        elif cipher == 'Hill':
            known = known_plaintext_entry.get("1.0", "end-1c").strip()  # Get the known plaintext for Hill cryptanalysis
            known = util.prepare_text(known)
            try:
                start_index = int(start_index_entry.get().strip())
                matrix_size = int(matrix_size_entry.get().strip())
                if start_index < 0 or matrix_size <= 0:
                    output_text.insert("1.0", "Error: Start index must be non-negative and matrix size must be positive.")
                    return
            except ValueError:
                output_text.insert("1.0", "Invalid input: Start index and matrix size must be integers.")
                return

            trimmed_known_text = extract_known(known, start_index, matrix_size)
            if not trimmed_known_text:
                output_text.insert("1.0", "Insufficient known plaintext for analysis.")
                return
            start_operation_in_thread(operations['Hill'][2], update_output_text, trimmed_known_text, text, matrix_size,
                                      start_index, update_output_text, update_terminal)
        else:
            output_text.insert("1.0", "Cryptanalysis not supported for this cipher.")




def update_terminal(message):
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


# Initialize the main application window
root = tk.Tk()
root.title("Cipher GUI")
root.geometry("1920x1080")
root.configure(bg='#262626')  # Set background color for the app

# Define color and font styles for consistency
background_color = '#262626'
foreground_color = '#FFFFFF'
button_color = '#032f42'
input_bg = '#23272A'
text_widget_bg = '#23272A'

font_style = ('Arial', 10)
label_font = ('Arial', 8)
mono_font_style = ('Courier', 10)

# Widget styles for buttons, labels, entries, and texts
button_style = {
    'font': font_style, 'bg': button_color, 'fg': foreground_color,
    'activebackground': button_color, 'activeforeground': foreground_color
}
label_style = {
    'font': label_font, 'bg': background_color, 'fg': foreground_color
}
entry_style = {
    'font': font_style, 'bg': input_bg, 'fg': foreground_color, 'insertbackground': foreground_color
}
entry_style2 = {
    'font': mono_font_style, 'bg': input_bg, 'fg': foreground_color, 'insertbackground': foreground_color
}
text_style = {
    'font': font_style, 'bg': text_widget_bg, 'fg': foreground_color
}
text_style2 = {
    'font': font_style, 'bg': background_color, 'fg': foreground_color
}

# Main frame configuration
mainframe = tk.Frame(root, bg=background_color)
mainframe.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Cipher selection and operation variables
cipher_choice = tk.StringVar(value="Caesar")
operation_var = tk.StringVar(value="Encode")

# Layout frames for cipher buttons, options, IO, and cipher info
cipher_buttons_frame = tk.Frame(mainframe, bg=background_color)
cipher_buttons_frame.pack(side=tk.TOP, fill=tk.X)

options_frame = tk.Frame(mainframe, bg=background_color, width=250)
options_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10)
options_frame.pack_propagate(False)

io_frame = tk.Frame(mainframe, bg=background_color)
io_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

cipher_info_frame = tk.Frame(mainframe, bg=background_color)
cipher_info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10)

# Cipher buttons configuration
ciphers = ["Caesar", "Vigenere", "Hill"]
cipher_buttons = {}
for cipher in ciphers:
    btn = tk.Button(cipher_buttons_frame, text=cipher, command=lambda c=cipher: select_cipher(c), **label_style)
    btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    cipher_buttons[cipher] = btn

# Operation selection (Encode, Decode, Cryptanalyse)
for operation in ["Encode", "Decode", "Cryptanalyse"]:
    tk.Radiobutton(options_frame, text=operation, variable=operation_var, value=operation, **text_style,
                   selectcolor=background_color).pack(anchor=tk.W, padx=5, pady=2)

# Key input with label
tk.Label(options_frame, text="Key:", **label_style).pack(anchor=tk.W)
key_entry = tk.Entry(options_frame, **entry_style)
key_entry.pack(padx=5, pady=5, fill=tk.X)

# Cipher-specific options - initially hidden
# Define label for key format example, will be updated based on the selected cipher
key_format_label = tk.Label(options_frame, text="Example: 3 (Shift amount)", **label_style)
key_format_label.pack(anchor=tk.W, pady=(0, 0))
key_format_label.config(font=label_font)
# key_format_label.pack_forget()  # Initially hide the label

# Define entries for maximum key length, key length guesses, and shift guesses
# These widgets will be shown or hidden based on the selected cipher

# Max key length for Vigenere cipher - initially hidden
max_key_length_label = tk.Label(options_frame, text="Max Key Length (Vigenere only):", **label_style)
max_key_length_entry = tk.Entry(options_frame, **entry_style)
max_key_length_label.pack(anchor=tk.W, pady=(5, 0))
max_key_length_entry.pack(padx=5, pady=(0, 5), fill=tk.X)
max_key_length_label.pack_forget()  # Initially hide
max_key_length_entry.pack_forget()  # Initially hide

# Key length guesses for certain ciphers - initially hidden
key_length_guesses_label = tk.Label(options_frame, text="Key Length Guesses:", **label_style)
key_length_guesses_entry = tk.Entry(options_frame, **entry_style)
key_length_guesses_label.pack(anchor=tk.W, pady=(5, 0))
key_length_guesses_entry.pack(padx=5, pady=(0, 5), fill=tk.X)
key_length_guesses_label.pack_forget()  # Initially hide
key_length_guesses_entry.pack_forget()  # Initially hide

# Shift guesses for Caesar cipher - initially hidden
shift_guesses_label = tk.Label(options_frame, text="Shift Guesses:", **label_style)
shift_guesses_entry = tk.Entry(options_frame, **entry_style)
shift_guesses_label.pack(anchor=tk.W, pady=(5, 0))
shift_guesses_entry.pack(padx=5, pady=(0, 5), fill=tk.X)
shift_guesses_label.pack_forget()  # Initially hide
shift_guesses_entry.pack_forget()  # Initially hide

# Hill cipher key generation button - initially hidden
generate_hill_button = tk.Button(options_frame, text="Generate Hill Key",
                                 command=lambda: hill_key_generated(matrix_size_entry.get()), **button_style)
generate_hill_button.pack(padx=5, pady=(5, 5), fill=tk.X)
generate_hill_button.pack_forget()  # Initially hide this button

matrix_size_label = tk.Label(options_frame, text="Matrix Size (n):", **label_style)
matrix_size_entry = tk.Entry(options_frame, **entry_style)
matrix_size_label.pack(anchor=tk.W, pady=(5, 0))
matrix_size_entry.pack(padx=5, pady=(0, 5), fill=tk.X)
matrix_size_label.pack_forget()  # Initially hide
matrix_size_entry.pack_forget()  # Initially hide

# Known plaintext entry for Hill cipher - initially hidden
known_plaintext_label = tk.Label(options_frame, text="Known Plaintext (Hill):", **label_style)
known_plaintext_entry = tk.Text(options_frame, height=4, width=20, **entry_style)  # Adjust size as needed

# Place these widgets in the GUI but keep them hidden initially
known_plaintext_label.pack(anchor=tk.W, pady=(5, 0))
known_plaintext_entry.pack(padx=5, pady=(0, 5), fill=tk.BOTH, expand=True)
known_plaintext_label.pack_forget()  # Initially hide
known_plaintext_entry.pack_forget()  # Initially hide

# Label and entry for start index (Hill cipher)
start_index_label = tk.Label(options_frame, text="Start Index (Hill):", **label_style)
start_index_entry = tk.Entry(options_frame, **entry_style)
start_index_label.pack(anchor=tk.W, pady=(5, 0))
start_index_entry.pack(padx=5, pady=(0, 5), fill=tk.X)
start_index_label.pack_forget()  # Initially hide
start_index_entry.pack_forget()  # Initially hide

start_index = 0


def hill_key_generated(n):
    """
    Generates a Hill cipher key for the specified matrix size and displays it.

    Args:
    - n (str): The size of the matrix, which should be a positive integer.
    """
    try:
        matrix_size = int(n)  # Attempt to convert the matrix size to an integer
        if matrix_size <= 0:
            # If the matrix size is zero or negative, display an error message
            update_output_text("Error: Key size must be a positive integer.")
            return
    except ValueError:
        # If conversion fails, it means the input was not an integer
        update_output_text("Error: Key size must be an integer.")
        return

    # If matrix_size is valid, proceed to generate the key
    try:
        key_matrix = generate_hill(matrix_size)
        if key_matrix is None:
            # If no matrix is returned, it indicates failure in generating an invertible matrix
            update_output_text("Failed to generate an invertible matrix. Please try a different size.")
            return

        key_entry.delete(0, tk.END)  # Clear the existing entry
        key_entry.insert(0, key_matrix)  # Display the generated key
    except Exception as e:
        # Handle any other exceptions that may occur
        update_output_text(f"An error occurred during key generation: {str(e)}")


# Cipher information display area with initial info and status updates
cipher_info_text1 = tk.Text(cipher_info_frame, height=5, width=50, bd=0, highlightthickness=0, wrap=tk.WORD,
                            **text_style2)
cipher_info_text1.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
cipher_info_text1.insert(tk.END, "Current Cipher: Caesar")
cipher_info_text1.config(state=tk.DISABLED)

status_label = tk.Label(cipher_info_frame, text="Status updates appear here", **label_style)
status_label.pack(padx=5, pady=0)

# Main cipher information text box with scrollbar
cipher_info_text = tk.Text(cipher_info_frame, height=33, width=50, **entry_style2)
scroll_bar = tk.Scrollbar(cipher_info_frame, command=cipher_info_text.yview)
cipher_info_text.config(yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
cipher_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# File upload button
upload_button = tk.Button(options_frame, text="Upload File", command=upload_file, **button_style)
upload_button.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=0)

# Plaintext/Ciphertext input and output areas with perform operation button
tk.Label(io_frame, text="Plaintext/Ciphertext:", **label_style).pack(anchor=tk.W)
input_text = tk.Text(io_frame, height=10, width=50, **entry_style)
input_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

perform_button = tk.Button(io_frame, text="Perform Operation", command=perform_operation, **button_style)
perform_button.pack(padx=5, pady=5, fill=tk.X)

output_text = tk.Text(io_frame, height=10, width=50, **entry_style)
output_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

# Buttons for text manipulation: clear input/output, swap I/O
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

    cipher_descriptions = {
        "Caesar": "The Caesar cipher, named after Julius Caesar who reportedly used it for his private "
                  "correspondence, is one of the oldest known encryption techniques."
                  "\n"
                  "\n"
                  "It's a type of substitution cipher where each letter in the plaintext is shifted a certain number "
                  "of places down or up the alphabet. For instance, with a shift of 3, 'A' would be replaced by 'D', "
                  "'B' would become 'E', and so forth, making it a straightforward yet elegant method for encoding "
                  "messages."
                  "\n"
                  "\n"
                  "The Caesar cipher is easily cracked due to its simplicity, but it lays the foundational concept "
                  "for more complex ciphers."
                  " Example:\nPlain: A B C D E \nCipher(+3): D E F G H\n"
                  "\n"
                  "Cryptanalysis Method:\n"
                  "The program uses a Chi-Square test to determine the most likely shift key. It decodes the "
                  "ciphertext with all possible shifts (0-25), and then calculates the Chi-Square statistic by comparing "
                  "the letter frequency of the decoded text to the expected frequency in the English language. The shift "
                  "with the lowest Chi-Square value is considered the most likely key.",

        "Vigenere": "The Vigenère cipher is an advancement in the art of war-time communication, representing a "
                    "significant step forward from the Caesar cipher by introducing a form of polyalphabetic "
                    "substitution."
                    "\n"
                    "\n"
                    "It utilizes a keyword to vary the shift for each letter in the plaintext. This key is repeated "
                    "to match the length of the plaintext message. For example, with a key of 'KEY', 'A' would be "
                    "shifted by the alphabet position of 'K', 'B' by 'E', and so on. This method creates a more "
                    "secure encryption, as it produces multiple ciphertext alphabets, making the Vigenère cipher much "
                    "harder to break without knowledge of the key."
                    " Example (Key: KEY):\nKey Repeated: K E Y K E \nPlain Text: H E L L O \nCipher Text: R I J M K\n"
                    "\n"
                    "Cryptanalysis Method:\n"
                    "The program uses statistical analysis by employing a Kasiski Examination and a frequency analysis "
                    "method to guess the length of the key and then deduces the possible keys. By aligning the most "
                    "frequent letters in segments of the ciphertext (divided by the guessed key length) with the most "
                    "frequent letters in English, it creates potential key segments and combines them to form the most "
                    "probable keys.",

        "Hill": "The Hill cipher, developed by Lester S. Hill in 1929, marks a departure from traditional "
                "substitution ciphers by employing mathematical concepts from linear algebra."
                "\n"
                "\n"
                "It transforms letters into numerical values ('A' = 0, 'B' = 1, ..., 'Z' = 25) and processes blocks "
                "of text as vectors. These vectors are then multiplied by a key matrix to produce the ciphertext. The "
                "key is a square matrix that must be invertible under modular arithmetic to ensure that decryption is "
                "possible. This method allows for the encryption of multiple letters at once, significantly "
                "increasing the cipher's strength against cryptanalysis."
                "\n"
                "\n"
                "Cryptanalysis Method:\n"
                "The program breaks the Hill cipher by using a known plaintext attack. It first identifies possible matrices "
                "that transform the known plaintext into the corresponding ciphertext through matrix operations. The "
                "procedure involves setting up equations based on the matrix multiplication rule and solving them to find "
                "the matrix coefficients. The coefficients that solve the equations correctly are potential keys, which "
                "are tested to ensure they can indeed decrypt the ciphertext to the known plaintext."
                "\n",
    }

    # Update text box with current cipher's information
    cipher_info_text1.config(state=tk.NORMAL)
    cipher_info_text1.delete("1.0", tk.END)
    cipher_info_text1.insert(tk.END, f"Current Cipher: {cipher_name}\n\n")
    cipher_info_text1.insert(tk.END, cipher_descriptions[cipher_name])
    cipher_info_text1.config(state=tk.DISABLED)

    # Handle UI components based on selected cipher
    if cipher_name == "Vigenere":
        max_key_length_label.pack(anchor=tk.W)
        max_key_length_entry.pack(padx=5, pady=5, fill=tk.X)
        key_length_guesses_label.pack(anchor=tk.W)
        key_length_guesses_entry.pack(padx=5, pady=5, fill=tk.X)
        shift_guesses_label.pack(anchor=tk.W)
        shift_guesses_entry.pack(padx=5, pady=5, fill=tk.X)

        matrix_size_label.pack_forget()
        matrix_size_entry.pack_forget()
        generate_hill_button.pack_forget()
        known_plaintext_label.pack_forget()
        known_plaintext_entry.pack_forget()
        start_index_label.pack_forget()
        start_index_entry.pack_forget()
    elif cipher_name == "Hill":
        matrix_size_label.pack(anchor=tk.W)
        matrix_size_entry.pack(padx=5, pady=(0, 5), fill=tk.X)
        generate_hill_button.pack(padx=5, pady=(5, 5), fill=tk.X)
        known_plaintext_label.pack(anchor=tk.W)
        known_plaintext_entry.pack(padx=5, pady=(0, 5), fill=tk.BOTH, expand=True)
        start_index_label.pack(anchor=tk.W)
        start_index_entry.pack(padx=5, pady=(0, 5), fill=tk.X)

        max_key_length_label.pack_forget()
        max_key_length_entry.pack_forget()
        key_length_guesses_label.pack_forget()
        key_length_guesses_entry.pack_forget()
        shift_guesses_label.pack_forget()
        shift_guesses_entry.pack_forget()
    else:
        max_key_length_label.pack_forget()
        max_key_length_entry.pack_forget()
        key_length_guesses_label.pack_forget()
        key_length_guesses_entry.pack_forget()
        shift_guesses_label.pack_forget()
        shift_guesses_entry.pack_forget()
        matrix_size_label.pack_forget()
        matrix_size_entry.pack_forget()
        generate_hill_button.pack_forget()
        known_plaintext_label.pack_forget()
        known_plaintext_entry.pack_forget()
        start_index_label.pack_forget()
        start_index_entry.pack_forget()

    # Update button appearance
    pressed_button_color = '#0a4f67'
    for cipher, btn in cipher_buttons.items():
        if cipher == cipher_name:
            btn.config(relief=tk.SUNKEN, bg=pressed_button_color)
        else:
            btn.config(relief=tk.RAISED, bg=button_color)

    update_key_format_example()


# Example: Select 'Caesar' cipher by default at the beginning of the script
select_cipher("Caesar")

# With this:
if __name__ == "__main__":
    root.mainloop()
