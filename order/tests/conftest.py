import pytest
from model_bakery import baker

from order.models import Order


@pytest.fixture
def order(user):
    return baker.make(Order, user=user)
