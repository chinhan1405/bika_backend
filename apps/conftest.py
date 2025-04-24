from rest_framework import test

import pytest
import pytest_django

from apps.users import factories as users_factories
from apps.users import models as users_models


@pytest.fixture
def api_client() -> test.APIClient:
    """Create api client."""
    return test.APIClient()


@pytest.fixture(scope="module")
def user(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> users_models.User:
    """Create default user."""
    with django_db_blocker.unblock():
        return users_factories.UserFactory()


@pytest.fixture
def user_api_client(
    api_client: test.APIClient,
    user: users_models.User,
) -> test.APIClient:
    """Create api client."""
    api_client.force_authenticate(user)
    return api_client


@pytest.fixture(scope="module")
def admin(
    django_db_blocker: pytest_django.DjangoDbBlocker,
) -> users_models.User:
    """Module-level fixture for admin."""
    with django_db_blocker.unblock():
        return users_factories.AdminUserFactory()
