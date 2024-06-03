from rest_framework import status
from rest_framework.response import Response
from reviews.tests import TestReviewSetup


class TestRestaurantAPIs(TestReviewSetup):

    def test_get_all_restaurants(self):
        response: Response = self.manager1_client.get('/api/restaurants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                self.restaurant1_dict,
                self.restaurant2_dict,
            ],
        }
        self.assertDictEqual(response.data, expected_data)

    def test_order_restaurants_by_rating_descending(self):
        response: Response = self.manager1_client.get(
            '/api/restaurants/?ordering=rating',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                self.restaurant2_dict,
                self.restaurant1_dict,
            ],
        }
        self.assertDictEqual(response.data, expected_data)

    def test_create_restaurant(self):
        new_restaurant = {
            'name': 'test restaurant',
            'description': 'testing',
            'address': 'Taiwan',
        }
        response: Response = self.manager1_client.post(
            '/api/restaurants/',
            data=new_restaurant,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in new_restaurant:
            self.assertEqual(new_restaurant[key], response.data[key])
        self.assertEqual(self.manager1.id, response.data['created_by'])
        # default value of rating should be null
        self.assertIsNone(response.data['rating'])
        self.assertEqual(response.data['total_reviews'], 0)

    def test_reviewer_create_restaurant(self):
        new_restaurant = {
            'name': 'test restaurant',
            'description': 'testing',
            'address': 'Taiwan',
        }
        response: Response = self.reviewer1_client.post(
            '/api/restaurants/',
            data=new_restaurant,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_restaurant(self):
        updated_restaurant = {
            'description': 'test updating',
        }
        response: Response = self.manager1_client.patch(
            f'/api/restaurants/{self.restaurant1.id}/',
            data=updated_restaurant,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['description'],
            updated_restaurant['description'],
        )
        self.assertNotEqual(
            response.data['created_at'],
            response.data['updated_at'],
        )

    def test_update_restaurant_not_owner(self):
        updated_restaurant = {
            'description': 'test updating',
        }
        response: Response = self.manager2_client.patch(
            f'/api/restaurants/{self.restaurant1.id}/',
            data=updated_restaurant,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_restaurant(self):
        response: Response = self.manager1_client.delete(
            f'/api/restaurants/{self.restaurant1.id}/',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_restaurant_not_owner(self):
        response: Response = self.manager2_client.delete(
            f'/api/restaurants/{self.restaurant1.id}/',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated(self):
        # get restaurants
        response: Response = self.anonymous_client.get('/api/restaurants/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # create restaurant
        new_restaurant = {
            'name': 'test restaurant',
            'description': 'testing',
            'address': 'Taiwan',
        }
        response: Response = self.anonymous_client.post(
            '/api/restaurants/',
            data=new_restaurant,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # update restaurant
        updated_restaurant = {
            'description': 'test updating',
        }
        response: Response = self.anonymous_client.patch(
            f'/api/restaurants/{self.restaurant1.id}/',
            data=updated_restaurant,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # delete restaurant
        response: Response = self.anonymous_client.delete(
            f'/api/restaurants/{self.restaurant1.id}/',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        pass
