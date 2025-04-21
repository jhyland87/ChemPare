#!/usr/bin/env bash

query_limit=20
query="${1:-acid}"
base_url='https://www.biofuranchem.com'

echo "Querying biocuranchem for ${query}..." >&2


# 1 Get the session binding from the initial request headers
session_bind=$(curl "${base_url}" \
  --get --silent --head \
  --data "Category=All" \
  --header 'sec-fetch-mode: navigate' \
  --header 'sec-fetch-dest: document' \
  --header 'sec-fetch-site: none' \
  -H 'sec-fetch-user: ?1' |
  jc --curl-head |
  jq --raw-output '.[0]."set-cookie"[] | select( . | contains("client-session-bind")) | split(";") | .[0] | split("=") | .[1]')


echo "session_bind: ${session_bind}" >&2

# 2 Get the XSRF id thingy
xsrf_token=$(curl "${base_url}" \
  --get --silent --head \
  --request-target '/_api/wix-laboratory-server/laboratory/conductAllInScope' \
  --data 'scope=wix-one-app' \
  --cookie 'server-session-bind='${session_bind}'; ssr-caching=cache#desc=miss#varnish=miss_miss#dc#desc=fastly_uw2-pub-1_g' |
  jc --curl-head |
  jq --raw-output '.[0]."set-cookie"[] | split("; ") | .[]| select( . | contains("XSRF-TOKEN")) | split("=") | .[1]')

echo "xsrf_token: ${xsrf_token}" >&2

# 3 Get the website instance ID ("access tokens" I guess?)
auth_token=$(curl "${base_url}" \
  --get --silent \
  --request-target '/_api/v1/access-tokens' \
  -H 'client-binding: '${session_bind} \
  -b 'server-session-bind='${session_bind}'; XSRF-TOKEN='${xsrf_token} |
  jq --raw-output '.apps["1380b703-ce81-ff05-f115-39571d94dfcd"].instance')

echo "auth_token: ${auth_token}" >&2

echo -e "Results:\n\n"  >&2

# 4 Make API query:
# curl -s --get "${base_url}/_api/wix-ecommerce-storefront-web/api" \
#   -d 'o=getFilteredProducts' \
#   -d 's=WixStoresWebClient' \
#   -d $'q=query,getFilteredProductsWithHasDiscount($mainCollectionId:String\u0021,$filters:ProductFilters,$sort:ProductSort,$offset:Int,$limit:Int,$withOptions:Boolean,=,false,$withPriceRange:Boolean,=,false){catalog{category(categoryId:$mainCollectionId){numOfProducts,productsWithMetaData(filters:$filters,limit:$limit,sort:$sort,offset:$offset,onlyVisible:true){totalCount,list{id,options{id,key,title,@include(if:$withOptions),optionType,@include(if:$withOptions),selections,@include(if:$withOptions){id,value,description,key,inStock}}productItems,@include(if:$withOptions){id,optionsSelections,price,formattedPrice}productType,price,sku,isInStock,urlPart,formattedPrice,name,description,brand,priceRange(withSubscriptionPriceRange:true),@include(if:$withPriceRange){fromPriceFormatted}}}}}}' \
#   --data-urlencode 'v={"mainCollectionId":"00000000-000000-000000-000000000001","offset":0,"limit":'${query_limit}',"sort":null,"filters":{"term":{"field":"name","op":"CONTAINS","values":["*'${query}'*"]}},"withOptions":true,"withPriceRange":false}' \
#   -H 'Authorization: '${auth_token} \
#   -H 'X-XSRF-TOKEN: '${xsrf_token} \
#   -H 'Content-Type: application/json; charset=utf-8' | jq '.data.catalog.category.numOfProducts'


curl -s --get \
    --variable "base=${base_url}" \
    --expand-url '{{base}}/_api/wix-ecommerce-storefront-web/api' \
    -d 'o=getFilteredProducts' \
    -d 's=WixStoresWebClient' \
    -d $'q=query,getFilteredProductsWithHasDiscount($mainCollectionId:String\u0021,$filters:ProductFilters,$sort:ProductSort,$offset:Int,$limit:Int,$withOptions:Boolean,=,false,$withPriceRange:Boolean,=,false){catalog{category(categoryId:$mainCollectionId){numOfProducts,productsWithMetaData(filters:$filters,limit:$limit,sort:$sort,offset:$offset,onlyVisible:true){totalCount,list{id,options{id,key,title,@include(if:$withOptions),optionType,@include(if:$withOptions),selections,@include(if:$withOptions){id,value,description,key,inStock}}productItems,@include(if:$withOptions){id,optionsSelections,price,formattedPrice}productType,price,sku,isInStock,urlPart,formattedPrice,name,description,brand,priceRange(withSubscriptionPriceRange:true),@include(if:$withPriceRange){fromPriceFormatted}}}}}}' \
    --data-urlencode 'v={"mainCollectionId":"00000000-000000-000000-000000000001","offset":0,"limit":'${query_limit}',"sort":null,"filters":{"term":{"field":"name","op":"CONTAINS","values":["*'${query}'*"]}},"withOptions":true,"withPriceRange":false}' \
    -H 'Authorization: '${auth_token} \
    -H 'X-XSRF-TOKEN: '${xsrf_token} \
    -H 'Content-Type: application/json; charset=utf-8' | jq '.data.catalog.category.numOfProducts'



# curl -s --get \
#     --variable 'base=https://www.biofuranchem.com' \
#     --expand-url '{{base}}/_api/wix-ecommerce-storefront-web/api' \
#     -d 'o=getFilteredProducts' \
#     -d 's=WixStoresWebClient' \
#     -d $'q=query,getFilteredProductsWithHasDiscount($mainCollectionId:String\u0021,$filters:ProductFilters,$sort:ProductSort,$offset:Int,$limit:Int,$withOptions:Boolean,=,false,$withPriceRange:Boolean,=,false){catalog{category(categoryId:$mainCollectionId){numOfProducts,productsWithMetaData(filters:$filters,limit:$limit,sort:$sort,offset:$offset,onlyVisible:true){totalCount,list{id,options{id,key,title,@include(if:$withOptions),optionType,@include(if:$withOptions),selections,@include(if:$withOptions){id,value,description,key,inStock}}productItems,@include(if:$withOptions){id,optionsSelections,price,formattedPrice}productType,price,sku,isInStock,urlPart,formattedPrice,name,description,brand,priceRange(withSubscriptionPriceRange:true),@include(if:$withPriceRange){fromPriceFormatted}}}}}}' \
#     --data-urlencode 'v={"mainCollectionId":"00000000-000000-000000-000000000001","offset":0,"limit":1,"sort":null,"filters":{"term":{"field":"name","op":"CONTAINS","values":["*acid*"]}},"withOptions":true,"withPriceRange":false}' \
#     -H 'Authorization: tAwlpYJYZF2AlS5HAXpXeLWLy-xdJM9tJkiRQg5d_yw.eyJpbnN0YW5jZUlkIjoiMjI1N2U2ODMtNjg2Yy00NjRkLTkzMTAtMjVmZTNjMjRlN2Q0IiwiYXBwRGVmSWQiOiIxMzgwYjcwMy1jZTgxLWZmMDUtZjExNS0zOTU3MWQ5NGRmY2QiLCJtZXRhU2l0ZUlkIjoiMTFmYjQ5ZGYtYjA0OC00YzdjLWI0YjYtYWRmNTc1MGZmZWE4Iiwic2lnbkRhdGUiOiIyMDI1LTA0LTIwVDE1OjQ3OjQxLjE2MFoiLCJ2ZW5kb3JQcm9kdWN0SWQiOiJzdG9yZXNfc2lsdmVyIiwiZGVtb01vZGUiOmZhbHNlLCJvcmlnaW5JbnN0YW5jZUlkIjoiMDc5ZjFlMmItMWNlZi00ZWY1LWJlN2QtODcwYjc4NDNkMTI5IiwiYWlkIjoiMWE2OTdhMmItNTMwOS00ODViLWEwZTktNjBhODY0ZDFiYWE4IiwiYmlUb2tlbiI6IjMzYWNhZjVjLWQ4MjQtMGEzMS0yN2E2LTg4MGI0OTJiMTk3YyIsInNpdGVPd25lcklkIjoiNzhkZGE4YmUtZTEyMi00MmE5LWI3NzItZmVjYTk1NDRmZDA4IiwiYnMiOiJlekM1X3NtdzUxTU11eHpTdXEyMVItb2RORmY1SmNwVGU0SlFqMlhCQTFzLklqY3hPVEk1TVRRMkxXWm1NRE10TkRNd1l5MWlZbVUzTFRobE9UY3pOelUxWVRObE5pSSIsInNjZCI6IjIwMjItMDEtMDJUMjA6MjE6NDcuMTU4WiJ9' \
#     -H 'X-XSRF-TOKEN: 1745164060|nXga95aKdwUc' \
#     -H 'Content-Type: application/json; charset=utf-8' | jq '.data.catalog.category.numOfProducts'
