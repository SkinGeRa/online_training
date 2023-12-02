from django.contrib import admin

from training.models import Course
from training.models import Lesson

admin.site.register(Course)
admin.site.register(Lesson)
