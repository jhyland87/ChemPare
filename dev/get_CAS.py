from __future__ import annotations

import requests

def get_cas(chem):
    # URL encode the identifier and representation (for any special characters)
    url = f"https://cactus.nci.nih.gov/chemical/structure/{chem}/cas"
    
    # Send a GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        decoded_data = response.content.decode('utf-8')  # Decode the bytes to a string
        split_data = decoded_data.split('\n')  # Split by newline
        last_value = split_data[len(split_data) - 1]  # Get the first value
        cas_number = last_value
        return cas_number
    else:
        return f"Error: {response.status_code}"
