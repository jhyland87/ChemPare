import regex

pattern = (r'^(?:(?P<currency>\p{Sc}|(?:us|au|ca)d?|eu|chf|rub)\s?(?P<price>[0-9]+(?:[,\.][0-9]+)*)'
            r'|(?P<price>[0-9]+(?:[,\.][0-9]+)*)\s?(?P<currency>\p{Sc}|(?:us|au|ca)d?|eu|chf|rub))$')

# Or even more comprehensive:
pattern = (r'^(?:(?P<currency>\p{Sc}|'
           r'(?:AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD?|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB'
           r'|BOV|BRL|BSD|BTN|BWP|BYN|BZD|CAD?|CDF|CHE|CHF|CHW|CLF|CLP|CNY|COP|COU|CRC|CUC|CUP'
           r'|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR?|FJD|FKP|GBP|GEL|GHS|GIP|GMD|GNF|GTQ|GYD'
           r'|HKD|HNL|HRK|HTG|HUF|IDR|ILS|INR|IQD|IRR|ISK|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW'
           r'|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRU|MUR|MVR|MWK'
           r'|MXN|MXV|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON'
           r'|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SRD|SSP|STN|SVC|SYP|SZL|THB|TJS'
           r'|TMT|TND|TOP|TRY|TTD|TWD|TZS|UAH|UGX|USD?|USN|UYI|UYU|UYW|UZS|VES|VND|VUV|WST|XAF'
           r'|XAG|XAU|XBA|XBB|XBC|XBD|XCD|XDR|XOF|XPD|XPF|XPT|XSU|XTS|XUA|XXX|YER|ZAR|ZMW|ZWL))'
           r'\s?(?P<price>[0-9]+(?:[,\.][0-9]+)*)'
           r'|(?P<price>[0-9]+(?:[,\.][0-9]+)*)\s?(?P<currency>\p{Sc}|'
           #r'(?:us|au|ca)d?|eur?|chf|rub|gbp|jyp|pln|sek|uah|hrk)'
           r'(?:AED|AFN|ALL|AMD|ANG|AOA|ARS|AUD?|AWG|AZN|BAM|BBD|BDT|BGN|BHD|BIF|BMD|BND|BOB'
           r'|BOV|BRL|BSD|BTN|BWP|BYN|BZD|CAD?|CDF|CHE|CHF|CHW|CLF|CLP|CNY|COP|COU|CRC|CUC|CUP'
           r'|CVE|CZK|DJF|DKK|DOP|DZD|EGP|ERN|ETB|EUR?|FJD|FKP|GBP|GEL|GHS|GIP|GMD|GNF|GTQ|GYD'
           r'|HKD|HNL|HRK|HTG|HUF|IDR|ILS|INR|IQD|IRR|ISK|JMD|JOD|JPY|KES|KGS|KHR|KMF|KPW|KRW'
           r'|KWD|KYD|KZT|LAK|LBP|LKR|LRD|LSL|LYD|MAD|MDL|MGA|MKD|MMK|MNT|MOP|MRU|MUR|MVR|MWK'
           r'|MXN|MXV|MYR|MZN|NAD|NGN|NIO|NOK|NPR|NZD|OMR|PAB|PEN|PGK|PHP|PKR|PLN|PYG|QAR|RON'
           r'|RSD|RUB|RWF|SAR|SBD|SCR|SDG|SEK|SGD|SHP|SLL|SOS|SRD|SSP|STN|SVC|SYP|SZL|THB|TJS'
           r'|TMT|TND|TOP|TRY|TTD|TWD|TZS|UAH|UGX|USD?|USN|UYI|UYU|UYW|UZS|VES|VND|VUV|WST|XAF'
           r'|XAG|XAU|XBA|XBB|XBC|XBD|XCD|XDR|XOF|XPD|XPF|XPT|XSU|XTS|XUA|XXX|YER|ZAR|ZMW|ZWL))'
           r')$')

examples = [
    '56£','$1','1$','$1','1$','₹98,85','55,23₹','$23.43','¥23',
    '$ 23','$ 123,231','£25,''€23.43','€23','€123,231','€ 23.43',
    '€ 23','€ 123,231','123,231 €','123 USD','USD 123,554',
    '894 EU','eu 123,554','$123,231','$ 23.43','99 AU','542 aud'
]

for example in examples:
    r = regex.match(pattern, example, regex.IGNORECASE)
    if r:
        print(r.groupdict())
