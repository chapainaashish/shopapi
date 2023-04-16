import pytest
from model_bakery import baker
from rest_framework import status

from order.models import OrderItem


@pytest.fixture
def endpoint(order):
    return f"/store/order/{order.id}/items/"


@pytest.fixture
def order_item(order):
    return baker.make(OrderItem, order=order)


@pytest.mark.django_db
class TestRetrieveOrderItem:
    """Testcases  of order item endpoint while retrieving order item"""

    def test_user_is_anonymous_returns_404(self, api_client, endpoint, order_item):
        response = api_client.get(f"{endpoint}{order_item.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_unauthorized_returns_200(
        self, api_client, authenticate, endpoint, order_item
    ):
        authenticate()
        response = api_client.get(f"{endpoint}{order_item.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_is_authenticated_and_authorized_returns_200(
        self, api_client, request_authenticate, endpoint, user, order_item
    ):
        request_authenticate(user)
        response = api_client.get(f"{endpoint}{order_item.id}/")
        assert response.status_code == status.HTTP_200_OK

    def test_user_is_admin_returns_200(
        self, api_client, authenticate, endpoint, order_item
    ):
        authenticate(is_staff=True)
        response = api_client.get(f"{endpoint}{order_item.id}/")
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteOrderItem:
    """Testcases of order item endpoint while deleting order item"""

    def test_user_is_anonymous_returns_404(
        self, send_delete_request, endpoint, order_item
    ):
        response = send_delete_request(f"{endpoint}{order_item.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_not_admin_returns_404(
        self, send_delete_request, authenticate, endpoint, order_item
    ):
        authenticate()
        response = send_delete_request(f"{endpoint}{order_item.id}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_is_admin_returns_204(
        self, send_delete_request, authenticate, endpoint, order_item
    ):
        authenticate(is_staff=True)
        response = send_delete_request(f"{endpoint}{order_item.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
