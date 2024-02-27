
from tabulate import tabulate

# Open text.txt file
with open("text3.txt") as file:
    cipher_text = file.read()

    # Remove Spaces and punctuation
    cipher_text = cipher_text.replace(" ", "")
    cipher_text = cipher_text.replace("!", "")
    cipher_text = cipher_text.replace(",", "")
    cipher_text = cipher_text.replace(".", "")
    cipher_text = cipher_text.replace("?", "")
    cipher_text = cipher_text.replace("-", "")
    cipher_text = cipher_text.replace('"', "")
    cipher_text = cipher_text.replace("(", "")
    cipher_text = cipher_text.replace(")", "")
    cipher_text = cipher_text.replace("\n", "")
    cipher_text = cipher_text.replace(":", "")
    # print(cipher_text)


def calculate_ic(column):
    # Make sure cipher_text is in uppercase
    column_text = column.upper()

    # Create list of frequencies
    freq = [0] * 26

    # Count Frequencies
    for char in column_text:
        match char:
            case 'A':
                freq[0] += 1
            case 'B':
                freq[1] += 1
            case 'C':
                freq[2] += 1
            case 'D':
                freq[3] += 1
            case 'E':
                freq[4] += 1
            case 'F':
                freq[5] += 1
            case 'G':
                freq[6] += 1
            case 'H':
                freq[7] += 1
            case 'I':
                freq[8] += 1
            case 'J':
                freq[9] += 1
            case 'K':
                freq[10] += 1
            case 'L':
                freq[11] += 1
            case 'M':
                freq[12] += 1
            case 'N':
                freq[13] += 1
            case 'O':
                freq[14] += 1
            case 'P':
                freq[15] += 1
            case 'Q':
                freq[16] += 1
            case 'R':
                freq[17] += 1
            case 'S':
                freq[18] += 1
            case 'T':
                freq[19] += 1
            case 'U':
                freq[20] += 1
            case 'V':
                freq[21] += 1
            case 'W':
                freq[22] += 1
            case 'X':
                freq[23] += 1
            case 'Y':
                freq[24] += 1
            case 'Z':
                freq[25] += 1

    # Calculate IC value
    IC_sum = 0

    for f in freq:
        IC_sum = IC_sum + (f * (f - 1))

    IC = IC_sum / (len(column_text) * (len(column_text) - 1))

    return IC


def create_matrix(n, num_rows, text):
    # Create the matrix
    matrix = [['' for _ in range(n)] for _ in range(num_rows)]

    # Populate with letters
    row = 0
    col = 0

    for letter in cipher_text:
        matrix[row][col] = letter
        col += 1

        # Move to the next row if the current row is full
        if col == n:
            row += 1
            col = 0

    return matrix


text_length = len(cipher_text)
print("Length of Cipher Text: " + str(text_length))

# Determine the largest key size the user wants to check for
max_key_length = int(input("What is the maximum key length?"))

# Create a 2D array to store the IC values with their corresponding key lengths
data = [[i, 0] for i in range(1, max_key_length + 1)]

# Iterate through key lengths
for n in range(1, max_key_length + 1):
    # Handle base case
    if n == 1:
        data[n - 1][1] = calculate_ic(cipher_text)
    else:
        # Determine number of rows for matrix
        num_rows = len(cipher_text) // n
        # Check that the text will not 'overflow'
        if text_length % n != 0:
            num_rows += 1

        # Create Matrix
        matrix_1 = create_matrix(n, num_rows, cipher_text)

        # Apply IC Function for each column
        ic_sum = 0
        for col_index in range(n):
            column = [matrix_1[row][col_index] for row in range(num_rows)]
            column_string = "".join(column)
            ic_sum += calculate_ic(column_string)

        # Save the average IC value
        data[n - 1][1] = ic_sum / n

# Sort by IC values and print table
sorted_matrix = sorted(data, key=lambda row: abs(row[1] - 0.0686))
headers = ["Key Length", "IC Value"]
table = tabulate(sorted_matrix, headers, tablefmt="grid")
print(table)

