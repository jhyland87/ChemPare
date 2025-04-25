from __future__ import annotations

from fuzzywuzzy import fuzz


search = "sodium borohydride"

string_list = [
    "Sodium Borohydride Anhydrous Powder, Reagent Grade, 98%",
    "Sodium Borohydride  (Granulated)",
    "Sodium Borohydride",
    "SODIUM BOROHYDRIDE, CAPLETS, REAGENT (ACS) - 100 G",
    "Sodium Borohydride for Reduction >99,9% - 500g",
    "Borane - Tetrahydrofuran Complex (8.5% in Tetrahydrofuran, ca. 0.9mol/L) (stabilized with Sodium Borohydride) 500mL",
    "Bor Standardlösung (1000mg/l)",
    "Sodium Amide",
    "sodium boro",
    "sodium boron",
    "sodium triacetoxyborohydride",
]

for string2 in string_list:

    similarity_ratioa = fuzz.ratio(search.lower(), string2.lower())
    similarity_ratiob = fuzz.partial_ratio(search.lower(), string2.lower())
    print(f"Similarity ratio of '{string2}'")
    print("    fuzz.ratio:", fuzz.ratio(search.lower(), string2.lower()))
    print(
        "    fuzz.token_set_ratio:",
        fuzz.token_set_ratio(search.lower(), string2.lower()),
    )
    print(
        "    fuzz.token_sort_ratio:",
        fuzz.token_sort_ratio(search.lower(), string2.lower()),
    )
    print(
        "    fuzz.partial_ratio:",
        fuzz.partial_ratio(search.lower(), string2.lower()),
    )
    print("\n")
