from tabulate import tabulate
from analysis import utility as util
from ciphers import caesar as c


def cryptanalyse(text):
    english_ic = 0.067
    data = []
    for i in range(26):
        decoded_text = c.decode(text, i)
        print(decoded_text)
        ic_value = util.compute_ic(decoded_text)
        data.append((i, ic_value))  # Store the shift and its IC value as a tuple

    # Sort by how close the IC values are to the expected English IC
    sorted_matrix = sorted(data, key=lambda row: abs(row[1] - english_ic))
    headers = ["Shift", "IC Value"]
    table = tabulate(sorted_matrix, headers, tablefmt="grid")
    print(table)
