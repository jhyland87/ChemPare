from __future__ import annotations

import re

import regex


iso_4217_pattern = (
    r"(?:ab\s?)?(?:(?P<currency>\p{Sc}|"
    r"(?P<currency>"
    r"A(?:[EM]D|[FZ]N|LL|[NW]G|OA|RS|UD?)|"
    r"B(?:AM|[BHMNZS]D|DT|[GT]N|IF|OB|RL|WP|YR)|"
    r"C(?:AD|[DH]F|[LOU]P|NY|[RU]C|VE|ZK)|"
    r"D(?:JF|KK|OP|ZD)|"
    r"E(?:GP|RN|TB|UR?)|"
    r"F(?:JD|KP)|"
    r"G(?:[BGI]P|EL|HS|[YM]D|NF|TQ)|"
    r"H(?:KD|NL|RK|TG|UF)|"
    r"I(?:[NRD]R|LS|MP|QD|SK)|"
    r"J(?:EP|MD|OD|PY)|"
    r"K(?:[GE]S|HR|MF|[PR]W|[WY]D|ZT)|"
    r"L(?:AK|BP|KR|[RY]D|SL)|"
    r"M(?:[AK]D|DL|GA|[MW]K|NT|OP|RO|[UVY]R|[XZ]N)|"
    r"N(?:[AZ]D|GN|IO|OK|PR)|"
    r"(?:QA|OM|YE)R|"
    r"P(?:AB|[EKL]N|GK|HP|KR|YG)|"
    r"R(?:ON|SD|UB|WF)|"
    r"S(?:[AC]R|[BRGDT]D|DG|EK|[HY]P|[LZP]L|OS|VC)|"
    r"T(?:HB|[JZ]S|MT|[NTVW]D|OP|RY)|"
    r"U(?:AH|GX|SD?|YU|ZS)|"
    r"V(?:EF|ND|UV)|WST|"
    r"X(?:[AOP]F|CD|DR)|"
    r"Z(?:AR|MW|WD)))"
    r"\s?(?P<price>[0-9]+(?:[,\.][0-9]+)*)"
    r"|(?P<price>[0-9]+(?:[,\.][0-9]+)*)\s?(?P<currency>\p{Sc}|"
    # r'(?:us|au|ca)d?|eur?|chf|rub|gbp|jyp|pln|sek|uah|hrk)'
    r"(?P<currency>"
    r"A(?:[EM]D|[FZ]N|LL|[NW]G|OA|RS|UD?)|"
    r"B(?:AM|[BHMNZS]D|DT|[GT]N|IF|OB|RL|WP|YR)|"
    r"C(?:AD|[DH]F|[LOU]P|NY|[RU]C|VE|ZK)|"
    r"D(?:JF|KK|OP|ZD)|"
    r"E(?:GP|RN|TB|UR?)|"
    r"F(?:JD|KP)|"
    r"G(?:[BGI]P|EL|HS|[YM]D|NF|TQ)|"
    r"H(?:KD|NL|RK|TG|UF)|"
    r"I(?:[NRD]R|LS|MP|QD|SK)|"
    r"J(?:EP|MD|OD|PY)|"
    r"K(?:[GE]S|HR|MF|[PR]W|[WY]D|ZT)|"
    r"L(?:AK|BP|KR|[RY]D|SL)|"
    r"M(?:[AK]D|DL|GA|[MW]K|NT|OP|RO|[UVY]R|[XZ]N)|"
    r"N(?:[AZ]D|GN|IO|OK|PR)|"
    r"(?:QA|OM|YE)R|"
    r"P(?:AB|[EKL]N|GK|HP|KR|YG)|"
    r"R(?:ON|SD|UB|WF)|"
    r"S(?:[AC]R|[BRGDT]D|DG|EK|[HY]P|[LZP]L|OS|VC)|"
    r"T(?:HB|[JZ]S|MT|[NTVW]D|OP|RY)|"
    r"U(?:AH|GX|SD?|YU|ZS)|"
    r"V(?:EF|ND|UV)|WST|"
    r"X(?:[AOP]F|CD|DR)|"
    r"Z(?:AR|MW|WD)))"
    r")"
)

string = "ab 102,17 € *"
matches = regex.match(iso_4217_pattern, string, regex.IGNORECASE)

print(matches.groupdict())
