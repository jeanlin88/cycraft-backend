from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import AppUser


class TestUserSetup(TestCase):
    def setUp(self) -> None:
        # users
        self.manager1 = AppUser(
            username="manager1",
            email="manager1@gmail.com",
            is_business=True,
        )
        self.manager1.save()
        self.manager2 = AppUser(
            username="manager2",
            email="manager2@gmail.com",
            is_business=True,
        )
        self.manager2.save()
        self.reviewer1 = AppUser(
            username="reviewer1",
            email="reviewer1@gmail.com",
            is_business=False,
        )
        self.reviewer1.save()
        self.reviewer2 = AppUser(
            username="reviewer2",
            email="reviewer2@gmail.com",
            is_business=False,
        )
        self.reviewer2.save()
        # clients
        self.anonymous_client = APIClient()
        self.manager1_client = APIClient()
        self.manager2_client = APIClient()
        self.reviewer1_client = APIClient()
        self.reviewer2_client = APIClient()
        manager1_refresh_token = RefreshToken.for_user(self.manager1)
        manager2_refresh_token = RefreshToken.for_user(self.manager2)
        reviewer1_refresh_token = RefreshToken.for_user(self.reviewer1)
        reviewer2_refresh_token = RefreshToken.for_user(self.reviewer2)
        self.manager1_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(manager1_refresh_token.access_token)}',
        )
        self.manager2_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(manager2_refresh_token.access_token)}',
        )
        self.reviewer1_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(reviewer1_refresh_token.access_token)}',
        )
        self.reviewer2_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(reviewer2_refresh_token.access_token)}',
        )
        pass
