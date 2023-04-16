import pytest
from model_bakery import baker
from rest_framework import status

from cart.models import Cart, CartItem
from product.models import Product


@pytest.fixture
def cart(user):
    return baker.make(Cart, user=user)


@pytest.fixture
def product():
    return baker.make(Product, quantity=100)


@pytest.fixture
def cart_item(cart):
    return baker.make(CartItem, cart=cart)


@pytest.fixture
def endpoint(cart):
    return f"/store/cart/{cart.id}/items/"


@pytest.fixture
def valid_data(product):
    return {"product": product.id, "quantity": 10}


@pytest.fixture
def invalid_data(product):
    return {"product": product.id, "quantity": -1}


@pytest.mark.django_db
class TestCreateCartItems:
    """Testcases  of cart item endpoint while creating cart item"""

    def test_user_is_anonymous_returns_400(
        self, send_post_request, endpoint, valid_data
    ):
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_unauthorized_returns_400(
        self, authenticate, send_post_request, endpoint, valid_data
    ):
        authenticate()
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_authenticated_and_authorized_but_data_invalid_returns_400(
        self, request_authenticate, send_post_request, endpoint, invalid_data, user
    ):
        request_authenticate(user)
        response = send_post_request(endpoint, invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_authenticated_and_authorized_and_data_valid_returns_201(
        self, request_authenticate, send_post_request, endpoint, valid_data, user
    ):
        request_authenticate(user)
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveReview:
    """Testcases  of cart item endpoint while retrieving cart item"""

    def test_user_is_anonymous_returns_404(self, api_client, endpoint, cart_item):
        response = api_client.get(f"{endpoint}{cart_item.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_unauthorized_returns_404(
        self, authenticate, api_client, endpoint, cart_item
    ):
        authenticate()
        response = api_client.get(f"{endpoint}{cart_item.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_is_authenticated_and_authorized_but_cart_item_not_exists_returns_404(
        self, request_authenticate, api_client, endpoint, cart_item, user
    ):
        request_authenticate(user)
        response = api_client.get(f"{endpoint}{cart_item.id+1}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_is_authenticated_and_authorized_and_cart_item_exists_returns_200(
        self, request_authenticate, api_client, endpoint, cart_item, user
    ):
        request_authenticate(user)
        response = api_client.get(f"{endpoint}{cart_item.id}/")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPatchCartItem:
    """Testcases of cart item endpoint while patching cart item"""

    def test_user_is_anonymous_returns_401(
        self,
        send_patch_request,
        endpoint,
        valid_data,
        cart_item,
    ):
        response = send_patch_request(f"{endpoint}{cart_item.id}/", valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_unauthorized_returns_404(
        self,
        authenticate,
        send_patch_request,
        endpoint,
        valid_data,
        cart_item,
    ):
        authenticate()
        response = send_patch_request(f"{endpoint}{cart_item.id}/", valid_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_is_authenticated_and_authorized_and_data_invalid_returns_400(
        self,
        request_authenticate,
        send_patch_request,
        endpoint,
        invalid_data,
        user,
        cart_item,
    ):
        request_authenticate(user)
        response = send_patch_request(f"{endpoint}{cart_item.id}/", invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_authenticated_and_authorized_and_data_valid_returns_200(
        self,
        request_authenticate,
        send_patch_request,
        endpoint,
        valid_data,
        user,
        cart_item,
    ):
        request_authenticate(user)
        response = send_patch_request(f"{endpoint}{cart_item.id}/", valid_data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteCartItem:
    """Testcases of cart item endpoint while deleting cart item"""

    def test_user_is_anonymous_returns_401(
        self,
        send_delete_request,
        endpoint,
        cart_item,
    ):
        response = send_delete_request(f"{endpoint}{cart_item.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_unauthorized_returns_404(
        self,
        authenticate,
        send_delete_request,
        endpoint,
        cart_item,
    ):
        authenticate()
        response = send_delete_request(f"{endpoint}{cart_item.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_is_authenticated_and_authorized(
        self,
        request_authenticate,
        send_delete_request,
        endpoint,
        user,
        cart_item,
    ):
        request_authenticate(user)
        response = send_delete_request(f"{endpoint}{cart_item.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
