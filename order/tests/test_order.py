import pytest
from model_bakery import baker
from rest_framework import status

from cart.models import Cart, CartItem
from customer.models import Address


@pytest.fixture
def endpoint():
    return "/store/order/"


@pytest.fixture
def cart(user):
    cart = baker.make(Cart, user=user)
    cart_item = baker.make(CartItem, cart=cart)
    return cart


@pytest.fixture
def address(user):
    return baker.make(Address, user=user)


@pytest.fixture
def valid_data(cart, address):
    return {
        "cart_id": cart.id,
        "billing_address": address.id,
        "shipping_address": address.id,
    }


@pytest.fixture
def invalid_data(cart, address):
    return {
        "cart_id": cart.id + 1,
        "billing_address": address.id,
        "shipping_address": address.id,
    }


@pytest.mark.django_db
class TestCreateOrder:
    """Testcases of order endpoint while creating order"""

    def test_user_is_anonymous_returns_401(
        self, send_post_request, endpoint, valid_data
    ):
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_and_valid_data_returns_201(
        self, send_post_request, request_authenticate, endpoint, user, valid_data
    ):
        request_authenticate(user)
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_is_authenticated_but_invalid_data_returns_201(
        self, send_post_request, request_authenticate, endpoint, user, invalid_data
    ):
        request_authenticate(user)
        response = send_post_request(endpoint, invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveOrder:
    """Testcases of order endpoint while retrieving order"""

    def test_user_is_anonymous_returns_401(self, api_client, order, endpoint):
        response = api_client.get(f"{endpoint}{order.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_unauthorized_returns_404(
        self, authenticate, api_client, order, endpoint
    ):
        authenticate()
        response = api_client.get(f"{endpoint}{order.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_is_authenticated_and_authorized_returns_200(
        self, request_authenticate, api_client, order, user, endpoint
    ):
        request_authenticate(user)
        response = api_client.get(f"{endpoint}{order.id}/")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPatchOrder:
    """Testcases of order endpoint while updating [patch] order"""

    def test_user_is_anonymous_returns_401(self, order, endpoint, send_patch_request):
        response = send_patch_request(f"{endpoint}{order.id}/", {"delivery": "C"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_not_admin_returns_403(
        self, authenticate, order, endpoint, send_patch_request
    ):
        authenticate()
        response = send_patch_request(f"{endpoint}{order.id}/", {"delivery": "C"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_admin_and_valid_data_returns_200(
        self, authenticate, order, endpoint, send_patch_request
    ):
        authenticate(is_staff=True)
        response = send_patch_request(f"{endpoint}{order.id}/", {"delivery": "C"})
        assert response.status_code == status.HTTP_200_OK

    def test_user_is_admin_but_invalid_data_returns_400(
        self, authenticate, order, endpoint, send_patch_request
    ):
        authenticate(is_staff=True)
        response = send_patch_request(f"{endpoint}{order.id}/", {"delivery": "X"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDeleteOrder:
    """Testcases of order endpoint while deleting order"""

    def test_user_is_anonymous_returns_401(self, order, endpoint, send_delete_request):
        response = send_delete_request(f"{endpoint}{order.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_not_admin_returns_403(
        self, authenticate, order, user, endpoint, send_delete_request
    ):
        authenticate()
        response = send_delete_request(f"{endpoint}{order.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_admin_returns_204(
        self, authenticate, order, endpoint, send_delete_request
    ):
        authenticate(is_staff=True)
        response = send_delete_request(f"{endpoint}{order.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
