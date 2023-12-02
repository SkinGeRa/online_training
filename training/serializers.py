from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from training.models import Course, Lesson, Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = '__all__'


class CourseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lesson_set.all().count()

    def get_lessons(self, course):
        return LessonSerializer(Lesson.objects.filter(course=course), many=True).data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj, is_active=True).exists()
        return False

    class Meta:
        model = Course
        fields = '__all__'
