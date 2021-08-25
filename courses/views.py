from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from courses.forms import CourseForm, CourseTimeForm, CourseTimeEditForm
from courses.models import CourseTime, Course
# Create your views here.
from school.models import School
from users.models import Account

context = {'schools': School.objects.all()}


@login_required
def index(request):
    context['account'] = request.user
    return render(request, 'index.html', context)


@login_required
def add_course(request):
    if not request.user.school:
        return redirect('index')

    context['account'] = request.user

    context['form_title'] = 'Add Course'
    context['form_description'] = 'Add a course to your schedule. This will integrate automatically with the ' \
                                  'calendar and schedule features'
    context['excluded_fields'] = ['school', 'user']

    if request.POST:
        form = CourseForm(request.POST, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            messages.success(request, '%s added successfully' % obj.name)
            obj.save()
            return redirect('manage_schedule')
    else:
        form = CourseForm()

    context['form'] = form

    return render(request, 'forms/add_course.html', context)


@login_required
def add_school(request):
    context['account'] = request.user

    if request.POST:
        school = request.POST.get('school')
        selected_school = get_object_or_404(School, id=school)
        Account.objects.filter(id=request.user.id).update(school=selected_school)
        return redirect('index')

    return redirect('index')


@login_required
def class_schedule(request):
    context['account'] = request.user

    if not Course.objects.filter(user=request.user):
        return redirect('manage_schedule')

    context['weekdays'] = [
        ('Sun', 'Sunday'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday')
    ]

    context['coursetimes'] = CourseTime.objects.filter(user=request.user)

    return render(request, 'schedule.html', context)


@login_required
def manage_schedule(request):
    context['account'] = request.user

    context['courses'] = Course.objects.filter(user=request.user)
    context['coursetimes'] = CourseTime.objects.filter(user=request.user)

    return render(request, 'manage_schedule.html', context)


@login_required
def add_coursetime(request):
    context['account'] = request.user

    if request.POST:
        form = CourseTimeForm(request.POST, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('manage_schedule')
        else:
            messages.error(request, '<strong>Error:</strong> Please enter a valid weekday for the Course Time')

    return redirect('manage_schedule')


@login_required
def edit_course(request, id):
    context['account'] = request.user

    course = get_object_or_404(Course, id=id)

    context['form_title'] = 'Edit ' + course.name
    context['form_description'] = 'Edit a course already in your schedule and it will be integrated with the calendar ' \
                                  'and other features '

    context['excluded_fields'] = ['school', 'user']

    if request.POST:
        form = CourseForm(request.POST, request.FILES or None, instance=course)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, '%s changed successfully' % obj.name)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('index')
    else:
        form = CourseForm(instance=course)

    context['form'] = form

    return render(request, 'forms/edit_course.html', context)


@login_required
def edit_coursetime(request, id):
    context['account'] = request.user

    coursetime = get_object_or_404(CourseTime, id=id)

    context['form_title'] = 'Edit ' + coursetime.course.name
    context['form_description'] = 'Edit a course already in your schedule and it will be integrated with the calendar ' \
                                  'and other features '

    context['excluded_fields'] = ['school', 'user']

    if request.POST:
        form = CourseTimeEditForm(request.POST, request.FILES or None, instance=coursetime, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, '%s changed successfully' % obj.course.name)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('index')
    else:
        form = CourseTimeEditForm(instance=coursetime, user=request.user)

    context['form'] = form

    return render(request, 'forms/edit_course.html', context)
