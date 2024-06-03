from restaurants.tests import TestRestaurantSetup

from .models import Review


class TestReviewSetup(TestRestaurantSetup):
    def setUp(self) -> None:
        super().setUp()
        self.review1 = Review(
            restaurant=self.restaurant1,
            score=5,
            comment="美味快速",
            created_by=self.reviewer1,
        )
        self.review1.save()
        self.review1_dict = {
            'id': str(self.review1.id),
            'restaurant': self.review1.restaurant.id,
            'score': self.review1.score,
            'comment': self.review1.comment,
            'created_by': self.review1.created_by.id,
            'created_at': self.review1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': self.review1.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.user1_reviews = [self.review1_dict]
        self.review2 = Review(
            restaurant=self.restaurant1,
            score=4,
            comment="備餐稍慢",
            created_by=self.reviewer2,
        )
        self.review2.save()
        self.review2_dict = {
            'id': str(self.review2.id),
            'restaurant': self.review2.restaurant.id,
            'score': self.review2.score,
            'comment': self.review2.comment,
            'created_by': self.review2.created_by.id,
            'created_at': self.review2.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': self.review2.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.restaurant1_dict |= {
            'rating': sum([self.review1.score, self.review2.score])/2,
            'total_reviews': 2,
        }
        self.restaurant1_reviews = [self.review1_dict, self.review2_dict]
        self.review3 = Review(
            restaurant=self.restaurant2,
            score=2,
            comment="衛生不好",
            created_by=self.reviewer2,
        )
        self.review3.save()
        self.review3_dict = {
            'id': str(self.review3.id),
            'restaurant': self.review3.restaurant.id,
            'score': self.review3.score,
            'comment': self.review3.comment,
            'created_by': self.review3.created_by.id,
            'created_at': self.review3.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': self.review3.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.restaurant2_dict |= {
            'rating': self.review3.score,
            'total_reviews': 1,
        }
        self.restaurant2_reviews = [self.review3_dict]
        self.user2_reviews = [self.review2_dict, self.review3_dict]
