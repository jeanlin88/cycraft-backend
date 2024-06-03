from users.tests import TestUserSetup

from .models import Restaurant


class TestRestaurantSetup(TestUserSetup):
    def setUp(self) -> None:
        super().setUp()
        self.restaurant1 = Restaurant(
            name="麥當勞",
            description="連鎖速食店",
            address="台北市",
            created_by=self.manager1,
        )
        self.restaurant1.save()
        self.restaurant1_dict = {
            'id': str(self.restaurant1.id),
            'name': self.restaurant1.name,
            'description': self.restaurant1.description,
            'address': self.restaurant1.address,
            'created_by': self.restaurant1.created_by.id,
            'created_at': self.restaurant1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': self.restaurant1.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.restaurant2 = Restaurant(
            name="巷口麵店",
            description="三十年老店",
            address="新北市",
            created_by=self.manager2,
        )
        self.restaurant2.save()
        self.restaurant2_dict = {
            'id': str(self.restaurant2.id),
            'name': self.restaurant2.name,
            'description': self.restaurant2.description,
            'address': self.restaurant2.address,
            'created_by': self.restaurant2.created_by.id,
            'created_at': self.restaurant2.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': self.restaurant2.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
