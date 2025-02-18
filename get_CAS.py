import requests

def get_cas(chem):
    # URL encode the identifier and representation (for any special characters)
    url = f"https://cactus.nci.nih.gov/chemical/structure/{chem}/cas"
    
    # Send a GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.content
    else:
        return f"Error: {response.status_code}"