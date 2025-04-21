import pytest
from chempare import datatypes
from typing import Any
import functools

# partialProduct = ProductType.partial({'supplier': 'Bar', 'country_code': 'USD', 'currency': '$'})
# product = partialProduct(title='Test from partial', price=123.45, quantity=5, uom='L', url='http://website.com')
# ProductType(country_code='USD', currency='$', price='123.45', quantity='5', supplier='Bar', title='Test from partial', uom='L', url='http://website.com')


class TestProductType:
    @pytest.mark.parametrize(
        ("data"),
        [
            (
                dict(
                    country_code='USD',
                    currency='$',
                    price='123.45',
                    quantity='5',
                    supplier='Bar',
                    title='Test from partial',
                    uom='L',
                    url='http://website.com',
                ),
            )
        ],
        ids=["ProductType Init"],
    )
    def test_init(self, data):
        product = datatypes.ProductType(**data)

        assert product is not None, "ProductType returned nothing"

    @pytest.mark.parametrize(
        ("partial_attrs", "residual_attrs"),
        [
            (
                dict(country_code='USD', currency='$', supplier='Bar'),
                dict(quantity='5', uom='L', url='http://website.com', price='123.45', title='Test from partial'),
            )
        ],
        ids=["Partial with just common attributes"],
    )
    def test_partial(self, partial_attrs: dict[str, Any], residual_attrs: dict[str, Any]):
        partial_product = datatypes.ProductType.partial(**partial_attrs)

        assert (
            isinstance(partial_product, functools.partial) is True
        ), "Partial (from kwargs) did not return functools.partial instance"

        created_product = partial_product(**residual_attrs)

        assert (
            isinstance(created_product, datatypes.ProductType) is True
        ), "Partial (from kwargs) usage did not return instance of ProductType"

        partial_product = datatypes.ProductType.partial(partial_attrs)

        assert (
            isinstance(partial_product, functools.partial) is True
        ), "Partial (from dict) did not return functools.partial instance"

        created_product = partial_product(**residual_attrs)

        assert (
            isinstance(created_product, datatypes.ProductType) is True
        ), "Partial (from dict) usage did not return instance of ProductType"
