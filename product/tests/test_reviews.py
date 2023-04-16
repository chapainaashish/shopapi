import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status

from product.models import Product, Review


@pytest.fixture
def user():
    return baker.make(User)


# we are using same user for authentication and for performing operation in review
@pytest.fixture
def request_authenticate(api_client):
    """For authentication and for request"""

    def inner_request_authenticate(user):
        return api_client.force_authenticate(user=user)

    return inner_request_authenticate


@pytest.fixture
def product():
    return baker.make(Product)


@pytest.fixture
def review(product, user):
    return baker.make(Review, product=product, user=user)


@pytest.fixture
def endpoint(product):
    return f"/store/product/{product.id}/reviews/"


@pytest.fixture
def valid_data(product, user):
    return {"product": product.id, "user": user.id, "description": "asdf", "rating": 3}


@pytest.fixture
def invalid_data(product, user):
    return {"product": product.id, "user": user.id, "description": "asdf", "rating": 8}


@pytest.mark.django_db
class TestCreateReview:
    """Testcases  of review endpoint while creating review"""

    def test_user_is_anonymous_returns_401(
        self, send_post_request, endpoint, valid_data
    ):
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_data_invalid_returns_401(
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

    def test_user_review_already_exists_returns_400(
        self, request_authenticate, send_post_request, endpoint, valid_data, user
    ):
        request_authenticate(user)
        first_response = send_post_request(endpoint, valid_data)
        second_response = send_post_request(endpoint, valid_data)

        assert second_response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveReview:
    """Testcases  of product endpoint while retrieving  product"""

    def test_review_exists_returns_200(self, api_client, endpoint, review):
        response = api_client.get(f"{endpoint}{review.id}/")
        assert response.status_code == status.HTTP_200_OK

    def test_review_not_exists_returns_404(self, api_client, endpoint, review):
        response = api_client.get(f"{endpoint}{review.id + 1}/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestPatchProduct:
    """Testcases  of review endpoint while patching review"""

    def test_user_is_anonymous_returns_401(
        self, send_patch_request, endpoint, review, valid_data
    ):
        response = send_patch_request(f"{endpoint}{review.id}/", valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_not_authorized_returns_403(
        self, authenticate, send_patch_request, endpoint, review, valid_data
    ):
        authenticate()
        response = send_patch_request(f"{endpoint}{review.id}/", valid_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_authorized_but_data_invalid_returns_400(
        self,
        request_authenticate,
        send_patch_request,
        endpoint,
        review,
        invalid_data,
        user,
    ):
        request_authenticate(user)
        response = send_patch_request(f"{endpoint}{review.id}/", invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_authorized_and_data_valid_returns_200(
        self,
        request_authenticate,
        send_patch_request,
        endpoint,
        review,
        valid_data,
        user,
    ):
        request_authenticate(user)
        response = send_patch_request(f"{endpoint}{review.id}/", valid_data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteProduct:
    """Testcases of review endpoint while deleting review"""

    def test_user_is_anonymous_returns_401(self, send_delete_request, endpoint, review):
        response = send_delete_request(f"{endpoint}{review.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_not_authorized_403(
        self, authenticate, send_delete_request, endpoint, review
    ):
        authenticate()
        response = send_delete_request(f"{endpoint}{review.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_is_authenticated_and_authorized_returns_201(
        self,
        request_authenticate,
        send_delete_request,
        endpoint,
        review,
        user,
    ):
        request_authenticate(user)
        response = send_delete_request(f"{endpoint}{review.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
