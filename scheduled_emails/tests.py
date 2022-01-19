# Create your tests here.
import datetime

import pytz
from django.core.management import call_command
from django.forms import model_to_dict

from base.tests import BaseTestCase
from homework.models import HomeworkAssignment
from scheduled_emails.models import ScheduledEmail


class ScheduledEmailTest(BaseTestCase):
    pass
