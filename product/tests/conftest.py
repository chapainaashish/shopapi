import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    """For authenticating normal and admin user"""

    def inner_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))

    return inner_authenticate


@pytest.fixture
def send_post_request(api_client):
    """For sending POST request to particular endpoint with particular data"""

    def inner_send_post_request(endpoint: str, data: dict):
        return api_client.post(endpoint, data)

    return inner_send_post_request


@pytest.fixture
def send_patch_request(api_client):
    """For sending PATCH request to particular endpoint with particular data"""

    def inner_send_patch_request(endpoint: str, data: dict):
        return api_client.patch(endpoint, data)

    return inner_send_patch_request


@pytest.fixture
def send_put_request(api_client):
    """For sending PUT request to particular endpoint with particular data"""

    def inner_send_put_request(endpoint: str, data: dict):
        return api_client.put(endpoint, data)

    return inner_send_put_request


@pytest.fixture
def send_delete_request(api_client):
    """For sending DELETE request to particular endpoint with particular data"""

    def inner_send_delete_request(endpoint: str):
        return api_client.delete(endpoint)

    return inner_send_delete_request
