from __future__ import annotations

import os
import sys

import urllib3
from rich.console import Console
from rich.panel import Panel

from chempare.search_factory import SearchFactory

urllib3.disable_warnings()

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

    term_width = get_terminal_width() - 2
    console = Console()

    # cas_number = get_cas(chem)

    product_search = SearchFactory(chem)

    # Create a progress bar with the total number of suppliers
    # with Progress(console=console) as progress:
    # task = progress.add_task("[cyan]Searching..",
    # total=len(product_search.results))

    supplier_list = {}

    # Loop over the products and create the panel for each.
    for product in product_search:

        if product["supplier"] in supplier_list:
            if supplier_list[product["supplier"]] == 3:
                continue
            else:
                supplier_list[product["supplier"]] += 1
        else:
            supplier_list[product["supplier"]] = 1

        title = product["title"]
        price = product["price"]
        currency = product["currency"]
        # currency_code = product["currency"]_code or "XX"
        # if hasattr(product, 'USD')
        cas = product.get("cas", "N/A")
        # trunk-ignore(git-diff-check/error)
        if product["quantity"] is None or product["uom"] is None:
            quantity = "N/A"
        else:
            quantity = f"{product["quantity"]}{product["uom"]}"

        supplier = product["supplier"]
        # Create the panel to print

        us_equiv = ""

        # If the price has a USD conversion, then show that in parenthesis
        if (usd := product.get('usd', None)) is not None:
            us_equiv = f" (${usd} USD)"

        result_row = Panel(
            (
                f"[yellow][b]{title}[/b][/yellow]\n"
                f"CAS: {cas}\n"
                f"Price: {currency}{price}{us_equiv}\n"
                f"Quantity: {quantity if quantity else "N/A"}\n"
                f"Supplier: {supplier}\n"
                f"URL: {product["url"] or "N/A"}"
            ),
            expand=True,
            # width=term_width,
            height=8,
            padding=(0, 0),
        )

        console.print(result_row)

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
