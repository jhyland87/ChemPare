import requests
from bs4 import BeautifulSoup
import re


def fetch_from_lab_chem(chem):
    name_list = []
    price_list = []
    quantity_list = []
    supplier_name = "LabChem Röttinger"
    location = "Germany"

    url = f"https://www.labchem.de/search?q={chem}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        # Find all product names and prices
        names = soup.find_all("h2", class_="product-item-title", limit=3)
        prices = soup.find_all("h3", class_="product-item-price-new", limit=3)

        pattern = r"^(.*) (-\s)?([0-9,]+)(k?g|[cmμ]m)"

        # Extract names and prices
        for i in range(min(len(names), len(prices))):
            name_list.append(names[i].text.strip())
            price_list.append(prices[i].text.strip())

            quantity = None
            try:
                quantity = re.match(pattern, names[i].text.strip()).group(3) + re.match(
                    pattern, names[i].text.strip()
                ).group(4)
            except:
                quantity = ""
            quantity_list.append(quantity)
    except AttributeError:
        pass  # Handle cases where elements are not found

    return name_list, price_list, supplier_name, location, url, quantity_list
