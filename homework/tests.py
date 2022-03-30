# Create your tests here.
import datetime

from django.urls import reverse

from base.tests import BaseTestCase
from homework.models import HomeworkAssignment, ReadingAssignment, ReadingDay


class HomeworkTest(BaseTestCase):
    def test_homework_list_view(self):
        response = self.client.get(reverse('homework'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homework.html')

    def test_homework_all_assignments(self):
        self.assertEqual(HomeworkAssignment.objects.all_assignments(self.user).count(), 1)
        self.assertEqual(HomeworkAssignment.objects.all_assignments(self.user).first().name, 'Problems 1-10')

    def test_homework_late_assignments(self):
        self.assertEqual(HomeworkAssignment.objects.late_assignments(self.user).count(), 0)
        test_late_assignment = HomeworkAssignment.objects.create(
            name='Late Assignment',
            due_date='2019-12-31',
            due_time='23:59',
            description='This is a late assignment',
            course=self.course
        )
        self.assertEqual(HomeworkAssignment.objects.late_assignments(self.user).count(), 1)
        HomeworkAssignment.objects.get(id=test_late_assignment.id).delete()

    def test_reading_assignment(self):
        self.assertEqual(ReadingAssignment.objects.all_assignments(self.user).count(), 0)
        test_reading_assignment = ReadingAssignment.objects.create(
            name='Reading Assignment',
            due_date=datetime.date.today(),
            due_time='23:59',
            description='This is a reading assignment',
            course=self.course,
            start_page=1,
            end_page=10
        )
        self.assertEqual(ReadingAssignment.objects.all_assignments(self.user).count(), 1)
        test_reading_assignment.delete()
        self.assertEqual(ReadingAssignment.objects.all_assignments(self.user).count(), 0)
