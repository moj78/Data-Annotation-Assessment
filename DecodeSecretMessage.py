import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

def get_google_doc_table(doc_url):
    # Convert Google Docs URL to export as HTML format
    doc_id = doc_url.split('/d/')[1].split('/')[0]
    export_url = f'https://docs.google.com/document/d/{doc_id}/export?format=html'
    
    #response = requests.get(export_url)
    response = requests.get(doc_url)
    if response.status_code != 200:
        raise Exception("Failed to retrieve the document. Make sure the URL is accessible.")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if not table:
        raise Exception("No table found in the document.")
    
    data = []
    rows = table.find_all('tr')[1:]  # Skip header row
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 3:
            continue
        x = int(cols[0].text.strip())
        char = cols[1].text.strip()
        y = int(cols[2].text.strip())
        data.append((x, char, y))
    
    return data

def create_character_grid(data):
    if not data:
        return []
    
    max_x = max(x for x, _, _ in data)
    max_y = max(y for _, _, y in data)
    max_index = max(max_x, max_y)  # added by Mnj to avoid index error
    
    #grid = np.full((max_y + 1, max_x + 1), ' ', dtype=str)    #Mnj : Commented out this line for the one below
    grid = np.full((max_index + 1, max_index + 1), ' ', dtype=str)  # Mnj : changed to max_index
    
    for x, char, y in data:
        grid[y, x] = char      # Mnj : commented out thia line for the one below
        #grid[x, y] = char
    
    return grid

def print_grid(grid):
    for row in grid:
        print(''.join(row))

# Example usage
doc_url = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
data = get_google_doc_table(doc_url)
grid = create_character_grid(data)
print_grid(grid)
