from __future__ import annotations

import json
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup, ResultSet

from chempare.suppliers import SupplierBase
from chempare.utils import _cas, _html, _quantity

if TYPE_CHECKING:
    from typing import Any, ClassVar, Final

    from datatypes import PriceType, ProductType, QuantityType, SupplierType, VariantType


# File: /suppliers/supplier_carolinachemical.py
class SupplierCarolinaChemical(SupplierBase):

    _supplier: Final[SupplierType] = {
        "name": "Carolina Chemical",
        # location=None,
        "base_url": "https://carolinachemical.com",
        "api_url": "https://carolinachemical.com",
    }
    """Supplier specific data"""

    allow_cas_search: Final[bool] = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    __defaults: ClassVar[PriceType] = {
        "currency_symbol": "$",
        "currency": "USD",
        "price": 0.0,  # Default price value
        # "is_restricted": False,
    }
    """Default values applied to products from this supplier"""

    def _query_products(self) -> None:
        """Query products from supplier

        Args:
            query (str): Query string to use
        """

        get_params = {"search": self._query}

        self._query_results = self.http_get_json("wp-json/wp/v2/search", params=get_params)

    # Method iterates over the product query results stored at
    # self._query_results and returns a list of ProductType objects.
    def _parse_products(self) -> None:
        for product_obj in self._query_results:
            # Add each product to the self._products list in the form of a
            # ProductType object.
            product_result = self._query_and_parse_product(product_obj)
            self._products.append(product_result)

    def _query_and_parse_product(self, product_obj: dict) -> ProductType:
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

        product = dict(**self.__defaults, url=product_obj.get("url"), supplier=self._supplier["name"])

        product_data = self.__query_product_page(product_obj["url"])

        product.update(product_data)

        return product

    def __query_product_page(self, product_url: str) -> dict[str, Any]:
        product_page = self.http_get_html(product_url)

        product_page_soup = BeautifulSoup(product_page, "html.parser")

        product_page_data: dict[str, Any] = {"url": product_url, "variants": []}

        product_variations = product_page_soup.find("form", class_="variations_form").attrs.get(  # type: ignore
            "data-product_variations"
        )
        if product_variations is None:
            raise ValueError("Failed to retrieve variant information for product")

        product_variations = json.loads(str(product_variations))

        for index, variant in enumerate(product_variations):
            variant_desc = BeautifulSoup(variant.get("variation_description"), "html.parser")

            quantity: QuantityType = _quantity.parse_quantity(variant.get("attributes").get("attribute_pa_size"))

            # Basic
            if quantity is not None:
                if quantity.get("quantity") is None and isinstance(quantity.get("uom"), str):
                    quantity["quantity"] = 1

                # variation.update(dict(quantity))

            variation: VariantType = {
                # _id=index,
                "title": str(variant_desc.get_text(strip=True)),
                "uuid": variant.get("variation_id"),
                "sku": variant.get("sku"),
                # description=variant_desc,
                "price": float(variant.get("display_price")),
                "quantity": quantity["quantity"],
                "uom": quantity.get("uom", "Piece"),
            }
            product_page_data["variants"].append(variation)

            if index == 0:
                product_page_data.update(variation)

        page_title = _html.text_from_element(product_page_soup.find("h1", class_="product_title"))
        # Get the title
        # title_elem: bs4.Tag | bs4.NavigableString | None = product_page_soup.find("h1", class_="product_title")

        product_page_data["title"] = page_title
        product_page_data["name"] = page_title

        # Get the CAS/formula/etc
        # .woocommerce-product-details__short-description > table > tbody > tr
        description_rows: ResultSet[Any] | Any = (
            product_page_soup.find("div", class_="woocommerce-product-details__short-description")
            .find('table')
            .find('tbody')
            .find_all('tr')
        )

        if isinstance(description_rows, ResultSet):
            for desc_row in description_rows:
                td = desc_row.find_all("td")
                attr = td[0].get_text(strip=True)
                val = td[1].get_text(strip=True)

                if _cas.is_cas(val):
                    product_page_data["cas"] = val
                    continue

                if attr == "Molecular Formula" and val:
                    product_page_data["formula"] = val
                    continue

        return product_page_data
