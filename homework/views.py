import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from homework.forms import HomeworkAssignmentForm, ReadingAssignmentForm
from homework.models import HomeworkAssignment, ReadingAssignment
from school.models import School

context = {'schools': School.objects.all()}


@login_required
def homework(request):
    context['account'] = request.user

    dt = datetime.datetime.today()

    last_assignment = HomeworkAssignment.objects.filter(course__user=request.user).order_by('due_date').last()

    all_delta = datetime.date(last_assignment.due_date.year, last_assignment.due_date.month,
                              last_assignment.due_date.day) - datetime.date(dt.year, dt.month, dt.day) if last_assignment else None

    all_dates = [dt + datetime.timedelta(days=i) for i in range(all_delta.days + 1)] if all_delta else []

    context['all_dates'] = all_dates

    context['late_assignments'] = HomeworkAssignment.objects.late_assignments(request.user)

    context['all_assignments'] = HomeworkAssignment.objects.all_assignments(request.user)

    context['reading_objects'] = ReadingAssignment.objects.all_assignments(request.user)

    context['reading_assignments'] = ReadingAssignment.get_recommended_readings(request.user)

    context['used_dates'] = HomeworkAssignment.objects.date_range(request.user)

    context['completed_assignments'] = HomeworkAssignment.objects.filter(completed=True, course__user=request.user)

    return render(request, 'homework.html', context)


@login_required
def add_assignment(request, id=None):
    context['account'] = request.user

    instance = None

    context['form_title'] = 'Add Assignment'
    context['form_description'] = 'Here you can add an assignment for a specific class'
    context['excluded_fields'] = []

    if id:
        instance = get_object_or_404(HomeworkAssignment, id=id)
        context['form_title'] = 'Edit Assignment'
        context['form_description'] = 'Here you can edit an assignment for a specific class'
        if not instance.course.user == request.user:
            return redirect('homework')

    if request.POST:
        form = HomeworkAssignmentForm(request.POST, instance=instance if instance else None, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            if id:
                messages.success(request, 'Assignment edited successfully')
            else:
                messages.success(request, 'Assignment added successfully')
            return redirect('homework')
    else:
        form = HomeworkAssignmentForm(instance=instance if instance else None, user=request.user,
                                      initial={'course': instance.course if instance else request.GET.get('course')})

    context['form'] = form

    return render(request, 'forms/add_assignment.html', context)


@login_required
def delete_assignment(request, id):
    context['account'] = request.user
    assignment = get_object_or_404(HomeworkAssignment, id=id)
    assignment.delete()
    return redirect('homework')


@login_required
def add_reading_assignment(request, id=None):
    context['account'] = request.user

    instance = None

    context['form_title'] = 'Add Reading Assignment'
    context['form_description'] = 'Here you can add a reading assignment for your class. This is different from a ' \
                                  'regular assignment because UMS will evenly distribute your reading automatically ' \
                                  'for you'
    context['excluded_fields'] = []

    if id:
        instance = get_object_or_404(ReadingAssignment, id=id)
        context['form_title'] = 'Edit Assignment'
        context['form_description'] = 'Here you can edit a reading assignment for your class. This is different from ' \
                                      'a regular assignment because UMS will evenly distribute your reading ' \
                                      'automatically for you '
        if not instance.course.user == request.user:
            return redirect('homework')

    if request.POST:
        form = ReadingAssignmentForm(request.POST, instance=instance if instance else None, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            if id:
                messages.success(request, 'Reading Assignment edited successfully')
            else:
                messages.success(request, 'Reading Assignment added successfully')
            return redirect('homework')
    else:
        form = ReadingAssignmentForm(instance=instance if instance else None, user=request.user,
                                     initial={'course': instance.course if instance else request.GET.get('course')})

    context['form'] = form

    return render(request, 'forms/add_assignment.html', context)


@login_required
def delete_reading_assignment(request, id):
    context['account'] = request.user
    assignment = get_object_or_404(ReadingAssignment, id=id)
    assignment.delete()
    return redirect('homework')


@login_required
def complete_assignment(request, id):
    context['account'] = request.user
    assignment = get_object_or_404(HomeworkAssignment, id=id)
    if assignment.completed:
        assignment.completed = False
        assignment.save()
    else:
        assignment.completed = True
        messages.success(request, 'Congratulations! I\'m proud of you!')
        assignment.save()
    return redirect('homework')
