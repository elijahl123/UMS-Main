# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from users.models import Account

context = {}


@login_required
def add_school(request):
    context['account'] = request.user

    if request.POST and request.POST.get('school'):
        user = Account.objects.get(id=request.user.id)
        user.school = request.POST.get('school')
        user.save()
        messages.success(request, 'School Successfully Selected')

        redirect_next = request.GET.get('next')

        return HttpResponseRedirect(redirect_next) if redirect_next else redirect('index')

    return render(request, 'set_up/add_school.html', context)
