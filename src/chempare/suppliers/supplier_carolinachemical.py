import json
from typing import Any

from bs4 import BeautifulSoup

from chempare.datatypes import ProductType
from chempare.datatypes import SupplierType
from chempare.datatypes import VariantType
from chempare.suppliers.supplier_base import SupplierBase


# File: /suppliers/supplier_carolinachemical.py
class SupplierCarolinaChemical(SupplierBase):

    _supplier: SupplierType = SupplierType(
        name="Carolina Chemical",
        # location=None,
        base_url="https://carolinachemical.com",
        api_url="https://carolinachemical.com",
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    __defaults: dict = {
        "currency": "$",
        "currency_code": "USD",
        # "is_restricted": False,
    }
    """Default values applied to products from this supplier"""

    def _query_products(self, query: str) -> None:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        get_params = {"search": self._query}

        search_result = self.http_get_json("wp-json/wp/v2/search", params=get_params)

        if not search_result:
            return

        self._query_results = search_result

    # Method iterates over the product query results stored at
    # self._query_results and returns a list of ProductType objects.
    def _parse_products(self) -> None:
        for product_obj in self._query_results:
            # Add each product to the self._products list in the form of a
            # ProductType object.
            product_result = self._query_and_parse_product(product_obj)
            self._products.append(product_result)

    def _query_and_parse_product(self, product_obj: tuple[list, dict]) -> ProductType:
        """Parse single product and return single ProductType object

        Args:
            product_obj (tuple[list, dict]): Single product object from JSON

        Returns:
            ProductType: Instance of ProductType

        Todo:
            - It looks like each product has a shopify_variants array that
              stores data about the same product but in different quantities.
              This could maybe be included?
        """

        # {
        #     "id": 3202,
        #     "title": "Hydrochloric Acid 22 BE (36.25%)",
        #     "url": "https://carolinachemical.com/product/hydrochloric-acid-22-be-36-25-copy/",
        #     "type": "post",
        #     "subtype": "product",
        #     "_links": {
        #     "self": [
        #         {
        #         "embeddable": true,
        #         "href": "https://carolinachemical.com/wp-json/wp/v2/product/3202"
        #         }
        #     ],
        #     "about": [
        #         {
        #         "href": "https://carolinachemical.com/wp-json/wp/v2/types/product"
        #         }
        #     ],
        #     "collection": [
        #         {
        #         "href": "https://carolinachemical.com/wp-json/wp/v2/search"
        #         }
        #     ]
        #     }
        # },

        product = dict(
            **self.__defaults,
            url=product_obj["url"],
            # uuid=product_obj["product_id"],
            # name=product_obj["title"],
            # title=product_obj["title"],
            # description=(
            #     str(product_obj["description"]).strip()
            #     if product_obj["description"]
            #     else None
            # ),
            # price=f"{float(product_obj['price']):.2f}",
            # url="{0}{1}".format(self._supplier["base_url"], product_obj["link"]),
            # manufacturer=product_obj["vendor"],
            # supplier=self._supplier["name"],
        )

        product_data = self.__query_product_page(product_obj["url"])

        product.update(product_data)

        product = ProductType(**product)

        return product.cast_properties()

    def __query_product_page(self, product_url: str) -> dict[str, Any]:
        product_page = self.http_get_html(product_url)

        product_page_soup = BeautifulSoup(product_page, "html.parser")

        product_page_data = {"url": product_url, "variants": []}

        try:
            product_variations = product_page_soup.find("form", class_="variations_form").attrs.get(
                "data-product_variations"
            )

            if product_variations:
                product_variations = json.loads(product_variations)

            for index, variant in enumerate(product_variations):
                variation = VariantType(
                    # _id=index,
                    uuid=variant["variation_id"],
                    sku=variant["sku"],
                    description=variant["variation_description"],
                    price=variant["display_price"],
                    quantity=variant["attributes"]["attribute_pa_size"],
                )

                variation.set_id(index)

                if variation.description:
                    variation.description = BeautifulSoup(variation.description, "html.parser")
                    variation.description = variation.description.get_text(strip=True)

                product_page_data["variants"].append(variation)

                if index == 0:
                    product_page_data.update(dict(variation))

            # Get the title
            title_elem = product_page_soup.find("h1", class_="product_title")

            product_page_data["title"] = title_elem.get_text(strip=True)
            product_page_data["name"] = product_page_data["title"]

            # Get the CAS/formula/etc
            # .woocommerce-product-details__short-description > table > tbody > tr
            description_rows = (
                product_page_soup.find("div", class_="woocommerce-product-details__short-description")
                .find('table')
                .find('tbody')
                .find_all('tr')
            )

            for desc_row in description_rows:
                td = desc_row.find_all("td")
                attr = td[0].get_text(strip=True)
                val = td[1].get_text(strip=True)

                if self._is_cas(val):
                    product_page_data["cas"] = val
                    continue

                if attr == "Molecular Formula" and val:
                    product_page_data["formula"] = val
                    continue

        except Exception as err:
            print("Something failed:", err)

        return product_page_data


__supplier_class = SupplierCarolinaChemical
