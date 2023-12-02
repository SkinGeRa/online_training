from django.utils import timezone
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from training.models import Course, Lesson, Subscription
from training.paginators import CoursePaginator
from training.permissions import IsModerator, IsOwner
from training.serializers import CourseSerializer, LessonSerializer, CourseCreateSerializer, SubscriptionSerializer
from training.services import send_sub_message
from training.tasks import send_update_course


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated | IsModerator | IsOwner]
    pagination_class = CoursePaginator

    def create(self, request, *args, **kwargs):
        serializer = CourseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()
        return Response(CourseCreateSerializer(new_course).data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.last_updated = timezone.now()
        instance.save()

        subscriptions = Subscription.objects.filter(
            course=instance,
            is_active=True
        )
        user_emails = [subscription.user.email for subscription in subscriptions]
        send_update_course.delay(instance.name, user_emails)


class LessonCreateAPIView(generics.CreateAPIView):
    """ Создание урока """
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """ Просмотр списка уроков """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsModerator | IsOwner]
    pagination_class = CoursePaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Просмотр урока """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Изменение урока """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Удаление урока """
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated | IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """ Создание подписки """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated | IsModerator | IsOwner]

    def perform_create(self, serializer):
        new_sub = serializer.save()
        new_sub.user = self.request.user
        new_sub.save()
        send_sub_message(new_sub.user.email, new_sub.course.title)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """ Удаление подписки """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated | IsModerator | IsOwner]