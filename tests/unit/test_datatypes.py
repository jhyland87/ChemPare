import pytest
from chempare import datatypes
from typing import Any
import functools


class TestProductType:
    @pytest.mark.parametrize(
        ("data"),
        [
            dict(
                currency_code='USD',
                currency='$',
                price=123.45,
                quantity='5',
                supplier='Bar',
                title='Test from partial',
                uom='L',
                url='http://website.com',
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
                dict(currency_code='USD', currency='$', supplier='Bar'),
                dict(quantity='5', uom='L', url='http://website.com', price=123.45, title='Test from partial'),
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

    @pytest.mark.parametrize(
        ("attrs", "missing_args"),
        [
            (dict(), ['title', 'price', 'currency', 'currency_code', 'quantity', 'uom', 'supplier', 'url']),
            (
                dict(
                    currency_code='USD',
                    currency='$',
                    quantity='5',
                    uom='L',
                    url='http://website.com',
                    price=123.45,
                    supplier='test',
                ),
                ['title'],
            ),
            (dict(currency_code='USD', currency='$', quantity='5', uom='L', title='test', price=123.45), ['supplier']),
            (
                dict(
                    currency_code='USD',
                    currency='$',
                    quantity='5',
                    uom='L',
                    title='test',
                    price=123.45,
                    supplier='test',
                ),
                ['url'],
            ),
            (
                dict(
                    currency_code='USD',
                    currency='$',
                    quantity='5',
                    uom='L',
                    title='test',
                    url='http://website.com',
                    supplier='test',
                ),
                ['price'],
            ),
            (
                dict(
                    currency_code='USD',
                    currency='$',
                    price=123.45,
                    uom='L',
                    title='test',
                    url='http://website.com',
                    supplier='test',
                ),
                ['quantity'],
            ),
        ],
        ids=[
            "Should fail with no arguments",
            "Should fail with no title",
            "Should fail with no supplier",
            "Should fail with no url",
            "Should fail with no price",
            "Should fail with no quantity",
        ],
    )
    def test_invalid_init(self, attrs: dict[str, Any], missing_args: list):
        with pytest.raises(TypeError) as error:
            datatypes.ProductType(**attrs)
        for arg in missing_args:
            assert f"'{arg}'" in str(error.value), f"Did not see '{arg}' mentioned in the error: {error.value}"
