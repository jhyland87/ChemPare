from S3 import fetch_from_es_drei
from LaboratoriumDiscounter import fetch_from_lab_dis
from Onyxmet import fetch_from_onyxmet
from LabChem import fetch_from_lab_chem
from get_cas import get_cas
from rich.console import Console
from rich.panel import Panel
import requests
import json
import re
from rich.progress import Progress

def main():
    print("Enter Chemical Name:")
    chem = input("> ")

    console = Console()

    with Progress(console=console) as progress:
        task = progress.add_task("[cyan]Searching.. ", total=int(4))

        supplier_list = []

        # Loop through each supplier and call get_supplier_results
        for supplier_name, fetch_function, identifier_type in [
            ('es_drei', fetch_from_es_drei, "iupac"),
            ('lab_dis', fetch_from_lab_dis, "CAS"),
            ('onxymet', fetch_from_onyxmet, "CAS"),
            ('labchem', fetch_from_lab_chem, "iupac"),
        ]:
            try:
                result = get_supplier_results(supplier_name, fetch_function, identifier_type, chem)
                if result is not None:
                    supplier_list.append(result)
                    progress.update(task, advance=1)
            except:
                pass
                

    # Display results
    for supplier in supplier_list:
        for name, price, quantity in zip(supplier['name'], supplier['price'], supplier['quantity']):
            panel = Panel(f"[yellow][b]{name}[/b][/yellow]\nPrice: {price}\nQuantity: {quantity}\nSupplier: {supplier['supplier']}\nLocation: {supplier['location']}\nURL: {supplier['url']}", expand=True)
            console.print(panel)


def get_supplier_results(supplier, fetch_command, search_mode, chem):

    combined_name_list = []
    combined_price_list = []
    combined_supplier_name_list = []
    combined_location_list = []
    combined_url_list = []

    console = Console()

    if search_mode == "CAS":
        search_query = get_cas(chem)
        if search_query == None:
            search_query = chem
    else:
        search_query = chem

    result = fetch_command(search_query)

    try:
        name_list, price_list, supplier_name, location, url, quantity_list = result
    except TypeError:
        return None

    results = {
        "name": name_list,
        "price": price_list,
        "supplier": supplier_name,
        "location": location,
        "url": url,
        "quantity": quantity_list
    }

    return(results)

if __name__ == "__main__":
    main()
    input("")