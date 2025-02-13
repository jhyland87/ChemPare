import requests
from bs4 import BeautifulSoup

def fetch_from_lab_dis(chem):
    name_list = []
    price_list = []
    supplier_name = "Laboratoriumdiscounter"
    location = "The Netherlands"

    urls = [
        f"https://www.laboratoriumdiscounter.nl/en/search/{chem}",
        f"https://www.laboratoriumdiscounter.nl/en/search/{chem}/?max=1000&min=0&limit=24&sort=asc&filter%5B%5D=837184",
        f"https://www.laboratoriumdiscounter.nl/en/search/{chem}/?max=1000&min=0&limit=24&sort=asc&filter%5B%5D=837179",
    ]

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            # Find all product names and prices
            names_container = soup.find_all("div", class_="product-title", limit=3)
            names = [div.find("a") for div in names_container]

            prices_container = soup.find_all("div", class_="product-price", limit=3)
            prices = [div.find("span") for div in prices_container]

            # Extract names and prices
            for i in range(min(len(names), len(prices))):
                name_list.append(names[i].text.strip())
                price_list.append(prices[i].text.strip())
        except AttributeError:
            pass  # Handle cases where elements are not found

    return name_list, price_list, supplier_name, location, url
