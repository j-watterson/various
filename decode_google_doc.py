# This script fetches a table from a publicly accessible Google Docs document, parses the table data, 
# and prints it as a grid of characters in a specific layout. The table is expected to have at least 
# three columns: 'x-coordinate', 'y-coordinate', and 'Character', where the x and y values represent 
# the positions of characters in a 2D grid. The characters are then arranged and printed row by row 
# to visually represent the grid. The code uses the `requests` library to fetch the document, `BeautifulSoup` 
# to parse the HTML, and `pandas` to process the table data. The resulting grid is printed in reverse order 
# of the y-coordinates, starting from the highest y-value.

import requests
from collections import defaultdict
import pandas as pd
from bs4 import BeautifulSoup

def parse_google_doc_table(url):
    # Fetch the HTML content of the page
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for failed requests
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Locate the table
    table = soup.find("table")
    if not table:
        print("No table found in the document.")
        return None

    # Parse table rows
    rows = table.find_all("tr")
    parsed_data = []
    for row in rows:
        # Extract data from each cell (td/th)
        cells = row.find_all(["td", "th"])
        parsed_data.append([cell.text.strip() for cell in cells])
    
    return parsed_data

def print_unicode_grid(url):
    # Retrieve and parse the data from the document
    data = parse_google_doc_table(url)
    if data and len(data) > 1:
        # Assuming the first row contains headers
        df = pd.DataFrame(data[1:], columns=data[0])
        print("Parsed Table Data as DataFrame:")
        print(df)
    else:
        print("No valid data to display.")
        return

    # Initialize a dictionary to store grid positions and characters
    grid = defaultdict(lambda: " ")

    # Populate the grid dictionary
    for _, row in df.iterrows():
        x, y, char = int(row['x-coordinate']), int(row['y-coordinate']), row['Character']
        grid[(x, y)] = char

    # Determine the dimensions of the grid
    max_x = max(coord[0] for coord in grid.keys())
    max_y = max(coord[1] for coord in grid.keys())

    # Build and print the grid row by row in reverse order
    for y in range(max_y, -1, -1):
        row = "".join(grid.get((x, y), " ") for x in range(max_x + 1))
        print(row)

# Example usage
url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
print_unicode_grid(url)
