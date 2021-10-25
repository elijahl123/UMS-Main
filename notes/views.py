import datetime

from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from pytz import timezone

from UMSMain.generic_class_views import school_required, timezone_required
from courses.models import Course
from notes.forms import NotesForm
from notes.models import Note

context = {}


@login_required
@school_required
@timezone_required
def notes_home(request):
    context['account'] = request.user
    context['courses'] = Course.objects.filter(user=request.user)
    return render(request, 'notes/notes_home.html', context)


@login_required
@school_required
@timezone_required
def notes_home_course(request, course_id):
    context['account'] = request.user
    course = get_object_or_404(Course, id=course_id)

    if not course.user == request.user:
        return redirect('notes_home')

    context['course'] = course
    context['notes'] = Note.objects.filter(course=course, user=request.user)
    return render(request, 'notes/notes_home_course.html', context)


@login_required
@school_required
@timezone_required
def add_notes(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if not course.user == request.user:
        return redirect('notes_home')

    obj = Note.objects.create(course=course, user=request.user,
                              title=f'Notes for {datetime.datetime.now(timezone(request.user.timezone)).strftime("%Y-%M-%d")}') if request.GET.get('daily-notes') else Note.objects.create(course=course, user=request.user)

    return redirect('notes_view_notes', course_id, obj.id)


@login_required
@school_required
@timezone_required
def view_notes(request, course_id, notes_id):
    context['account'] = request.user
    course = get_object_or_404(Course, id=course_id)

    if not course.user == request.user:
        return redirect('notes_home')

    context['course'] = course
    note = get_object_or_404(Note, id=notes_id)
    context['note'] = note

    if request.POST:
        form = NotesForm(request.POST, instance=note)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
    else:
        form = NotesForm(instance=note)

    context['form'] = form

    return render(request, 'notes/notes_view_notes.html', context)


@login_required
@school_required
@timezone_required
def delete_notes(request, course_id, notes_id):
    course = get_object_or_404(Course, id=course_id)

    if not course.user == request.user:
        return redirect('notes_home')

    note = get_object_or_404(Note, id=notes_id)
    note.delete()
    return redirect('notes_home_course', course_id)
