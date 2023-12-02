from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from training.models import Course, Subscription
from users.models import User


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@user.com', is_active=True, password='123')
        self.client.force_authenticate(user=self.user)
        self.user.set_password('123')
        self.user.save()

        self.course = Course.objects.create(title='TestCourse', description='TestCourse', owner=self.user)

        self.subscription = Subscription.objects.create(is_active=True, course=self.course, user=self.user)

    def test_create_subscription(self):
        """  Test subscription creating """

        self.course = Course.objects.create(
            title='TestCourse',
            description='TestCourse',
            owner=self.user
        )

        data = {
            'is_active': True,
            'course': self.course.id,
            'user': self.user.id,
        }

        response = self.client.post(reverse('collection:sub_create'), data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {
                'id': response.json()['id'],
                'is_active': True,
                'course': self.course.id,
                'user': self.user.id,
            }
        )

    def test_delete_subscription(self):
        """ Test subscription deleting """

        response = self.client.delete(reverse('collection:sub_delete', kwargs={'pk': self.subscription.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.all().exists())