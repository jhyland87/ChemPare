from suppliers.supplier_base import SupplierBase, TypeProduct, TypeSupplier
from typing import Tuple, Optional, NoReturn
from bs4 import BeautifulSoup


# File: /suppliers/supplier_labchem.py
class SupplierLabchem(SupplierBase):
    """
    Todo: It looks like for LabChem, if you want to do a CAS Search, you first have to query a product
          search page with the CAS, which returns HTML, then look for all 'a.log-addTocart-btn elements',
          grab the 'id' value, then send a GET request to the getPriceDetailPage.action page with the
          comma separated list of id's as the 'productIdList' parameter. Example below:
          https://www.labchem.com/getPriceDetailPage.action?productIdList=LC261700-L03,LC261700-L27
    """

    _supplier: TypeSupplier = dict(
        name="Labchem",
        # location = 'Poland',
        base_url="https://www.labchem.com/",
    )
    """Supplier specific data"""

    allow_cas_search: bool = True
    """Determines if the supplier allows CAS searches in addition to name searches"""

    def _query_products(self, query: str) -> NoReturn:
        # Search types/ID's:
        #   desc = -1
        #   searchCustomerPartNumber = 1
        #   manufacturer_part_num = 3
        #   casno = 11
        #   formula = 12
        # searchPage.action?keyWord=mercury&srchTyp=4&overRideCatId=N

        get_params = dict(keyWord=query, overRideCatId="N", resultPage=60)

        if self._is_cas(query) is True:
            get_params["srchTyp"] = 11
        else:
            get_params["srchTyp"] = -1

        # 1) Query the main product search page (returns HTML, but does not include prices)
        self._query_results = self.http_get_html("searchPage.action", params=get_params)

    def __query_products_autocomplete(self) -> NoReturn:
        """Query products from supplier"""

        # Example request url for Labchem Supplier
        # https://www.labchem.com/AutoComplete.slt?q=mercury&limit=20
        #
        get_params = {
            "limit": self._limit,
            "q": self._query,
            "timestamp": 1739971044228,
            "width": "395px",
            "_": 1739962847766,
        }

        search_result = self.http_get_json("AutoComplete.slt", params=get_params)

        if not search_result:
            return

        self._query_results = search_result["response"]["docs"]["item"][0 : self._limit]

    def _parse_products(self) -> NoReturn:
        """Parse product query results.

        Iterate over the products returned from self._query_products, creating new requests
        for each to get the HTML content of the individual product page, and creating a
        new TypeProduct object for each to add to _products
        """

        product_page_soup = BeautifulSoup(self._query_results, "html.parser")

        # 2) Get the product ID's from the search page
        product_part_elems = product_page_soup.find_all("a", class_="log-addTocart-btn")

        # If no products were found, don't process anything
        if product_part_elems is None or len(product_part_elems) == 0:
            return

        product_part_numbers = [n.attrs["id"] for n in product_part_elems]

        # 3) Query for the price information using the part numbers
        product_prices = self.__query_products_prices(product_part_numbers)
        product_containers = product_page_soup.find_all("li", class_="listView")

        for product_elem in product_containers[: self._limit]:
            product_obj = self.__parse_product(product_elem)
            product_obj.price = product_prices.get(product_obj.mpn)
            self._products.append(product_obj)

    def __parse_product(self, product_elem: BeautifulSoup) -> TypeProduct:
        inputs = product_elem.find_all("input")
        link = product_elem.find("div", class_="prodImage").find("a").attrs["href"]
        cas = product_elem.find("ul", class_="otherNumWrap").find("span")

        # Get the compare ID, which is necessary since its used in some element identifiers
        compare_id = next(
            x.attrs["value"] for x in inputs if x.attrs["name"] == "compareId"
        )
        part_number = next(
            x.attrs["value"]
            for x in inputs
            if x.attrs["id"] == f"partNumber_{compare_id}"
        )
        mpn_value = next(
            x.attrs["id"]
            for x in inputs
            if x.attrs["value"] == part_number and x.attrs["id"].startswith("MPNValue_")
        )
        mpn_value = mpn_value.replace("MPNValue_", "")

        title_elem = product_elem.find("h4").find("a").get_text(strip=True)

        _product = TypeProduct(
            name=title_elem,
            title=title_elem,
            supplier=self._supplier["name"],
            mpn=mpn_value,
            uuid=compare_id,
            url=self._supplier["base_url"] + link,
        )

        if cas:
            _product.cas = (cas.get_text(strip=True),)

        return _product.cast_properties()

    def __query_products_prices(self, part_numbers: Tuple[str, list]) -> Optional[dict]:
        """Query specific product prices by their part numeber(s)

        Args:
            part_numbers (str|list): partnumber(s) of chem(s) to query for.

        Returns:
            dict: lookup dictionary with the part number and list price values
        """

        if part_numbers is None or len(part_numbers) == 0:
            return None

        if type(part_numbers) is list:
            part_numbers = ",".join(part_numbers)

        params = {"productIdList": part_numbers}

        product_json = self.http_get_json("getPriceDetailPage.action", params=params)

        res = dict()

        for p in product_json:
            res[p["partNumber"]] = (
                str(p["listPrice"]).strip() if p["listPrice"] else None
            )

        return res


if __package__ == "suppliers":
    __disabled__ = False
