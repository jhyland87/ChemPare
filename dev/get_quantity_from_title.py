from __future__ import annotations

import re

def get_quantity_from_title(title):
    pattern = r"^(.*) (-\s)?([0-9,]+)(k?g|[cmμ]m)"
    quantity = re.match(pattern, title).group(3) + re.match(pattern, title).group(4)
    return quantity
