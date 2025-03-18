import math
import sys
import os
import signal
from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from chempare import SearchFactory


# def signal_handler(sig, frame):
#     print('You pressed Ctrl+C!')
#     sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)
# print('Press Ctrl+C')
# signal.pause()

def get_terminal_width():
    """
    Returns the width of the terminal in characters.
    """
    try:
        terminal_size = os.get_terminal_size()
        return int(terminal_size.columns)
    except OSError:
        # If not running in a terminal, return a default width
        return 80


def main():
    if len(sys.argv) >= 2:
        chem = str(sys.argv[1]).strip()
    else:
        print("Enter Chemical Name:")
        chem = input("> ")

    col_widths = math.floor(get_terminal_width() / 2 - 2)
    console = Console()

    # cas_number = get_cas(chem)

    product_search = SearchFactory(chem)

    # Create a progress bar with the total number of suppliers
    # with Progress(console=console) as progress:
    # task = progress.add_task("[cyan]Searching..",
    # total=len(product_search.results))

    supplier_list = {}

    # Loop over the products and create the panel for each.
    col_a = None
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
        currency = product.currency
        currency_code = product.currency_code or "XX"
        #if hasattr(product, 'USD')
        cas = product.cas or "N/A"
        # trunk-ignore(git-diff-check/error)
        if product.quantity is None or product.uom is None:
            quantity = "N/A"
        else:
            quantity = f"{product.quantity}{product.uom}"
        # quantity = product['quantity']
        url = product.url
        supplier = product.supplier
        # Create the panel to print

        if not col_a:
            col_a = Panel(
                (
                    f"[yellow][b]{name}[/b][/yellow]\nCAS: {cas}\n"
                    f"Price: {currency}{price} ({currency_code})\n"
                    f"Quantity: {quantity if quantity else 'N/A'}\n"
                    f"Supplier: {supplier}\nURL: {url if url else 'N/A'}"
                ),
                expand=True,
                width=col_widths,
                height=8,
                padding=(0, 0),
            )
        else:
            col_b = Panel(
                (
                    f"[yellow][b]{name}[/b][/yellow]\n"
                    f"CAS: {cas}\nPrice: {currency}{price} ({currency_code})\n"
                    f"Quantity: {quantity if quantity else 'N/A'}\n"
                    f"Supplier: {supplier}\nURL: {url if url else 'N/A'}"
                ),
                expand=True,
                border_style="none",
                width=col_widths,
                height=8,
                padding=(0, 0),
            )
            panel = Panel.fit(
                Columns([col_a, col_b]),
                # title="My Panel",
                # border_style="Yellow",
                border_style="black",
                title_align="left",
                padding=(0, 0),
            )
            col_a = None
            console.print(panel)
    sys.exit()

if __name__ == "__main__":
    main()
# If returns none okay, skip.
# Quantities.
# Translate for LabChem (and S3).
# Onyxmet check if out of stock.
# CAS
# Progressbar.
# URL ONYXMET
# Labchem
