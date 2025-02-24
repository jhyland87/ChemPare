import regex

pattern = r'^(?:(?P<currency>\p{Sc}|usd?|eu)\s?(?P<price>[0-9]+(?:[,\.][0-9]+)*)|(?P<price>[0-9]+(?:[,\.][0-9]+)*)\s?(?P<currency>\p{Sc}|usd?|eu))$'

examples = [
    '56£','$1','1$','$1','1$','$23.43','$23','$123,231','$ 23.43',
    '$ 23','$ 123,231','£25,''€23.43','€23','€123,231','€ 23.43',
    '€ 23','€ 123,231','123,231 €','123 USD','USD 123,554',
    '894 EU','eu 123,554',
]

for example in examples:
    r = regex.match(pattern, example, regex.IGNORECASE)
    if r:
        print(r.groupdict())