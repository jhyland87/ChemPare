# pragma: exclude file
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

import chempare.utils as utils
from chempare.suppliers.supplier_base import SupplierBase

if TYPE_CHECKING:
    from typing import Any, ClassVar, Final

    from datatypes import ProductType, SupplierType


# File: /suppliers/supplier_labchem.py
class SupplierLabchem(SupplierBase):
    """
    Todo: It looks like for LabChem, if you want to do a CAS Search, you first
          have to query a product search page with the CAS, which returns HTML,
          then look for all 'a.log-addTocart-btn elements', grab the 'id'
          value, then send a GET request to the getPriceDetailPage.action page
          with the comma separated list of id's as the 'productIdList'
          parameter. Example below:
          https://www.labchem.com/getPriceDetailPage.action?productIdList=LC261700-L03,LC261700-L27
    """

    _supplier: Final[SupplierType] = {
        "name": "Labchem",
        # location = 'Poland',
        "base_url": "https://www.labchem.com",
    }
    """Supplier specific data"""

    allow_cas_search: Final[bool] = True
    """Determines if the supplier allows CAS searches in addition to name
    searches"""

    __defaults: ClassVar[dict[str, Any]] = {"currency": "$", "currency_code": "USD"}
    """Default values applied to products from this supplier"""

    _cookies: ClassVar[dict[str, Any]] = {
        'pagemode': 'gridView',
        'pc_debug': '',
        'pc_debug_x': 'null',
        'pc_debug_y': 'null',
        'pc_v_4jVxV9OCTyi5I8mvWtt7fA': 'HgF_3YRvT6qa2weat2bTaw',
        '__cf_bm': 'Ol7_TUtqmumqj16.ayzc7Xeo_LJxfBEXKAY15iya5QE-1745547173-1.0.1.1-b8pYHisMpI5ei3lbKJquUTACSkPUbbDYwvHkRIXMi78llXD8yihYYmWi4dFY_B6pYyx.J6c34nFJPMSNEPYgXhjRuoPbSXJ4CygSVuaqxxM',
        'cf_clearance': 'T3qB0XsANn0uVg0RWgcuOjm66mkdGBi0qofEVx.j5ZE-1745547177-1.2.1.1-ufab_88_cexgu4bSYhZz97Q3Fnij17fEtPZ2ZlHrssj0LiTOio0grxOSQqRYCUkuSqmUp8xBzSnMx9eRM0iCX08nvccBzr1XXt9EEH2X7TIJlbhrQx7mY6bLjopxQsSIiH2cJSJNcyB6TZjcBaTptcqpjMp3Z4ZfbbGlrj4bAQmPHPzGR.DhKWo.TL.Vw8U_PKhy339d1GYwKbjO_pOnfPrrk0EfMA9dx041XqBE7yPQLgj4KhSuVcyvbnmfsk8Wiegx0MMfPSrjvFswjKbuFWOrDAr2oL0wj2oP7nddC7FTWtIsXB7mvjGylVjT.RJH8hIeDbVS5_AZ57mjX5jtWK8PH80GZtD29inxmhVbyWZuEIQBqYv7GqJLeGKNiOsv',
        'JSESSIONID': 'E8ACBECBE976C097FFCF7BF18DCE0356',
        'pc_sessid_4jVxV9OCTyi5I8mvWtt7fA': '4NlMO1x3T3CdF4yFM9h17A',
    }

    _headers: ClassVar[dict[str, Any]] = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        'cache-control': 'no-cache',
        'content-type': 'text/plain;charset=UTF-8',
        'origin': 'https://www.labchem.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'cookie': 'pagemode=gridView; pc_debug=; pc_debug_x=null; pc_debug_y=null; pc_v_4jVxV9OCTyi5I8mvWtt7fA=HgF_3YRvT6qa2weat2bTaw; __cf_bm=Ol7_TUtqmumqj16.ayzc7Xeo_LJxfBEXKAY15iya5QE-1745547173-1.0.1.1-b8pYHisMpI5ei3lbKJquUTACSkPUbbDYwvHkRIXMi78llXD8yihYYmWi4dFY_B6pYyx.J6c34nFJPMSNEPYgXhjRuoPbSXJ4CygSVuaqxxM; cf_clearance=T3qB0XsANn0uVg0RWgcuOjm66mkdGBi0qofEVx.j5ZE-1745547177-1.2.1.1-ufab_88_cexgu4bSYhZz97Q3Fnij17fEtPZ2ZlHrssj0LiTOio0grxOSQqRYCUkuSqmUp8xBzSnMx9eRM0iCX08nvccBzr1XXt9EEH2X7TIJlbhrQx7mY6bLjopxQsSIiH2cJSJNcyB6TZjcBaTptcqpjMp3Z4ZfbbGlrj4bAQmPHPzGR.DhKWo.TL.Vw8U_PKhy339d1GYwKbjO_pOnfPrrk0EfMA9dx041XqBE7yPQLgj4KhSuVcyvbnmfsk8Wiegx0MMfPSrjvFswjKbuFWOrDAr2oL0wj2oP7nddC7FTWtIsXB7mvjGylVjT.RJH8hIeDbVS5_AZ57mjX5jtWK8PH80GZtD29inxmhVbyWZuEIQBqYv7GqJLeGKNiOsv; JSESSIONID=E8ACBECBE976C097FFCF7BF18DCE0356; pc_sessid_4jVxV9OCTyi5I8mvWtt7fA=4NlMO1x3T3CdF4yFM9h17A',
    }

    def _query_products(self) -> None:
        # Search types/ID's:
        #   desc = -1
        #   searchCustomerPartNumber = 1
        #   manufacturer_part_num = 3
        #   casno = 11
        #   formula = 12
        # searchPage.action?keyWord=mercury&srchTyp=4&overRideCatId=N

        get_params = dict(q=self._query, overRideCatId="N", resultPage=60)

        get_params["productIdList"] = (
            "LC101000-L02,LC101600-L03,LC103900-L03,LC179200-M02,LC271000-M02,LC102600-L03,LC258300-L04,LC102600-L04,LC153300-L04,LC153300-L03,LC258300-L02,LC153200-L04"
        )
        if utils.is_cas(self._query) is True:
            get_params["srchTyp"] = 11
        else:
            get_params["srchTyp"] = -1

        # 1) Query the main product search page (returns HTML, but does not
        # include prices)
        self._query_results = self.http_get_html(
            "searchPage.action", params=get_params, headers=self._headers, cookies=self._cookies
        )

    # def __query_products_autocomplete(self) -> None:
    #     """Query products from supplier"""

    #     # Example request url for Labchem Supplier
    #     # https://www.labchem.com/AutoComplete.slt?q=mercury&limit=20
    #     #
    #     get_params = {
    #         "limit": self._limit,
    #         "q": self._query,
    #         "timestamp": 1739971044228,
    #         "width": "395px",
    #         "_": 1739962847766,
    #     }

    #     search_result = self.http_get_json(
    #         "AutoComplete.slt", params=get_params, headers=self._headers, cookies=self._cookies
    #     )

    #     if not search_result:
    #         return

    #     self._query_results = search_result["response"]["docs"]["item"][: self._limit]

    def _parse_products(self) -> None:
        """Parse product query results.

        Iterate over the products returned from self._query_products, creating
        new requests for each to get the HTML content of the individual
        product page, and creating a new ProductType object for each to add
        to _products
        """
        # Check if title of rsult shows
        product_page_soup = BeautifulSoup(self._query_results, "html.parser")

        # Check if the page is loading the cloudflare page..
        page_title = product_page_soup.find('title').get_text(strip=True)
        if page_title == "Just a moment...":
            print("Cloudflare page loaded for labchem... skipping parsing product")
            return
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
            if not product_obj:
                continue

            product_obj["price"] = product_prices.get(product_obj["mpn"])

            product: ProductType = product_obj

            self._products.append(product)

    def __parse_product(self, product_elem: BeautifulSoup) -> ProductType:
        title_elem = product_elem.find("h4").find("a").get_text(strip=True)
        link = product_elem.find("div", class_="prodImage").find("a").attrs["href"]

        cas = product_elem.find("ul", class_="otherNumWrap").find("span")

        # Get the compare ID, which is necessary since its used in some element
        # identifiers
        compare_input = product_elem.find_all("input", attrs={"name": "compareId", "type": "checkbox"})

        if not compare_input:
            raise AttributeError("Unable to find a compareId")

        compare_id = compare_input[0].attrs['value']
        part_number_elem = product_elem.find("input", attrs={"id": f"partNumber_{compare_id}"})

        part_number = None

        variant_part_number = None

        id_list_price = product_elem.find('input', attrs={"name": "idListPrice"})

        if id_list_price:
            variant_part_number = id_list_price.attrs["value"]

        if part_number_elem:
            part_number = part_number_elem.attrs["value"] or None

        mpn_value_elem = product_elem.find("input", attrs={"id": re.compile(r"^MPNValue_")})

        mpn_value = None
        if mpn_value_elem:
            mpn_value = mpn_value_elem.attrs["value"] or None

        product = {
            **self.__defaults,
            "name": title_elem,
            "title": title_elem,
            "supplier": self._supplier["name"],
            "mpn": variant_part_number or part_number or mpn_value,
            "uuid": compare_id,
            "url": self._supplier["base_url"] + link,
        }

        if cas:
            product["cas"] = cas.get_text(strip=True)

        return product

    def __query_products_prices(self, part_numbers: tuple[str, list]) -> dict | None:
        """Query specific product prices by their part numeber(s)

        Args:
            part_numbers (str|list): partnumber(s) of chem(s) to query for.

        Returns:
            dict: lookup dictionary with the part number and list price values
        """

        if part_numbers is None or len(part_numbers) == 0:
            return None

        if isinstance(part_numbers, list):
            part_numbers = ",".join(part_numbers)

        params = {"productIdList": part_numbers}

        product_json = self.http_get_json(
            "getPriceDetailPage.action", params=params, headers=self._headers, cookies=self._cookies
        )

        res = dict()

        for p in product_json:
            res[p["partNumber"]] = str(p["listPrice"]).strip() if p["listPrice"] else None

        return res


__disabled__ = True
