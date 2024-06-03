from rest_framework import status
from rest_framework.response import Response
from reviews.tests import TestReviewSetup


class TestReviewAPIs(TestReviewSetup):

    def test_get_restaurant_all_reviews(self):
        response: Response = self.manager1_client.get(
            f'/api/reviews/?restaurant={self.restaurant1.id}',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [self.review1_dict, self.review2_dict],
        }
        self.assertDictEqual(response.data, expected_data)

    def test_get_user_all_reviews(self):
        response: Response = self.manager1_client.get(
            f'/api/reviews/?created_by={self.reviewer2.id}',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [self.review2_dict, self.review3_dict],
        }
        self.assertDictEqual(response.data, expected_data)

    def test_get_all_reviews(self):
        response: Response = self.manager1_client.get('/api/reviews/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review(self):
        new_review = {
            'restaurant': self.restaurant2.id,
            'score': 5,
            'comment': '便宜又好吃',
        }
        response: Response = self.reviewer1_client.post(
            '/api/reviews/',
            data=new_review,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in new_review:
            self.assertEqual(new_review[key], response.data[key])
        self.assertEqual(self.reviewer1.id, response.data['created_by'])
        pass

    def test_create_review_invalid_score(self):
        new_review = {
            'restaurant': self.restaurant2.id,
            'score': 6,
            'comment': '便宜又好吃',
        }
        response: Response = self.reviewer1_client.post(
            '/api/reviews/',
            data=new_review,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        new_review = {
            'restaurant': self.restaurant2.id,
            'score': 0,
            'comment': '便宜又好吃',
        }
        response: Response = self.reviewer1_client.post(
            '/api/reviews/',
            data=new_review,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        new_review = {
            'restaurant': self.restaurant2.id,
            'score': 3.3,
            'comment': '便宜又好吃',
        }
        response: Response = self.reviewer1_client.post(
            '/api/reviews/',
            data=new_review,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        pass

    def test_create_duplicate_review(self):
        new_review = {
            'restaurant': self.restaurant1.id,
            'score': 5,
            'comment': '再訪還是好吃',
        }
        response: Response = self.reviewer1_client.post(
            '/api/reviews/',
            data=new_review,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        pass

    def test_manager_create_review(self):
        new_review = {
            'restaurant': self.restaurant1.id,
            'score': 5,
            'comment': '第一次吃',
        }
        response: Response = self.manager1_client.post(
            '/api/reviews/',
            data=new_review,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        pass

    def test_update_review(self):
        updated_review = {
            'score': 4,
            'comment': '備餐速度有改善',
        }
        response: Response = self.reviewer2_client.patch(
            f'/api/reviews/{self.review2.id}/',
            data=updated_review,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['score'],
            updated_review['score'],
        )
        self.assertEqual(
            response.data['comment'],
            updated_review['comment'],
        )
        self.assertNotEqual(
            response.data['created_at'],
            response.data['updated_at'],
        )
        # restaurant rating & total_reviews
        response: Response = self.manager1_client.get('/api/restaurants/')
        restaurant1 = None
        for result in response.data['results']:
            if result['id'] == str(self.restaurant1.id):
                restaurant1 = result
                break
        self.assertIsNotNone(restaurant1)
        self.assertEqual(
            restaurant1['rating'],
            sum([self.review1.score, updated_review['score']])/2,
        )
        self.assertEqual(restaurant1['total_reviews'], 2)

    def test_update_review_invalid_score(self):
        updated_review = {
            'score': 6,
            'comment': '備餐速度有改善',
        }
        response: Response = self.reviewer2_client.patch(
            f'/api/reviews/{self.review2.id}/',
            data=updated_review,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        updated_review = {
            'score': 0,
            'comment': '備餐速度有改善',
        }
        response: Response = self.reviewer2_client.patch(
            f'/api/reviews/{self.review2.id}/',
            data=updated_review,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        updated_review = {
            'score': 3.3,
            'comment': '備餐速度有改善',
        }
        response: Response = self.reviewer2_client.patch(
            f'/api/reviews/{self.review2.id}/',
            data=updated_review,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_review_restaurant(self):
        updated_review = {
            'restaurant': self.restaurant2.id,
            'comment': 'should not update review restaurant'
        }
        response: Response = self.reviewer1_client.patch(
            f'/api/reviews/{self.review1.id}/',
            data=updated_review,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_review_not_owner(self):
        updated_review = {
            'score': 4,
            'comment': '備餐速度有改善',
        }
        response: Response = self.reviewer1_client.patch(
            f'/api/reviews/{self.review2.id}/',
            data=updated_review,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review(self):
        response: Response = self.reviewer2_client.delete(
            f'/api/reviews/{self.review2.id}/',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # restaurant rating & total_reviews
        response: Response = self.manager1_client.get('/api/restaurants/')
        restaurant1 = None
        for result in response.data['results']:
            if result['id'] == str(self.restaurant1.id):
                restaurant1 = result
                break
        self.assertIsNotNone(restaurant1)
        self.assertEqual(restaurant1['rating'], self.review1.score)
        self.assertEqual(restaurant1['total_reviews'], 1)

    def test_delete_review_not_owner(self):
        response: Response = self.reviewer1_client.delete(
            f'/api/reviews/{self.review2.id}/',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authenticated(self):
        # get restaurant all reviews
        response: Response = self.anonymous_client.get(
            f'/api/reviews/?restaurant={self.restaurant1.id}',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # get user all reviews
        response: Response = self.anonymous_client.get(
            f'/api/reviews/?created_by={self.reviewer2.id}',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # get all reviews
        response: Response = self.anonymous_client.get(
            f'/api/reviews/',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # create review
        new_review = {
            'restaurant': self.restaurant2.id,
            'score': 5,
            'comment': '便宜又好吃',
        }
        response: Response = self.anonymous_client.post(
            '/api/reviews/',
            data=new_review,
        )
        # update review
        updated_review = {
            'score': 4,
            'comment': '備餐速度有改善',
        }
        response: Response = self.anonymous_client.patch(
            f'/api/reviews/{self.review2.id}/',
            data=updated_review,
        )
        # delete review
        response: Response = self.anonymous_client.delete(
            f'/api/reviews/{self.review2.id}/',
        )
