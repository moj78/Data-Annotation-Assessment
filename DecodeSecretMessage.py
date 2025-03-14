import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np



def decode_secret_message(doc_url):

    ######################################################################
    #  read the google doc url and extract the table in a list of tuples
    # each tuple contains (x, character, y)
    ######################################################################

    # read document for url
    response = requests.get(doc_url)
    # check if the request was successful
    if response.status_code != 200:
        raise Exception("Failed to retrieve the document. Make sure the URL is accessible.")
    
    # parse the document using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # extract the table from the document
    table = soup.find('table')
    if not table:
        raise Exception("No table found in the document.")
    
    # read the table and fill the data list with tuples (x, character, y)
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


    ######################################################################
    # Fill a 2D array (grid) with characters from the data list 
    # 
    ######################################################################

    if not data:
        return []
    
    max_x = max(x for x, _, _ in data)
    max_y = max(y for _, _, y in data)
    max_index = max(max_x, max_y)  # added by Mnj to avoid index error
    
    grid = np.full((max_y + 1, max_x + 1), ' ', dtype=str)    #Mnj : Commented out this line for the one below
    #grid = np.full((max_index, max_index), ' ', dtype=str)  # Mnj : changed to max_index
    
    for x, char, y in data:
        # since the y coordinate is inverted in the grid, we need to subtract y from max_y
        # to place the character in the correct position
        grid[max_y - y, x] = char      

    ######################################################################
    # Print the grid to the console
    ######################################################################
    
    for row in grid:
        print(''.join(row))

