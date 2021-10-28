import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from pytz import timezone

from UMSMain.generic_class_views import school_required, timezone_required
from class_calendar.models import CalendarEvent
from courses.forms import CourseForm, CourseTimeForm, CourseTimeEditForm, CourseFileForm, FeedbackForm, CourseLinkForm
from courses.models import CourseTime, Course, CourseFile, CourseLink
# Create your views here.
from homework.models import HomeworkAssignment
from users.models import Account

context = {}


@login_required
@school_required
@timezone_required
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
@school_required
@timezone_required
def add_coursetime(request):
    context['account'] = request.user

    if request.POST:
        form = CourseTimeForm(request.POST, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('manage_schedule')
        for error in form.errors.as_data():
            for e in form.errors[error]:
                messages.error(request, 'Error in \'{}\' field: {}'.format(error, e).title())

    return redirect('manage_schedule')


@login_required
@school_required
@timezone_required
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
@school_required
@timezone_required
def edit_course(request, id):
    context['account'] = request.user

    course = get_object_or_404(Course, id=id)

    if not course.user == request.user:
        return redirect('manage_schedule')

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
@school_required
@timezone_required
def edit_coursetime(request, id):
    context['account'] = request.user

    coursetime = get_object_or_404(CourseTime, id=id)

    if not coursetime.user == request.user:
        return redirect('manage_schedule')

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
        form = CourseTimeEditForm(instance=coursetime, user=request.user, initial={'course': coursetime.course})

    context['form'] = form

    return render(request, 'forms/edit_course.html', context)


@login_required
@school_required
@timezone_required
def index(request):
    context['account'] = request.user

    dt = datetime.datetime.now(timezone(request.user.timezone))
    week_dates = [dt + datetime.timedelta(days=i) for i in range(4)]
    today_weekday = datetime.datetime.now(timezone(request.user.timezone)).strftime("%A")

    context['upcoming_assignments'] = HomeworkAssignment.objects.upcoming_assignments(request.user)

    context['late_assignments'] = HomeworkAssignment.objects.late_assignments(request.user)

    context['today_and_tomorrow'] = CalendarEvent.objects.filter(user=request.user, date__in=week_dates)

    context['coursetimes_for_today'] = CourseTime.objects.filter(weekday__contains=today_weekday,
                                                                 course__user=request.user)

    return render(request, 'index.html', context)


@login_required
@school_required
@timezone_required
def feedback(request):
    context['account'] = request.user

    context['form_title'] = 'Feedback'
    context['form_description'] = 'Give the developers feedback on the software and report any problems in the system ' \
                                  'as well ideas for new features. '

    if request.POST:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            email = EmailMessage(**form.cleaned_data, to=['elijah.kane.1972@gmail.com'],
                                 from_email='%s via UMS <untitledmanagementsoftware@gmail.com>' % request.user.username)
            email.send()
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('index')
    else:
        form = FeedbackForm()

    context['form'] = form

    return render(request, 'form_template.html', context)


@login_required
@school_required
@timezone_required
def manage_schedule(request):
    context['account'] = request.user

    context['courses'] = Course.objects.filter(user=request.user)
    context['coursetimes'] = CourseTime.objects.filter(user=request.user)

    return render(request, 'manage_schedule.html', context)


@login_required
@school_required
@timezone_required
def delete_course(request, id):
    context['account'] = request.user
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect('class_schedule')


@login_required
@school_required
@timezone_required
def delete_coursetime(request, id):
    context['account'] = request.user
    coursetime = get_object_or_404(CourseTime, id=id)
    coursetime.delete()
    return redirect('class_schedule')


@login_required
@school_required
@timezone_required
def course_view(request, id):
    context['account'] = request.user
    course = get_object_or_404(Course, id=id)
    if course.user != request.user:
        return redirect('class_schedule')
    context['course'] = course
    return render(request, 'courses/course_template.html', context)


@login_required
@school_required
@timezone_required
def course_files(request, id):
    context['account'] = request.user
    course = get_object_or_404(Course, id=id)
    if course.user != request.user:
        return redirect('class_schedule')
    context['course'] = course

    context['course_files'] = CourseFile.objects.filter(course__user=request.user, course=course)

    return render(request, 'courses/course_files.html', context)


@login_required
@school_required
@timezone_required
def add_course_file(request, id, file_id=None):
    context['account'] = request.user
    course = get_object_or_404(Course, id=id)
    if course.user != request.user:
        return redirect('class_schedule')
    context['course'] = course

    context['form_title'] = 'Add Course File'
    context['form_description'] = 'Here you can add important files to your course'

    coursefile = None
    if file_id:
        coursefile = get_object_or_404(CourseFile, id=file_id)
        context['form_title'] = 'Edit Course File'
        if coursefile.course.user != request.user:
            return redirect('course_files')

    if request.POST:
        form = CourseFileForm(request.POST, request.FILES, instance=coursefile, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            message = 'Course File was added successfully'
            if file_id:
                message = 'Course File was edited successfully'
            messages.success(request, message)
            return redirect('course_files', course.id)
    else:
        form = CourseFileForm(instance=coursefile, user=request.user, initial={'course': id})

    context['form'] = form

    return render(request, 'form_template.html', context)


@login_required
@school_required
@timezone_required
def delete_course_file(request, id, file_id):
    context['account'] = request.user
    course = get_object_or_404(Course, id=id)
    if course.user != request.user:
        return redirect('class_schedule')
    context['course'] = course
    coursefile = get_object_or_404(CourseFile, id=file_id)
    coursefile.delete()
    return redirect('course_files', id)


@login_required
@school_required
@timezone_required
def course_assignments(request, id):
    context['account'] = request.user
    course = get_object_or_404(Course, id=id)
    if course.user != request.user:
        return redirect('class_schedule')
    context['course'] = course

    context['class_assignments'] = HomeworkAssignment.objects.all_assignments(request.user, course=course)

    context['late_class_assignments'] = HomeworkAssignment.objects.late_assignments(request.user, course=course)

    context['completed_class_assignments'] = HomeworkAssignment.objects.filter(course=course, completed=True)

    return render(request, 'courses/course_assignments.html', context)


@login_required
@school_required
@timezone_required
def course_links(request, id):
    context['account'] = request.user
    course = get_object_or_404(Course, id=id)
    if course.user != request.user:
        return redirect('class_schedule')
    context['course'] = course

    context['course_links'] = CourseLink.objects.filter(course__user=request.user, course=course)

    return render(request, 'courses/course_links.html', context)


@login_required
@school_required
@timezone_required
def add_course_link(request, id, link_id=None):
    context['account'] = request.user
    course = get_object_or_404(Course, id=id)
    if course.user != request.user:
        return redirect('class_schedule')
    context['course'] = course

    context['form_title'] = 'Add Course Link'
    context['form_description'] = 'Here you can add important links to your course'

    courselink = None
    if link_id:
        courselink = get_object_or_404(CourseLink, id=link_id)
        context['form_title'] = 'Edit Course Link'
        if courselink.course.user != request.user:
            return redirect('course_links')

    if request.POST:
        form = CourseLinkForm(request.POST, request.FILES, instance=courselink, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            message = 'Course Link was added successfully'
            if link_id:
                message = 'Course Link was edited successfully'
            messages.success(request, message)
            return redirect('course_links', course.id)
    else:
        form = CourseLinkForm(instance=courselink, user=request.user, initial={'course': id})

    context['form'] = form

    return render(request, 'form_template.html', context)


@login_required
@school_required
@timezone_required
def delete_course_link(request, id, link_id):
    context['account'] = request.user
    course = get_object_or_404(Course, id=id)
    if course.user != request.user:
        return redirect('class_schedule')
    context['course'] = course
    courselink = get_object_or_404(CourseLink, id=link_id)
    courselink.delete()
    return redirect('course_links', id)


@login_required
@school_required
@timezone_required
def course_coursetimes(request, id):
    context['account'] = request.user
    course = get_object_or_404(Course, id=id)
    if course.user != request.user:
        return redirect('class_schedule')
    context['course'] = course

    coursetimes = CourseTime.objects.filter(course=course)
    context['coursetimes'] = coursetimes

    return render(request, 'courses/course_coursetimes.html', context)


def privacy_policy(request):
    context['account'] = request.user

    return render(request, 'privacy-policy.html', context)
