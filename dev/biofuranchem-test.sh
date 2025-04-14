#!/usr/bin/env bash

query_limit=20
query="${1:-acid}"

echo "Querying biocuranchem for ${query}..." >&2

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


echo "session_bind: ${session_bind}" >&2

# 2 Get the XSRF id thingy
xsrf_token=$(curl 'https://www.biofuranchem.com' \
  --get --silent --head \
  --request-target '/_api/wix-laboratory-server/laboratory/conductAllInScope' \
  --data 'scope=wix-one-app' \
  --cookie 'server-session-bind='${session_bind}'; ssr-caching=cache#desc=miss#varnish=miss_miss#dc#desc=fastly_uw2-pub-1_g' |
  jc --curl-head |
  jq --raw-output '.[0]."set-cookie"[] | split("; ") | .[]| select( . | contains("XSRF-TOKEN")) | split("=") | .[1]')

echo "xsrf_token: ${xsrf_token}" >&2

# 3 Get the website instance ID ("access tokens" I guess?)
auth_token=$(curl 'https://www.biofuranchem.com' \
  --get --silent \
  --request-target '/_api/v1/access-tokens' \
  -H 'client-binding: '${session_bind} \
  -b 'server-session-bind='${session_bind}'; XSRF-TOKEN='${xsrf_token} |
  jq --raw-output '.apps["1380b703-ce81-ff05-f115-39571d94dfcd"].instance')

echo "auth_token: ${auth_token}" >&2

echo -e "Results:\n\n"  >&2

# 4 Make API query:
curl -s --get 'https://www.biofuranchem.com/_api/wix-ecommerce-storefront-web/api' \
  -d 'o=getFilteredProducts' \
  -d 's=WixStoresWebClient' \
  -d $'q=query,getFilteredProductsWithHasDiscount($mainCollectionId:String\u0021,$filters:ProductFilters,$sort:ProductSort,$offset:Int,$limit:Int,$withOptions:Boolean,=,false,$withPriceRange:Boolean,=,false){catalog{category(categoryId:$mainCollectionId){numOfProducts,productsWithMetaData(filters:$filters,limit:$limit,sort:$sort,offset:$offset,onlyVisible:true){totalCount,list{id,options{id,key,title,@include(if:$withOptions),optionType,@include(if:$withOptions),selections,@include(if:$withOptions){id,value,description,key,inStock}}productItems,@include(if:$withOptions){id,optionsSelections,price,formattedPrice}productType,price,sku,isInStock,urlPart,formattedPrice,name,description,brand,priceRange(withSubscriptionPriceRange:true),@include(if:$withPriceRange){fromPriceFormatted}}}}}}' \
  --data-urlencode 'v={"mainCollectionId":"00000000-000000-000000-000000000001","offset":0,"limit":'${query_limit}',"sort":null,"filters":{"term":{"field":"name","op":"CONTAINS","values":["*'${query}'*"]}},"withOptions":true,"withPriceRange":false}' \
  -H 'Authorization: '${auth_token} \
  -H 'X-XSRF-TOKEN: '${xsrf_token} \
  -H 'Content-Type: application/json; charset=utf-8' | jq --raw-output
