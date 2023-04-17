import pytest
from rest_framework import status


@pytest.fixture
def endpoint():
    return "/store/product/"


@pytest.fixture
def valid_data(category):
    return {
        "name": "asdf",
        "description": "asdf",
        "quantity": 1,
        "price": 10,
        "category": category.id,
    }


@pytest.fixture
def invalid_data():
    return {
        "name": "a" * 256,
        "description": "a" * 256,
        "quantity": 89,
        "price": 10,
    }


@pytest.mark.django_db
class TestCreateProduct:
    """Testcases  of product endpoint while creating product"""

    def test_user_is_anonymous_returns_401(
        self, send_post_request, endpoint, valid_data
    ):
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_not_admin_returns_403(
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
        assert response.data["id"] > 0


@pytest.mark.django_db
class TestRetrieveProduct:
    """Testcases  of product endpoint while retrieving  product"""

    def test_category_exists_returns_200(self, api_client, endpoint, product):
        response = api_client.get(f"{endpoint}{product.id}/")
        assert response.status_code == status.HTTP_200_OK

    def test_category_not_exists_returns_404(self, api_client, endpoint, product):
        response = api_client.get(f"{endpoint}{product.id + 1}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPatchProduct:
    """Testcases  of product endpoint while patching product"""

    def test_user_is_anonymous_returns_401(
        self, send_patch_request, endpoint, product, valid_data
    ):
        response = send_patch_request(f"{endpoint}{product.id}/", valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_not_admin_returns_403(
        self, authenticate, send_patch_request, endpoint, product, valid_data
    ):
        authenticate()
        response = send_patch_request(f"{endpoint}{product.id}/", valid_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_admin_but_data_invalid_returns_400(
        self,
        authenticate,
        send_patch_request,
        endpoint,
        product,
        invalid_data,
    ):
        authenticate(is_staff=True)
        response = send_patch_request(f"{endpoint}{product.id}/", invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_admin_and_data_valid_returns_200(
        self, authenticate, send_patch_request, endpoint, product, valid_data
    ):
        authenticate(is_staff=True)
        response = send_patch_request(f"{endpoint}{product.id}/", valid_data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestPutProduct:
    """Testcases  of product endpoint while updating(PUT) product"""

    def test_user_is_anonymous_returns_401(
        self, send_put_request, endpoint, product, valid_data
    ):
        response = send_put_request(f"{endpoint}{product.id}/", valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_not_admin_returns_403(
        self, authenticate, send_put_request, endpoint, product, valid_data
    ):
        authenticate()
        response = send_put_request(f"{endpoint}{product.id}/", valid_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_admin_but_data_invalid_returns_400(
        self,
        authenticate,
        send_put_request,
        endpoint,
        product,
        invalid_data,
    ):
        authenticate(is_staff=True)
        response = send_put_request(f"{endpoint}{product.id}/", invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_admin_and_data_valid_returns_200(
        self, authenticate, send_put_request, endpoint, product, valid_data
    ):
        authenticate(is_staff=True)
        response = send_put_request(f"{endpoint}{product.id}/", valid_data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteProduct:
    """Testcases of product endpoint while deleting product"""

    def test_user_is_anonymous_returns_401(
        self, send_delete_request, endpoint, product
    ):
        response = send_delete_request(f"{endpoint}{product.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_not_admin_returns_403(
        self, authenticate, send_delete_request, endpoint, product
    ):
        authenticate()
        response = send_delete_request(f"{endpoint}{product.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_admin_returns_204(
        self, authenticate, send_delete_request, endpoint, product
    ):
        authenticate(is_staff=True)
        response = send_delete_request(f"{endpoint}{product.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
