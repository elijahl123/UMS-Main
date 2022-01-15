from django.shortcuts import get_object_or_404

# Create your tests here.
from base.tests import BaseTestCase
from courses.models import Course
from users.models import Account


class CourseTestCase(BaseTestCase):

    def test_delete_course(self):
        self.course.delete()
