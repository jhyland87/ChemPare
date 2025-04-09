#!/usr/bin/env bash

query="acid"

curl "https://api.chemworldcorp.com/?search=${query}" \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: en-US,en;q=0.5' \
  -H 'cache-control: no-cache' \
  -H 'origin: https://www.chemworld.com' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.chemworld.com/' \
  -H 'sec-ch-ua: "Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-gpc: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'

https://www.ChemWorld.com/ProductDetails.asp?ProductCode=BA3000-Q
https://www.chemworld.com/Boric-Acid-Solution-2-percent-p/ba3000-q.htm
