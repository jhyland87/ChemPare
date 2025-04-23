from __future__ import annotations

import regex

# pattern = r'(?P<B>(?<=A)B|B(?=A))|(?P<A>(?<=B)A|A(?=B))'
# Partial test at https://regex101.com/r/KFaYjq/4
# iso_4217_pattern = r'(?:AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD?|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BOV|BRL|BSD|BTN|BWP|BYN|BZD|CAD|CDF|CHE|CHF|CHW|CLF|CLP|CNY|COP|COU|CRC|CUC|CUP|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR?|FJD|FKP|GBP|GEL|GHS|GIP|GMD|GNF|GTQ|GYD|HKD|HNL|HRK|HTG|HUF|IDR|ILS|INR|IQD|IRR|ISK|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRU|MUR|MVR|MWK|MXN|MXV|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SRD|SSP|STN|SVC|SYP|SZL|THB|TJS|TMT|TND|TOP|TRY|TTD|TWD|TZS|UAH|UGX|USD?|USN|UYI|UYU|UYW|UZS|VES|VND|VUV|WST|XAF|XAG|XAU|XBA|XBB|XBC|XBD|XCD|XDR|XOF|XPD|XPF|XPT|XSU|XTS|XUA|XXX|YER|ZAR|ZMW|ZWL)'
pattern = (
    r"^(?:(?P<currency>\p{Sc}|"
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
    r")$"
)

examples = [
    "56£",
    "$1",
    "1$",
    "$1",
    "1$",
    "₹98,85",
    "55,23₹",
    "$23.43",
    "¥23",
    "$ 23",
    "$ 123,231",
    "£25," "€23.43",
    "€23",
    "€123,231",
    "€ 23.43",
    "€ 23",
    "€ 123,231",
    "123,231 €",
    "123 USD",
    "USD 123,554",
    "894 EU",
    "eu 123,554",
    "$123,231",
    "$ 23.43",
    "99 AU",
    "542 aud",
]

for example in examples:
    r = regex.match(pattern, example, regex.IGNORECASE)
    if r:
        print(r.groupdict())


"""

AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD|AWG|AZN|
BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB|BRL|BSD|BTN|BWP|BYR|BZD|
CAD|CDF|CHF|CLP|CNY|COP|CRC|CUC|CUP|CVE|CZK|
DJF|DKK|DOP|DZD|
EGP|ERN|ETB|EUR|
FJD|FKP|
GBP|GEL|GGP|GHS|GIP|GMD|GNF|GTQ|GYD|
HKD|HNL|HRK|HTG|HUF|
IDR|ILS|IMP|INR|IQD|IRR|ISK|
JEP|JMD|JOD|JPY|
KES|KGS|KHR|KMF|KPW|KRW|KWD|KYD|KZT|
LAK|LBP|LKR|LRD|LSL|LYD|
MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRO|MUR|MVR|MWK|MXN|MYR|MZN|
NAD|NGN|NIO|NOK|NPR|NZD|
OMR|
PAB|PEN|PGK|PHP|PKR|PLN|PYG|
QAR|
RON|RSD|RUB|RWF|
SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SPL|SRD|STD|SVC|SYP|SZL|
THB|TJS|TMT|TND|TOP|TRY|TTD|TVD|TWD|TZS|
UAH|UGX|USD|UYU|UZS|
VEF|VND|VUV|
WST|
XAF|XCD|XDR|XOF|XPF|
YER|
ZAR|ZMW|ZWD
"""
