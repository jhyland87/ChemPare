from __future__ import annotations

import webbrowser
from webbrowser import MacOSXOSAScript
from webbrowser import register

register("brave-browser", None, MacOSXOSAScript("Brave Browser"))

webbrowser.get("brave-browser").open(
    f'file:///Users/justin.hyland/Documents/scripts/ChemPare/coverage-html/index.html', new=0, autoraise=False
)
