from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from training.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@user.com', is_active=True, password='123')
        self.client.force_authenticate(user=self.user)
        self.user.set_password('123')
        self.user.save()

        self.course = Course.objects.create(title='TestCourse')

        self.lesson = Lesson.objects.create(title='TestLesson', course=self.course)

    def test_create_lesson(self):
        """  Test lesson creating """

        data = {
            "title": "test",
            "video": "https://www.youtube.com/",
            "course": self.course.id,
            "owner": self.user.id

        }

        response = self.client.post(reverse('collection:lesson_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(),
            {
                'id': response.json()['id'],
                'title': 'test',
                'description': None,
                'preview': None,
                'video': 'https://www.youtube.com/',
                'course': self.course.id,
                'owner': self.user.id
            }
        )

    def test_list_lesson(self):
        """  Test for getting list of lessons """

        response = self.client.get(reverse('collection:lesson_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.id,
                        "title": "TestLesson",
                        "description": None,
                        "preview": None,
                        "video": None,
                        "course": self.course.id,
                        "owner": None
                    },
                ]
            }
        )

    def test_retrieve_lesson(self):
        """  Test for getting lesson """

        url = reverse('collection:lesson_get', kwargs={'pk': self.lesson.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'title': 'TestLesson',
                'description': None,
                "preview": None,
                "video": None,
                "course": self.course.id,
                "owner": None
            }
        )

    def test_update_lesson(self):
        """ Test lesson updating """

        data = {
            'title': 'NewTestLesson',
            'description': 'NewTestLesson',
            "preview": '',
            "video": 'https://www.youtube.com',
            "course": self.course.id,
            "owner": self.user.id
        }

        response = self.client.put(reverse('collection:lesson_update', kwargs={'pk': self.lesson.id}), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.id,
                'title': 'NewTestLesson',
                'description': 'NewTestLesson',
                "preview": None,
                "video": 'https://www.youtube.com',
                "course": self.course.id,
                "owner": self.user.id
            }
        )

    def test_delete_lesson(self):
        """ Test lesson deleting """

        response = self.client.delete(reverse('collection:lesson_delete', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.all().exists())

    def tearDown(self):
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()