import pytest
from model_bakery import baker
from rest_framework import status

from cart.models import Cart


@pytest.fixture
def endpoint():
    return "/store/cart/"


@pytest.fixture
def cart(user):
    return baker.make(Cart, user=user)


@pytest.mark.django_db
class TestCreateCart:
    """Testcases  of cart endpoint while creating cart"""

    def test_user_is_anonymous_returns_401(self, send_post_request, endpoint):
        response = send_post_request(endpoint, {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_and_cart_not_exists_returns_201(
        self, send_post_request, request_authenticate, endpoint, user
    ):
        request_authenticate(user)
        response = send_post_request(endpoint, {})
        assert response.status_code == status.HTTP_201_CREATED

    def test_user_cart_already_exists_returns_403(
        self, send_post_request, request_authenticate, endpoint, user
    ):
        request_authenticate(user)
        first_response = send_post_request(endpoint, {})
        second_response = send_post_request(endpoint, {})
        assert second_response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveCart:
    """Testcases of cart endpoint while retrieving cart"""

    def test_user_is_anonymous_returns_401(self, api_client, cart, endpoint):
        response = api_client.get(f"{endpoint}{cart.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_unauthorized_returns_404(
        self, authenticate, api_client, cart, user, endpoint
    ):
        authenticate(user)
        response = api_client.get(f"{endpoint}{cart.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_is_authenticated_and_authorized_returns_200(
        self, request_authenticate, api_client, cart, user, endpoint
    ):
        request_authenticate(user)
        response = api_client.get(f"{endpoint}{cart.id}/")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteCart:
    """Testcases of cart endpoint while deleting cart"""

    def test_user_is_anonymous_returns_401(self, cart, endpoint, send_delete_request):
        response = send_delete_request(f"{endpoint}{cart.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_unauthorized_returns_404(
        self, authenticate, cart, user, endpoint, send_delete_request
    ):
        authenticate(user)
        response = send_delete_request(f"{endpoint}{cart.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_is_authenticated_and_authorized_returns_200(
        self, request_authenticate, cart, user, endpoint, send_delete_request
    ):
        request_authenticate(user)
        response = send_delete_request(f"{endpoint}{cart.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
