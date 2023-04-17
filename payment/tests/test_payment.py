import pytest
from model_bakery import baker
from rest_framework import status

from order.models import Order
from payment.models import Payment


@pytest.fixture
def endpoint():
    return "/store/payment/"


@pytest.fixture
def order(user):
    return baker.make(Order, user=user)


@pytest.fixture
def payment(order):
    return baker.make(Payment, order=order)


@pytest.fixture
def valid_data(order):
    return {"status": "C", "order": order.id}


@pytest.fixture
def invalid_data(order):
    return {"status": "Xb", "order": order.id}


@pytest.mark.django_db
class TestRetrievePayment:
    """Testcases  of payment endpoint while retrieving payment"""

    def test_user_is_anonymous_returns_401(self, api_client, endpoint):
        response = api_client.get(endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_returns_200(
        self, authenticate, endpoint, api_client
    ):
        authenticate()
        response = api_client.get(endpoint)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPatchPayment:
    """Testcases  of payment endpoint while updating [patch] payment"""

    def test_user_is_anonymous_returns_401(
        self, send_patch_request, endpoint, valid_data, payment
    ):
        response = send_patch_request(f"{endpoint}{payment.pk}/", valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_not_admin_returns_403(
        self,
        authenticate,
        send_patch_request,
        endpoint,
        valid_data,
        payment,
    ):
        authenticate()
        response = send_patch_request(f"{endpoint}{payment.pk}/", valid_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_authenticated_and_admin_returns_200(
        self,
        authenticate,
        send_patch_request,
        endpoint,
        valid_data,
        payment,
    ):
        authenticate(is_staff=True)
        response = send_patch_request(f"{endpoint}{payment.pk}/", valid_data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeletePayment:
    """Testcases  of payment endpoint while deleting payment"""

    def test_user_is_anonymous_returns_401(
        self, send_delete_request, endpoint, payment
    ):
        response = send_delete_request(f"{endpoint}{payment.pk}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_not_admin_returns_403(
        self,
        authenticate,
        send_delete_request,
        endpoint,
        payment,
    ):
        authenticate()
        response = send_delete_request(f"{endpoint}{payment.pk}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_authenticated_and_admin_returns_200(
        self,
        authenticate,
        send_delete_request,
        endpoint,
        payment,
    ):
        authenticate(is_staff=True)
        response = send_delete_request(f"{endpoint}{payment.pk}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
