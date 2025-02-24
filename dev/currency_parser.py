import regex

pattern = (r'^(?:(?P<currency>\p{Sc}|(?:us|au|ca)d?|eu|chf|rub)\s?(?P<price>[0-9]+(?:[,\.][0-9]+)*)'
            r'|(?P<price>[0-9]+(?:[,\.][0-9]+)*)\s?(?P<currency>\p{Sc}|(?:us|au|ca)d?|eu|chf|rub))$')
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
