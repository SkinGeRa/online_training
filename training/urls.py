from django.urls import path

from training.apps import TrainingConfig
from rest_framework.routers import DefaultRouter

from training.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView

app_name = TrainingConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    # lesson
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    # subscriptions
    path('sub/create/', SubscriptionCreateAPIView.as_view(), name='sub_create'),
    path('sub/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='sub_delete'),
] + router.urls
