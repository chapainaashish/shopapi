import pytest
from model_bakery import baker
from rest_framework import status

from product.models import Category


@pytest.fixture
def endpoint():
    return "/store/category/"


@pytest.fixture
def category():
    return baker.make(Category)


@pytest.fixture
def valid_data():
    return {"name": "a", "description": "adf"}


@pytest.fixture
def invalid_data():
    return {"name": "a" * 256, "description": "a" * 256}


@pytest.mark.django_db
class TestCreateCategory:
    """Testcases of category endpoint while creating category"""

    def test_user_is_anonymous_returns_401(
        self, send_post_request, endpoint, valid_data
    ):
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_not_admin_returns_401(
        self, authenticate, send_post_request, endpoint, valid_data
    ):
        authenticate()
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_admin_but_data_invalid_returns_400(
        self, authenticate, send_post_request, endpoint, invalid_data
    ):
        authenticate(is_staff=True)
        response = send_post_request(endpoint, invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_admin_and_data_valid_returns_201(
        self, authenticate, send_post_request, endpoint, valid_data
    ):
        authenticate(is_staff=True)
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveCategory:
    """Testcases of category endpoint while retrieving category"""

    def test_category_exists_returns_200(self, api_client, endpoint, category):
        response = api_client.get(f"{endpoint}{category.id}/")
        assert response.status_code == status.HTTP_200_OK

    def test_category_not_exists_returns_404(self, api_client, endpoint, category):
        response = api_client.get(f"{endpoint}{category.id + 1}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPatchCategory:
    """Testcases of category endpoint while patching category"""

    def test_user_is_anonymous_returns_401(
        self, send_patch_request, endpoint, category, valid_data
    ):
        response = send_patch_request(f"{endpoint}{category.id}/", valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_not_admin_returns_401(
        self, authenticate, send_patch_request, endpoint, category, valid_data
    ):
        authenticate()
        response = send_patch_request(f"{endpoint}{category.id}/", valid_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_admin_but_data_invalid_returns_400(
        self,
        authenticate,
        send_patch_request,
        endpoint,
        category,
        invalid_data,
    ):
        authenticate(is_staff=True)
        response = send_patch_request(f"{endpoint}{category.id}/", invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_admin_and_data_valid_returns_201(
        self, authenticate, send_patch_request, endpoint, category, valid_data
    ):
        authenticate(is_staff=True)
        response = send_patch_request(f"{endpoint}{category.id}/", valid_data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteCategory:
    """Testcases of category endpoint while deleting category"""

    def test_user_is_anonymous_returns_401(
        self, send_delete_request, endpoint, category
    ):
        response = send_delete_request(f"{endpoint}{category.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_not_admin_returns_401(
        self, authenticate, send_delete_request, endpoint, category
    ):
        authenticate()
        response = send_delete_request(f"{endpoint}{category.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_admin_returns_204(
        self, authenticate, send_delete_request, endpoint, category
    ):
        authenticate(is_staff=True)
        response = send_delete_request(f"{endpoint}{category.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
