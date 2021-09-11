import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from homework.forms import HomeworkAssignmentForm
from homework.models import HomeworkAssignment
from school.models import School

context = {'schools': School.objects.all()}


@login_required
def homework(request):
    context['account'] = request.user

    dt = datetime.datetime.today()
    dt_time = datetime.datetime.now().strftime('%H:%M:%S')
    week_dates = [dt + datetime.timedelta(days=i) for i in range(7)]

    context['late_assignments'] = HomeworkAssignment.objects.filter(
        due_date__lte=dt,
        completed=False,
        course__user=request.user,
        due_time__lt=dt_time
    )

    context['all_assignments'] = HomeworkAssignment.objects.filter(
        completed=False,
        course__user=request.user,
        due_date__gte=dt
    )

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
        form = HomeworkAssignmentForm(instance=instance if instance else None, user=request.user, initial={'course': instance.course if instance else request.GET.get('course')})

    context['form'] = form

    return render(request, 'forms/add_assignment.html', context)


@login_required
def delete_assignment(request, id):
    context['account'] = request.user
    assignment = get_object_or_404(HomeworkAssignment, id=id)
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
