from curl_cffi.requests.cookies import CookieTypes
from curl_cffi.requests.headers import HeaderTypes

cookies: CookieTypes = {
    "client-session-bind": "055a8b8b-38ee-4d1a-88b2-00d2f3f4036e",
    "server-session-bind": "055a8b8b-38ee-4d1a-88b2-00d2f3f4036e",
}

headers: HeaderTypes = {
    "content-type": "application/json;charset=utf-8",
    "etag": "W/\"e2c7bcd69db0bf519d57b89f8b4dee85\"",
    "x-envoy-upstream-service-time": "57",
    "age": "0",
    "x-wix-request-id": "1744606569.71859319029063953267",
    "cache-control": "public,max-age=0,must-revalidate",
    "server": "Pepyaka",
    "x-content-type-options": "nosniff",
    "content-encoding": "br",
    "accept-ranges": "bytes",
    "date": "Mon, 14 Apr 2025 04:56:09 GMT",
    "x-served-by": "cache-bur-kbur8200128-BUR",
    "x-cache": "MISS",
    "vary": "Accept-Encoding",
    "server-timing": "cache;desc=miss, varnish;desc=miss_miss, dc;desc=fastly_uw2-pub-1_g",
    "set-cookie": "client-session-bind=055a8b8b-38ee-4d1a-88b2-00d2f3f4036e; Path=/; Secure; SameSite=Lax;, server-session-bind=055a8b8b-38ee-4d1a-88b2-00d2f3f4036e; Path=/; Secure; SameSite=Lax; HttpOnly;",
    "x-seen-by": "yvSunuo/8ld62ehjr5B7kA==,T7xPrjRFKDMHVv938PYVfx9slopJdhD+WySraMrpIY8=,m0j2EEknGIVUW/liY8BLLgusAIMgWk1Brq+Ibw9VA8kG/hKs8AeY1T4OIbgnD+yx,2d58ifebGbosy5xc+FRalmYjQjlVvnxyj3Gd1PFJj2jymsdglN1UE/8d/7c688ag2mfjnHH7ZVYPa7oyjEKT4g==,2UNV7KOq4oGjA5+PKsX47NvcbHKbYhM0YAEePb/2IAkG/hKs8AeY1T4OIbgnD+yx,R8nVwPJv9QJL1m78OROO+Nc4fHxTiE33kcCYOAxvT9E=",
    "via": "1.1 google",
    "glb-x-seen-by": "bS8wRlGzu0Hc+WrYuHB8QIg44yfcdCMJRkBoQ1h6Vjc=",
    "alt-svc": "h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000",
}
query_water = {
    "data": {
        "catalog": {
            "category": {
                "numOfProducts": 632,
                "productsWithMetaData": {
                    "totalCount": 1,
                    "list": [
                        {
                            "id": "904ea4b8-5cc2-c400-d43e-2ed93fa1e71f",
                            "options": [
                                {
                                    "id": "opt-20",
                                    "key": "Size",
                                    "title": "Size",
                                    "optionType": "DROP_DOWN",
                                    "selections": [
                                        {
                                            "id": 1,
                                            "value": "100G",
                                            "description": "100G",
                                            "key": "100G",
                                            "inStock": None,
                                        },
                                        {
                                            "id": 2,
                                            "value": "500g",
                                            "description": "500g",
                                            "key": "500g",
                                            "inStock": None,
                                        },
                                        {"id": 3, "value": "1kg", "description": "1kg", "key": "1kg", "inStock": None},
                                        {"id": 4, "value": "5kg", "description": "5kg", "key": "5kg", "inStock": None},
                                        {
                                            "id": 5,
                                            "value": "10kg",
                                            "description": "10kg",
                                            "key": "10kg",
                                            "inStock": None,
                                        },
                                        {
                                            "id": 6,
                                            "value": "15kg",
                                            "description": "15kg",
                                            "key": "15kg",
                                            "inStock": None,
                                        },
                                    ],
                                }
                            ],
                            "productItems": [
                                {
                                    "id": "22c85282-0a22-4e5c-bb02-9b26e47d2443",
                                    "optionsSelections": [4],
                                    "price": 429.29,
                                    "formattedPrice": "$429.29",
                                },
                                {
                                    "id": "dbbce921-61fe-4288-be04-6a091d5eb09c",
                                    "optionsSelections": [5],
                                    "price": 643.94,
                                    "formattedPrice": "$643.94",
                                },
                                {
                                    "id": "fea267a9-6353-4cea-b99d-f8a249b34f3f",
                                    "optionsSelections": [6],
                                    "price": 1094.69,
                                    "formattedPrice": "$1,094.69",
                                },
                                {
                                    "id": "65e38095-1599-4d7b-870e-df21476ea3ee",
                                    "optionsSelections": [1],
                                    "price": 23.36,
                                    "formattedPrice": "$23.36",
                                },
                                {
                                    "id": "d2440fc7-a0dc-4266-9d40-2847b1a0338b",
                                    "optionsSelections": [2],
                                    "price": 81.77,
                                    "formattedPrice": "$81.77",
                                },
                                {
                                    "id": "1491a0e0-3ce3-4ed7-9cc1-d67bb8a08b0b",
                                    "optionsSelections": [3],
                                    "price": 122.65,
                                    "formattedPrice": "$122.65",
                                },
                            ],
                            "productType": "physical",
                            "price": 23.36,
                            "sku": "",
                            "isInStock": True,
                            "urlPart": "potassium-oleate-paste-in-water-cas-143-18-0",
                            "formattedPrice": "$23.36",
                            "name": "Potassium oleate paste in water, CAS 143-18-0",
                            "description": "<p>Appearance: yellowish, viscous liquid or paste</p><p>CAS: 143-18-0</p><p>Product ID: OLE14P</p><p>Purity: 80%+</p><p>Formula: C18H33KO2</p><p>MW: 320.55g/mol</p><p>pH: 9-12 (10wt% aqueous solution)</p><p>Density: 1.0g/mL+</p><p>Solubility: water / alcohol soluble</p><p>HS Code: 291615</p><p>MDL: MFCD00064243</p><p>SMILES: [K+].[H]C(CCCCCCCC)=C(/[H])CCCCCCCC([O-])=O</p><p>LD50 (rat, oral) &gt; 5,000mg/kg</p>",
                            "brand": None,
                        }
                    ],
                },
            }
        }
    }
}


query_5949_29_1 = {
    "data": {
        "catalog": {
            "category": {
                "numOfProducts": 632,
                "productsWithMetaData": {
                    "totalCount": 1,
                    "list": [
                        {
                            "id": "3e87ca61-d026-be20-a34f-11d6239e0c80",
                            "options": [
                                {
                                    "id": "opt-20",
                                    "key": "Size",
                                    "title": "Size",
                                    "optionType": "DROP_DOWN",
                                    "selections": [
                                        {"id": 1, "value": "25g", "description": "25g", "key": "25g", "inStock": None},
                                        {"id": 2, "value": "50g", "description": "50g", "key": "50g", "inStock": None},
                                        {
                                            "id": 3,
                                            "value": "100g",
                                            "description": "100g",
                                            "key": "100g",
                                            "inStock": None,
                                        },
                                        {
                                            "id": 4,
                                            "value": "500g",
                                            "description": "500g",
                                            "key": "500g",
                                            "inStock": None,
                                        },
                                        {"id": 5, "value": "1kg", "description": "1kg", "key": "1kg", "inStock": None},
                                    ],
                                }
                            ],
                            "productItems": [
                                {
                                    "id": "0960c421-cb5d-4f75-80fd-04f167f390d9",
                                    "optionsSelections": [4],
                                    "price": 76.0,
                                    "formattedPrice": "$76.00",
                                },
                                {
                                    "id": "1a146ad4-428b-4c89-b68f-684ae80b28eb",
                                    "optionsSelections": [5],
                                    "price": 114.0,
                                    "formattedPrice": "$114.00",
                                },
                                {
                                    "id": "d198cf89-b43d-49ba-8c78-4993b83d1fa7",
                                    "optionsSelections": [1],
                                    "price": 13.52,
                                    "formattedPrice": "$13.52",
                                },
                                {
                                    "id": "b964852c-7c83-4c06-9d09-926546811a07",
                                    "optionsSelections": [2],
                                    "price": 20.27,
                                    "formattedPrice": "$20.27",
                                },
                                {
                                    "id": "179e29e4-35cc-4626-a398-f43e9f1ba5a1",
                                    "optionsSelections": [3],
                                    "price": 30.4,
                                    "formattedPrice": "$30.40",
                                },
                            ],
                            "productType": "physical",
                            "price": 13.52,
                            "sku": "",
                            "isInStock": True,
                            "urlPart": "citric-acid-monohydrate-cas-5949-29-1",
                            "formattedPrice": "$13.52",
                            "name": "Citric acid monohydrate, CAS 5949-29-1",
                            "description": "<p>Appearance: colorless crystalline powder</p><p>CAS: 5949-29-1</p><p>Product ID: CITH</p><p>Purity: 99%+</p><p>Formula: C6H10O8</p><p>MW: 210.14g/mol</p><p>MP: 135-152C</p><p>Solubility: alcohol soluble</p><p>HS Code: 291814</p><p>MDL: MFCD00149972</p><p>SMILES: O.OC(=O)CC(O)(CC(O)=O)C(O)=O</p><p>LD50 (rat, oral) &gt;3,000mg/kg</p><p>TSCA: Yes</p>",
                            "brand": None,
                        }
                    ],
                },
            }
        }
    }
}


query_nonsense = {
    "data": {"catalog": {"category": {"numOfProducts": 632, "productsWithMetaData": {"totalCount": 0, "list": []}}}}
}


query_9999_99_99 = {
    "data": {"catalog": {"category": {"numOfProducts": 632, "productsWithMetaData": {"totalCount": 0, "list": []}}}}
}
