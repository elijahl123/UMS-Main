from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from school.models import School
from users.forms import AccountForm

context = {'schools': School.objects.all()}


@login_required
def account(request):
    context['account'] = request.user

    if request.POST:
        form = AccountForm(request.POST, request.FILES or None, instance=request.user)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('account')
    else:
        form = AccountForm(instance=request.user)

    context['form'] = form

    return render(request, 'account.html', context)
