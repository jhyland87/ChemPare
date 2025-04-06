#!/usr/bin/env bash

query_limit=20
search_term="acid"


# 1 Get the session binding from the initial request headers
session_bind=$(curl 'https://www.biofuranchem.com' \
  --get --silent --head \
  --request-target "/shop" \
  --data "Category=All" \
  --header 'sec-fetch-mode: navigate' \
  --header 'sec-fetch-dest: document' \
  --header 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' |
  jc --curl-head |
  jq --raw-output '.[0]."set-cookie"[] | select( . | contains("client-session-bind")) | split(";") | .[0] | split("=") | .[1]')
  #jq --raw-output '.[0]."set-cookie"[] | select( . | contains("session-bind")) | split(";") | .[0] | split("=") | @tsv'
# client-session-bind     c5340d24-ed5b-49c0-ac95-97d6e04e0440
# server-session-bind     c5340d24-ed5b-49c0-ac95-97d6e04e0440

echo "session_bind: ${session_bind}"

# 2 Get the XSRF id thingy
xsrf_token=$(curl 'https://www.biofuranchem.com' \
  --get --silent --head \
  --request-target '/_api/wix-laboratory-server/laboratory/conductAllInScope' \
  --data 'scope=wix-one-app' \
  --cookie 'server-session-bind='${session_bind}'; ssr-caching=cache#desc=miss#varnish=miss_miss#dc#desc=fastly_uw2-pub-1_g' |
  jc --curl-head |
  jq --raw-output '.[0]."set-cookie"[] | split("; ") | .[]| select( . | contains("XSRF-TOKEN")) | split("=") | .[1]')
# XSRF-TOKEN      1743857993|-KY61-XZjSlL

echo "xsrf_token: ${xsrf_token}"

# 3 Get the website instance ID ("access tokens" I guess?)
# 14517e1a-3ff0-af98-408e-2bd6953c36a2
# 1380b703-ce81-ff05-f115-39571d94dfcd - API
auth_token=$(curl 'https://www.biofuranchem.com' \
  --get --silent \
  --request-target '/_api/v1/access-tokens' \
  -H 'client-binding: '${session_bind} \
  -b 'server-session-bind='${session_bind}'; XSRF-TOKEN='${xsrf_token} |
  jq --raw-output '.apps["1380b703-ce81-ff05-f115-39571d94dfcd"].instance')

echo "auth_token: ${auth_token}"

# qEUlMvbax-QJbYJNPT63348PkPfDnmR2RjrHkbzrJjs.eyJpbnN0YW5jZUlkIjoiMmIwYzcxZmItMzE5Ny00YjcyLWE0NzctNWQzOWU5Y2Y2YmU2IiwiYXBwRGVmSWQiOiIxNDUxN2UxYS0zZmYwLWFmOTgtNDA4ZS0yYmQ2OTUzYzM2YTIiLCJtZXRhU2l0ZUlkIjoiMTFmYjQ5ZGYtYjA0OC00YzdjLWI0YjYtYWRmNTc1MGZmZWE4Iiwic2lnbkRhdGUiOiIyMDI1LTA0LTA1VDEzOjAwOjExLjc3NVoiLCJkZW1vTW9kZSI6ZmFsc2UsIm9yaWdpbkluc3RhbmNlSWQiOiI1YWVlN2Q0Yi1hMjdlLTRlMjUtOTY5Ny1kYWIwM2E0NTNjZTAiLCJhaWQiOiI0MmY1NTMxNC1iOTlmLTQ0NzgtYjU4Yi0xZTQ4NTllYzg0ODUiLCJiaVRva2VuIjoiM2FmNzM4MjQtODFkZi0wNzBlLTEwYzEtZjBjYzljYzA5NTRlIiwic2l0ZU93bmVySWQiOiI3OGRkYThiZS1lMTIyLTQyYTktYjc3Mi1mZWNhOTU0NGZkMDgiLCJicyI6Ikh6UmlQVEI3WC04TTFTZ1k4VDdNTlRacTlnTmxmeHhQTzlROFVVZFN0YTQuSWpJMVpHUmlZV1l4TFRjd1pHUXROR0pqTUMxaFpqZzJMV05tT1dZM1pqZGlPVEprTVNJIiwic2NkIjoiMjAyMi0wMS0wMlQyMDoyMTo0Ny4xNThaIn0


# 4 Make API query:
curl -s --get 'https://www.biofuranchem.com/_api/wix-ecommerce-storefront-web/api' \
    -d 'o=getFilteredProducts' \
    -d 's=WixStoresWebClient' \
    -d $'q=query,getFilteredProductsWithHasDiscount($mainCollectionId:String\u0021,$filters:ProductFilters,$sort:ProductSort,$offset:Int,$limit:Int,$withOptions:Boolean,=,false,$withPriceRange:Boolean,=,false){catalog{category(categoryId:$mainCollectionId){numOfProducts,productsWithMetaData(filters:$filters,limit:$limit,sort:$sort,offset:$offset,onlyVisible:true){totalCount,list{id,options{id,key,title,@include(if:$withOptions),optionType,@include(if:$withOptions),selections,@include(if:$withOptions){id,value,description,key,inStock}}productItems,@include(if:$withOptions){id,optionsSelections,price,formattedPrice}productType,price,sku,isInStock,urlPart,formattedPrice,name,description,brand,priceRange(withSubscriptionPriceRange:true),@include(if:$withPriceRange){fromPriceFormatted}}}}}}' \
    --data-urlencode 'v={"mainCollectionId":"00000000-000000-000000-000000000001","offset":0,"limit":'${query_limit}',"sort":null,"filters":{"term":{"field":"name","op":"CONTAINS","values":["*'${search_term}'*"]}},"withOptions":true,"withPriceRange":false}' \
  -H 'Authorization: '${auth_token} \
  -H 'X-XSRF-TOKEN: '${xsrf_token} \
  -H 'Content-Type: application/json; charset=utf-8' |
  jq '.data.catalog.category.productsWithMetaData.list'


curl -s 'https://www.biofuranchem.com/_api/wix-ecommerce-storefront-web/api?o=getFilteredProducts&s=WixStoresWebClient&q=query%2CgetFilteredProductsWithHasDiscount%28%24mainCollectionId%3AString%21%2C%24filters%3AProductFilters%2C%24sort%3AProductSort%2C%24offset%3AInt%2C%24limit%3AInt%2C%24withOptions%3ABoolean%2C%3D%2Cfalse%2C%24withPriceRange%3ABoolean%2C%3D%2Cfalse%29%7Bcatalog%7Bcategory%28categoryId%3A%24mainCollectionId%29%7BnumOfProducts%2CproductsWithMetaData%28filters%3A%24filters%2Climit%3A%24limit%2Csort%3A%24sort%2Coffset%3A%24offset%2ConlyVisible%3Atrue%29%7BtotalCount%2Clist%7Bid%2Coptions%7Bid%2Ckey%2Ctitle%2C%40include%28if%3A%24withOptions%29%2CoptionType%2C%40include%28if%3A%24withOptions%29%2Cselections%2C%40include%28if%3A%24withOptions%29%7Bid%2Cvalue%2Cdescription%2Ckey%2CinStock%7D%7DproductItems%2C%40include%28if%3A%24withOptions%29%7Bid%2CoptionsSelections%2Cprice%2CformattedPrice%7DproductType%2Cprice%2Csku%2CisInStock%2CurlPart%2CformattedPrice%2Cname%2Cdescription%2Cbrand%2CpriceRange%28withSubscriptionPriceRange%3Atrue%29%2C%40include%28if%3A%24withPriceRange%29%7BfromPriceFormatted%7D%7D%7D%7D%7D%7D&v=%7B%22mainCollectionId%22%3A+%2200000000-000000-000000-000000000001%22%2C+%22offset%22%3A+0%2C+%22limit%22%3A+100%2C+%22sort%22%3A+null%2C+%22filters%22%3A+%7B%22term%22%3A+%7B%22field%22%3A+%22name%22%2C+%22op%22%3A+%22CONTAINS%22%2C+%22values%22%3A+%5B%22%2A%27acid%27%2A%22%5D%7D%7D%2C+%22withOptions%22%3A+true%2C+%22withPriceRange%22%3A+false%7D' \
    -H 'Authorization: 5cHeUaqulML6lPZalZ-sFBaigbK_jyqtPBUyp4MQCHo.eyJpbnN0YW5jZUlkIjoiMjI1N2U2ODMtNjg2Yy00NjRkLTkzMTAtMjVmZTNjMjRlN2Q0IiwiYXBwRGVmSWQiOiIxMzgwYjcwMy1jZTgxLWZmMDUtZjExNS0zOTU3MWQ5NGRmY2QiLCJtZXRhU2l0ZUlkIjoiMTFmYjQ5ZGYtYjA0OC00YzdjLWI0YjYtYWRmNTc1MGZmZWE4Iiwic2lnbkRhdGUiOiIyMDI1LTA0LTA2VDEzOjU3OjMxLjM4NloiLCJ2ZW5kb3JQcm9kdWN0SWQiOiJzdG9yZXNfc2lsdmVyIiwiZGVtb01vZGUiOmZhbHNlLCJvcmlnaW5JbnN0YW5jZUlkIjoiMDc5ZjFlMmItMWNlZi00ZWY1LWJlN2QtODcwYjc4NDNkMTI5IiwiYWlkIjoiODkzNTYwZmUtYzg4OC00NmJlLTgxZWEtMTFiNDgwOTZkMDJmIiwiYmlUb2tlbiI6IjMzYWNhZjVjLWQ4MjQtMGEzMS0yN2E2LTg4MGI0OTJiMTk3YyIsInNpdGVPd25lcklkIjoiNzhkZGE4YmUtZTEyMi00MmE5LWI3NzItZmVjYTk1NDRmZDA4IiwiYnMiOiIzcWJEVll4aEZWZFY4bEZpQ0VYVEdUeE0xUjdrSWZtQld3d1o5NUR4NTlzLkltWmpOR1ptWmpjeExUUTNOMk10TkdJNE9DMWlNelJrTFdKaE4yWXhZalJpTmpBM01pSSIsInNjZCI6IjIwMjItMDEtMDJUMjA6MjE6NDcuMTU4WiJ9' \
    -H 'X-XSRF-TOKEN: 1743947851|kASoVETBADvw' |
  jq '.data.catalog.category.productsWithMetaData.list'
