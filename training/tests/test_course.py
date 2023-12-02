from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from training.models import Lesson, Course, Subscription
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@user.com', is_active=True, password='123')
        self.client.force_authenticate(user=self.user)
        self.user.set_password('123')
        self.user.save()

        self.course = Course.objects.create(title='TestCourse', description='TestCourse', owner=self.user)

        self.lesson = Lesson.objects.create(title='TestLesson', course=self.course)

        self.subscription = Subscription.objects.create(is_active=True, course=self.course, user=self.user)

    def test_create_course(self):
        """  Test course creating """

        data = {
            "title": "TestCourse1",
            "description": "TestCourse1",
            "owner": self.user.id

        }

        response = self.client.post('/courses/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(),
            {
                'id': response.json()['id'],
                'title': 'TestCourse1',
                'preview': None,
                'description': 'TestCourse1',
                'owner': self.user.id
            }
        )

    def test_list_course(self):
        """  Test for getting list of course """

        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.course.id,
                        "lesson_count": 1,
                        "lessons": [
                            {
                                "id": self.lesson.id,
                                "title": "TestLesson",
                                "description": None,
                                "preview": None,
                                "video": None,
                                "course": self.course.id,
                                "owner": None
                            },
                        ],
                        "is_subscribed": True,
                        "title": "TestCourse",
                        "preview": None,
                        "description": 'TestCourse',
                        "owner": self.user.id
                    }
                ]
            }
        )

    def test_retrieve_course(self):
        """  Test for getting course """

        response = self.client.get(f'/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),

            {
                "id": self.course.id,
                "lesson_count": 1,
                "lessons": [
                    {
                        "id": self.lesson.id,
                        "title": "TestLesson",
                        "description": None,
                        "preview": None,
                        "video": None,
                        "course": self.course.id,
                        "owner": None
                    },
                ],
                "is_subscribed": True,
                "title": "TestCourse",
                "preview": None,
                "description": 'TestCourse',
                "owner": self.user.id
            }

        )

    def test_update_course(self):
        """ Test course updating """

        data = {
            "title": "NewCourse",
            "description": "NewCourse",
            "owner": self.user.id

        }

        response = self.client.put(f'/courses/{self.course.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": self.course.id,
                "lesson_count": 1,
                "lessons": [
                    {
                        "id": self.lesson.id,
                        "title": "TestLesson",
                        "description": None,
                        "preview": None,
                        "video": None,
                        "course": self.course.id,
                        "owner": None
                    },
                ],
                "is_subscribed": True,
                "title": "NewCourse",
                "preview": None,
                "description": 'NewCourse',
                "owner": self.user.id
            }
        )

    def test_delete_course(self):
        """ Test course deleting """

        response = self.client.delete(f'/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.all().exists())

    def tearDown(self):
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()