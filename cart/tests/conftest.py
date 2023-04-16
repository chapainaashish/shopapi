import pytest
from model_bakery import baker

from cart.models import Cart


@pytest.fixture
def cart(user):
    return baker.make(Cart, user=user)
