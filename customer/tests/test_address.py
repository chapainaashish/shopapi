import pytest
from model_bakery import baker
from rest_framework import status

from customer.models import Address


@pytest.fixture
def endpoint():
    return "/user/address/"


@pytest.fixture
def address(user):
    return baker.make(Address, user=user, country="GY")


@pytest.fixture
def valid_data(user):
    return {
        "house_no": "241",
        "street": "20955 Kuhic Junctions",
        "city": "Metzborough",
        "postal_code": "47683-8856",
        "country": "GY",
        "user": user.id,
    }


@pytest.fixture
def invalid_data(user):
    return {
        "house_no": "2.3",
        "street": "20955 Kuhic Junctions",
        "city": "slkdfj",
        "postal_code": "-8856",
        "country": "jskdsfds",
        "user": user.id,
    }


@pytest.mark.django_db
class TestCreateAddress:
    """Testcases  of address endpoint while creating address"""

    def test_user_is_anonymous_returns_401(
        self, send_post_request, endpoint, valid_data
    ):
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_invalid_data_returns_400(
        self, request_authenticate, send_post_request, endpoint, invalid_data, user
    ):
        request_authenticate(user)
        response = send_post_request(endpoint, invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_authenticated_and_data_valid_returns_201(
        self, request_authenticate, send_post_request, endpoint, valid_data, user
    ):
        request_authenticate(user)
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestPatchAddress:
    """Testcases  of address endpoint while updating [patch] address"""

    def test_user_is_anonymous_returns_401(
        self, send_patch_request, endpoint, valid_data, address
    ):
        response = send_patch_request(f"{endpoint}{address.id}/", valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_invalid_data_returns_400(
        self,
        request_authenticate,
        send_patch_request,
        endpoint,
        invalid_data,
        user,
        address,
    ):
        request_authenticate(user)
        response = send_patch_request(f"{endpoint}{address.id}/", invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_authenticated_and_valid_data_returns_200(
        self,
        request_authenticate,
        send_patch_request,
        endpoint,
        valid_data,
        user,
        address,
    ):
        request_authenticate(user)
        response = send_patch_request(f"{endpoint}{address.id}/", valid_data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteAddress:
    """Testcases  of address endpoint while deleting address"""

    def test_user_is_anonymous_returns_401(
        self, send_delete_request, endpoint, address
    ):
        response = send_delete_request(f"{endpoint}{address.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_returns_204(
        self, send_delete_request, request_authenticate, endpoint, address, user
    ):
        request_authenticate(user)
        response = send_delete_request(f"{endpoint}{address.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
