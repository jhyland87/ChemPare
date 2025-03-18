from rich.console import Console
from rich.panel import Panel
from chempare import SearchFactory
import sys

def main():
    if len(sys.argv) >= 2:
        chem = str(sys.argv[1]).strip()
    else:
        print("Enter Chemical Name:")
        chem = input("> ")

    console = Console()

    #cas_number = get_cas(chem)

    product_search = SearchFactory(chem)

    # Create a progress bar with the total number of suppliers
    # with Progress(console=console) as progress:
        # task = progress.add_task("[cyan]Searching..", total=len(product_search.results))

    supplier_list = {}

    # Loop over the products and create the panel for each.
    for product in product_search:

        if product.supplier in supplier_list:
            if supplier_list[product.supplier] == 3:
                continue
            else:
                supplier_list[product.supplier] += 1
        else:
            supplier_list[product.supplier] = 1

        name = product.name
        price = product.price
        # trunk-ignore(git-diff-check/error)
        if product.quantity is None or product.uom is None:
            quantity = 'N/A'
        else:
            quantity = f'{product.quantity}{product.uom}'
        # quantity = product['quantity']
        url = product.url
        supplier = product.supplier

        # Create the panel to print
        panel = Panel(f"[yellow][b]{name}[/b][/yellow]\nPrice: {price}\nQuantity: {quantity if quantity else 'N/A'}\nSupplier: {supplier}\nURL: {url if url else 'N/A'}", expand=True)
        console.print(panel)
    sys.exit()

if __name__ == "__main__":
    main()
    input("")

# If returns none okay, skip.
# Quantities.
# Translate for LabChem (and S3).
# Onyxmet check if out of stock.
# CAS
# Progressbar.
# URL ONYXMET
# Labchem