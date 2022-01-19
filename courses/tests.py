# Create your tests here.
from base.tests import BaseTestCase
from courses.models import *


class CourseTestCase(BaseTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.course_link = CourseLink.objects.create(
            course=self.course,
            title='Test Link',
            link='https://client.untitledmanagementsoftware.com'
        )

    def test_delete_course(self):
        self.course.delete()
