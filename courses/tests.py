# Create your tests here.
from django.urls import reverse

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

    def test_course_urls(self):
        # Course CRUD

        test_course = Course.objects.create(
            name='test_course_urls.name',
            user=self.user,
            title='test_course_urls.title',
            teacher='Elijah Lopez',
            color='primary'
        )
        self.assertEqual(self.client.get(reverse("add_course")).status_code, 200)
        self.assertEqual(self.client.get(reverse("edit_course", args=[test_course.id])).status_code, 200)
        self.assertEqual(self.client.get(reverse("delete_course", args=[test_course.id])).status_code, 302)

        # CourseTime CRUD

        test_coursetime = CourseTime.objects.create(
            course=self.course,
            user=self.user,
            location='Online',
            start_time='15:00:00',
            end_time='18:15:00',
            weekday="['Tuesday', 'Thursday']"
        )
        self.assertEqual(self.client.get(reverse("add_coursetime")).status_code, 302)
        self.assertEqual(self.client.get(reverse("edit_coursetime", args=[test_coursetime.id])).status_code, 200)
        self.assertEqual(self.client.get(reverse("delete_coursetime", args=[test_coursetime.id])).status_code, 302)

        # Course Link CRUD

        test_course_link = CourseLink.objects.create(
            course=self.course,
            title='test_course_link_urls.title',
            link='https://client.untitledmanagementsoftware.com/login'
        )
        self.assertEqual(self.client.get(reverse("add_course_link", args=[self.course.id])).status_code, 200)
        self.assertEqual(
            self.client.get(reverse("edit_course_link", args=[self.course.id, test_course_link.id])).status_code,
            200
        )
        self.assertEqual(
            self.client.get(reverse("delete_course_link", args=[test_coursetime.id, test_course_link.id])).status_code,
            302
        )

    def test_delete_course(self):
        self.course.delete()
