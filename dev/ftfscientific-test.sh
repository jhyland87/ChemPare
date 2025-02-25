#!/usr/bin/env bash

search_query="${1}"
function get_init_cookies {
    curl -sI  'https://www.ftfscientific.com/' \
        -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8' \
        -H 'accept-language: en-US,en;q=0.5' \
        -H 'cache-control: no-cache' \
        -H 'pragma: no-cache' \
        -H 'priority: u=0, i' \
        -H 'sec-ch-ua: "Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"' \
        -H 'sec-ch-ua-mobile: ?0' \
        -H 'sec-ch-ua-platform: "macOS"' \
        -H 'sec-fetch-dest: document' \
        -H 'sec-fetch-mode: navigate' \
        -H 'sec-fetch-site: none' \
        -H 'sec-fetch-user: ?1' \
        -H 'sec-gpc: 1' \
        -H 'upgrade-insecure-requests: 1' \
        -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36' | jc --curl-head | jq -rM '.[0].["set-cookie"][]' | awk -F';' '{print $1}' | awk 'BEGIN{ FS="="; IFS="=";OFS="=";}{k=$1; sub($1 FS,""); printf("%s %s\n", k, $0) }'
}


function get_auth_token {
    header="${1}"
    cookie="${2}"
    curl --silent 'https://www.ftfscientific.com/_api/v1/access-tokens' \
        -H 'accept: */*' \
        -H 'accept-language: en-US,en;q=0.5' \
        -H 'cache-control: no-cache' \
        -H "${header}" \
        -b "${cookie}" \
        -H 'pragma: no-cache' \
        -H 'priority: u=1, i' \
        -H 'referer: https://www.ftfscientific.com/' \
        -H 'sec-ch-ua: "Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"' \
        -H 'sec-ch-ua-mobile: ?0' \
        -H 'sec-ch-ua-platform: "macOS"' \
        -H 'sec-fetch-dest: empty' \
        -H 'sec-fetch-mode: cors' \
        -H 'sec-fetch-site: same-origin' \
        -H 'sec-gpc: 1' \
        -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36' | tee access-tokens.out | jq -r '.apps["1484cb44-49cd-5b39-9681-75188ab429de"].instance'
}

function search_ftf {
    access_token="${1}"
    query="${2}"

    curl --silent 'https://www.ftfscientific.com/_api/search-services-sitesearch/v1/search' \
        -H 'x-wix-brand: wix' \
        -H "authorization: ${access_token}" \
        -H 'Referer: https://www.ftfscientific.com/_partials/wix-thunderbolt/dist/clientWorker.2323647d.bundle.min.js' \
        -H 'X-Wix-Client-Artifact-Id: wix-thunderbolt' \
        -H 'commonConfig: %7B%22brand%22%3A%22wix%22%2C%22host%22%3A%22VIEWER%22%2C%22BSI%22%3A%22%22%2C%22siteRevision%22%3A%22316%22%2C%22renderingFlow%22%3A%22NONE%22%2C%22language%22%3A%22en%22%2C%22locale%22%3A%22en-us%22%7D' \
        -H 'x-wix-search-bi-correlation-id: 5c4da737-0647-42a5-6bcb-ea87a4718a8b' \
        -H 'Accept: application/json, text/plain, */*' \
        -H 'Content-Type: application/json' \
        -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36' \
        --data-raw '{"documentType":"public/stores/products","query":"'"${query}"'","paging":{"skip":0,"limit":12},"includeSeoHidden":false,"facets":{"clauses":[{"aggregation":{"name":"discountedPriceNumeric","aggregation":"MIN"}},{"aggregation":{"name":"discountedPriceNumeric","aggregation":"MAX"}},{"term":{"name":"collections","limit":999}}]},"ordering":{"ordering":[]},"language":"en","properties":[],"fuzzy":true,"fields":["description","title","id","currency","discountedPrice","inStock"]}' | tee -a query_responses.out | jq -r '.documents[].title'
}


header=""
cookie=""
while read cookie_name cookie_val; do
    #echo "cookie: $cookie_name is $cookie_val"
    if [[ $cookie_name == 'client-session-bind' ]]; then
        header_a="client-binding: ${cookie_val}"
        continue
    fi

    if [[ $cookie_name == 'server-session-bind' ]] || [[ $cookie_name == 'ssr-caching' ]]; then
        cookie="${cookie_name}=${cookie_val}; ${cookie}"
        continue
    fi
done <<< $(get_init_cookies)

access_token=$(get_auth_token "${header}" "${cookie}")

search_ftf "${access_token}" "${search_query}"