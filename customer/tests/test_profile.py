import pytest
from model_bakery import baker
from rest_framework import status

from customer.models import Profile


@pytest.fixture
def endpoint():
    return "/user/profile/"


@pytest.fixture
def profile(user):
    return baker.make(Profile, user=user, phone="+12125552368")


@pytest.fixture
def valid_data(user):
    return {"phone": "+12125552368", "user": user.id}


@pytest.fixture
def invalid_data(user):
    return {"phone": "d9898s", "user": user.id}


@pytest.mark.django_db
class TestCreateProfile:
    """Testcases  of profile endpoint while creating profile"""

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

    def test_user_is_authenticated_and_profile_already_exists_returns_400(
        self, request_authenticate, send_post_request, endpoint, valid_data, user
    ):
        request_authenticate(user)
        first_response = send_post_request(endpoint, valid_data)
        second_response = send_post_request(endpoint, valid_data)
        assert first_response.status_code == status.HTTP_201_CREATED
        assert second_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_authenticated_and_data_valid_returns_201(
        self, request_authenticate, send_post_request, endpoint, valid_data, user
    ):
        request_authenticate(user)
        response = send_post_request(endpoint, valid_data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestPatchProfile:
    """Testcases  of profile endpoint while updating [patch] profile"""

    def test_user_is_anonymous_returns_401(
        self, send_patch_request, endpoint, valid_data, profile
    ):
        response = send_patch_request(f"{endpoint}{profile.id}/", valid_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_is_authenticated_but_invalid_data_returns_400(
        self,
        request_authenticate,
        send_patch_request,
        endpoint,
        invalid_data,
        user,
        profile,
    ):
        request_authenticate(user)
        response = send_patch_request(f"{endpoint}{profile.id}/", invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_is_authenticated_and_valid_data_returns_200(
        self,
        request_authenticate,
        send_patch_request,
        endpoint,
        valid_data,
        user,
        profile,
    ):
        request_authenticate(user)
        response = send_patch_request(f"{endpoint}{profile.id}/", valid_data)
        assert response.status_code == status.HTTP_200_OK
