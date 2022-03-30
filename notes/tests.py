from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from base.tests import BaseTestCase

from notes.models import Note


class NotesTestCase(BaseTestCase):
    def test_notes_page(self):
        response = self.client.get(reverse('notes_home'))
        self.assertEqual(response.status_code, 200)

    def test_create_note(self):
        test_note = Note.objects.create(
            title='Test Note',
            content='This is a test note.',
            course=self.course,
            user=self.user
        )
        self.assertEqual(test_note.title, 'Test Note')
        self.assertEqual(test_note.content, 'This is a test note.')
        self.assertEqual(test_note.course, self.course)
        self.assertEqual(test_note.user, self.user)

    def test_delete_note(self):
        test_note = Note.objects.create(
            title='Test Note',
            content='This is a test note.',
            course=self.course,
            user=self.user
        )
        test_note.delete()
        self.assertEqual(Note.objects.count(), 0)