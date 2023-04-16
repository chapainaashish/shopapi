import pytest
from model_bakery import baker

from product.models import Category, Product


@pytest.fixture
def product():
    return baker.make(Product)


@pytest.fixture
def category():
    return baker.make(Category)
