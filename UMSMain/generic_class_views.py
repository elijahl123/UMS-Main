from functools import wraps
from urllib.parse import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.views import View
from django.views.generic import TemplateView


def school_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    actual_decorator = user_passes_test(
        lambda u: u.school,
        login_url='add_school',
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def timezone_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    actual_decorator = user_passes_test(
        lambda u: u.timezone,
        login_url='select_timezone',
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def all_permissions_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    perms = [
        (lambda u: u.school, 'add_school'),
        (lambda u: u.timezone, 'select_timezone'),
        (lambda u: u.check_sub_status(), 'choose_plan'),
        (lambda u: u.check_payment_status(), 'payment_edit_payment_method')
    ]

    actual_decorator = user_passes_multiple_tests(
        perms,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def user_passes_multiple_tests(perms, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            for test_func, login_url in perms:

                if test_func(request.user):
                    continue
                path = request.build_absolute_uri()
                resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
                # If the login url is the same scheme and net location then just
                # use the path as the "next" url.
                login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
                current_scheme, current_netloc = urlparse(path)[:2]
                if ((not login_scheme or login_scheme == current_scheme) and
                        (not login_netloc or login_netloc == current_netloc)):
                    path = request.get_full_path()
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(
                    path, resolved_login_url, redirect_field_name)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


class PermissionsRequiredMixin(UserPassesTestMixin):
    login_url = 'add_school'

    def handle_no_permission(self):
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
                (not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )

    def test_func(self):
        if not self.request.user.school:
            self.login_url = 'add_school'
            return False
        if not self.request.user.timezone:
            self.login_url = 'select_timezone'
            return False
        if not self.request.user.check_sub_status():
            self.login_url = 'choose_plan'
            return False
        if not self.request.user.check_payment_status():
            return False
        return True


class ModelCreationView(LoginRequiredMixin, PermissionsRequiredMixin, TemplateView):
    form_class = None
    initial: dict = {}
    instance = None
    template_name: str = None
    redirect_url: str = 'index'

    form_title: str = ''
    form_description: str = ''
    excluded_fields: list = []
    success_message = None
    require_user: bool = False

    context: dict = {}

    def get_form_kwargs(self, request, **kwargs):
        form_class_kwargs = {
            'initial': self.initial,
        }
        if self.require_user:
            form_class_kwargs['user'] = request.user
        if self.instance:
            form_class_kwargs['instance'] = self.instance
        form_class_kwargs.update(**kwargs)
        return form_class_kwargs

    def get_context_data(self, request, **kwargs):
        context = self.context
        form_data = {
            'form_title': self.form_title,
            'form_description': self.form_description,
            'excluded_fields': self.excluded_fields,
        }
        context.update(form_data)
        context.update(kwargs)
        return context

    def get(self, request, **kwargs):
        additional_context = {'account': request.user}

        temp_init = self.initial

        if request.GET:
            for key in request.GET:
                temp_init[key] = request.GET[key]
        else:
            temp_init.clear()

        self.initial.update(temp_init)

        form: ModelForm = self.form_class(**self.get_form_kwargs(request))

        additional_context['form'] = form

        return render(request, self.template_name, self.get_context_data(request, **additional_context))

    def post(self, request, **kwargs):
        additional_context = {'account': request.user}

        form: ModelForm = self.form_class(request.POST, request.FILES or None, **self.get_form_kwargs(request))

        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

            if self.success_message:
                messages.success(request, self.success_message)

            redirect_next = request.GET.get('next')

            return HttpResponseRedirect(redirect_next) if redirect_next else redirect(self.redirect_url)

        additional_context['form'] = form

        return render(request, self.template_name, self.get_context_data(request, **additional_context))


class ModelEditView(ModelCreationView):
    model = None
    identifier_name = 'id'

    def get_instance_kwargs(self, request, **kwargs):
        instance_kwargs = {
            'id': kwargs[self.identifier_name]
        }
        if hasattr(self.model, 'course'):
            instance_kwargs['course__user'] = request.user
        return instance_kwargs

    def get(self, request, **kwargs):
        self.instance = get_object_or_404(self.model, **self.get_instance_kwargs(request, **kwargs))
        return super().get(request, **kwargs)

    def post(self, request, **kwargs):
        self.instance = get_object_or_404(self.model, **self.get_instance_kwargs(request, **kwargs))
        return super().post(request, **kwargs)


class ModelDeleteView(LoginRequiredMixin, PermissionsRequiredMixin, View):
    model = None
    redirect_url = 'index'
    identifier_name = 'id'
    success_message = None

    def get_instance_kwargs(self, **kwargs):
        instance_kwargs = {
            'id': kwargs[self.identifier_name]
        }
        return instance_kwargs

    def get(self, request, **kwargs):
        obj = get_object_or_404(self.model, **self.get_instance_kwargs(**kwargs))
        obj.delete()
        if self.success_message:
            messages.success(request, self.success_message)

        redirect_next = request.GET.get('next')

        return HttpResponseRedirect(redirect_next) if redirect_next else redirect(self.redirect_url)


class ModelChangeAttrView(LoginRequiredMixin, PermissionsRequiredMixin, View):
    model = None
    redirect_url: str = 'index'
    change_attr: str = ''
    change_to = None
    alternate: bool = True
    identifier_name: str = 'id'

    def get_instance_kwargs(self, request, **kwargs):
        instance_kwargs = {
            'id': kwargs[self.identifier_name]
        }
        if hasattr(self.model, 'course'):
            instance_kwargs['course__user'] = request.user
        return instance_kwargs

    def get(self, request, **kwargs):
        obj = get_object_or_404(self.model, **self.get_instance_kwargs(request, **kwargs))
        if self.alternate:
            setattr(obj, self.change_attr, not getattr(obj, self.change_attr))
        else:
            setattr(obj, self.change_attr, self.change_to)
        obj.save()

        redirect_next = request.GET.get('next')

        return HttpResponseRedirect(redirect_next) if redirect_next else redirect(self.redirect_url)
