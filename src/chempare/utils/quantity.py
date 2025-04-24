from __future__ import annotations

from unicodedata import normalize
import chempare.utils as utils
import regex
from datatypes import QuantityType


def parse_quantity(value: str) -> QuantityType:
    """
    Parse a string for the quantity and unit of measurement

    Args:
        value (str): Suspected quantity string

    Returns:
        Optional[QuantityType]: Returns a dictionary with the 'quantity' and
                        'uom' values
    """

    value = normalize('NFKC', value)

    # When a UOM is found, its lower case key can be used to look up the
    # correct case format for it. If the UOM is in one of the below tuple
    # keys, then it's substituted with the value.
    uom_cases = {
        ("liter", "liters", "litres", "l"): "L",
        ("ml", "mls", "millilitre", "millilitres", "milliliter", "milliliters"): "mL",
        ("g", "gram", "grams"): "g",
        ("lb", "lbs", "pound", "pounds"): "lb",
        ("kg", "kgs", "killogram", "killograms"): "kg",
        ("mm", "millimeter", "millimeters", "millimetre", "millimetres"): "mm",
        ("cm", "centimeter", "centimeters", "centimetre", "centimetres"): "cm",
        ("m", "meter", "meters", "metre", "metres"): "m",
        ("oz", "ounce", "ounces"): "oz",
        ("gal", "gallon", "gallons"): "gal",
        ("qt", "quart", "quarts"): "qt",
    }

    if isinstance(value, str) is False:
        return {}

    value = value.strip()

    if not value or value.isspace():
        return {}

    # https://regex101.com/r/lDLuVX/4
    pattern = (
        r"(?P<quantity>[0-9][0-9\.\,]*)?\s?"
        r"(?P<uom>gal(?:lon)|(?:milli|kilo|centi)"
        r"(?:gram|meter|liter|metre)s?|z|ounces?|grams?|gallon|gal"
        r"|kg|g|lbs?|pounds?|l|qt|m?[glm]|piece|drum)"
    )

    matches = regex.search(pattern, value, regex.IGNORECASE)

    if not matches:
        return {}

    quantity_obj: QuantityType = matches.groupdict()

    # Look for any proper substitution UOM's
    proper_uom = utils.find_values_with_element(uom_cases, str(quantity_obj["uom"]).lower())

    if len(proper_uom) > 0:
        quantity_obj["uom"] = proper_uom[0]

    return quantity_obj
