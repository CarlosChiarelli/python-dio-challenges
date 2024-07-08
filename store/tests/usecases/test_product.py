from typing import List
from uuid import UUID

import pytest

# from store.core.exceptions import NotFoundException
# from store.schemas.product import ProductOut
# from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import product_usecase


async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    # assert isinstance(result, ProductOut)
    assert result is None
