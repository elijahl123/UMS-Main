import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# Create your views here.
from pytz import timezone

from UMSMain.generic_class_views import ModelCreationView, ModelEditView, ModelDeleteView, ModelChangeAttrView, \
    all_permissions_required
from homework.forms import HomeworkAssignmentForm, ReadingAssignmentForm
from homework.models import HomeworkAssignment, ReadingAssignment

context = {}


@login_required
@all_permissions_required
def homework(request):
    context['account'] = request.user

    dt = datetime.datetime.now(timezone(request.user.timezone))

    last_assignment = HomeworkAssignment.objects.filter(course__user=request.user).order_by('due_date').last()

    all_delta = timezone(request.user.timezone).localize(last_assignment.due_datetime) - dt if last_assignment else None

    all_dates = [dt + datetime.timedelta(days=i) for i in range(all_delta.days + 2)] if all_delta else []

    context['all_dates'] = all_dates

    context['late_assignments'] = HomeworkAssignment.objects.late_assignments(request.user)

    context['all_assignments'] = HomeworkAssignment.objects.all_assignments(request.user)

    context['reading_objects'] = ReadingAssignment.objects.all_assignments(request.user, reading=True)

    context['reading_assignments'] = ReadingAssignment.get_recommended_readings(request.user)

    context['used_dates'] = HomeworkAssignment.objects.date_range(request.user)

    context['completed_assignments'] = HomeworkAssignment.objects.filter(completed=True, course__user=request.user)

    return render(request, 'homework.html', context)


class AddAssignmentView(ModelCreationView):
    form_class = HomeworkAssignmentForm
    template_name = 'forms/add_assignment.html'
    redirect_url = 'homework'

    form_title = 'Add Assignment'
    form_description = 'Here you can add an assignment for a specific class'
    excluded_fields = ['uid']
    success_message = 'Assignment added successfully'
    require_user = True


class EditAssignmentView(ModelEditView):
    model = HomeworkAssignment
    form_class = HomeworkAssignmentForm
    template_name = 'forms/add_assignment.html'
    redirect_url = 'homework'

    form_title = 'Edit Assignment'
    form_description = 'Here you can edit an assignment for a specific class'
    excluded_fields = ['uid']
    success_message = 'Assignment edited successfully'
    require_user = True


class DeleteAssignmentView(ModelDeleteView):
    model = HomeworkAssignment
    redirect_url = 'homework'
    success_message = 'Assignment deleted successfully'


class AddReadingAssignment(ModelCreationView):
    form_class = ReadingAssignmentForm
    template_name = 'forms/add_reading_assignment.html'
    redirect_url = 'homework'

    form_title = 'Add Reading Assignment'
    form_description = 'Here you can add a reading assignment for your class. This is different from a ' \
                       'regular assignment because UMS will evenly distribute your reading automatically ' \
                       'for you'
    excluded_fields = ['include_due_date', 'uid']
    success_message = 'Reading Assignment added successfully'
    require_user = True


class EditReadingAssignment(ModelEditView):
    model = ReadingAssignment
    form_class = ReadingAssignmentForm
    template_name = 'forms/add_reading_assignment.html'
    redirect_url = 'homework'

    form_title = 'Edit Reading Assignment'
    form_description = 'Here you can edit a reading assignment for your class. This is different from a ' \
                       'regular assignment because UMS will evenly distribute your reading automatically ' \
                       'for you'
    excluded_fields = ['include_due_date', 'uid']
    success_message = 'Reading Assignment edited successfully'
    require_user = True


class DeleteReadingAssignment(ModelDeleteView):
    model = ReadingAssignment
    redirect_url = 'homework'
    success_message = 'Reading Assignment deleted successfully'


class CompleteAssignment(ModelChangeAttrView):
    model = HomeworkAssignment
    redirect_url = 'homework'
    change_attr: str = 'completed'
    alternate = True
