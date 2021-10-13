from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView


# noinspection PyMissingConstructor
class ModelCreationView(LoginRequiredMixin, TemplateView):
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

        form = self.form_class(**self.get_form_kwargs(request))

        additional_context['form'] = form

        return render(request, self.template_name, self.get_context_data(request, **additional_context))

    def post(self, request, **kwargs):
        additional_context = {'account': request.user}

        form = self.form_class(request.POST, request.FILES or None, **self.get_form_kwargs(request))

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


class ModelDeleteView(LoginRequiredMixin, View):
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


class ModelChangeAttrView(LoginRequiredMixin, View):
    model = None
    redirect_url: str = 'index'
    change_attr: str = ''
    change_to = None
    alternate: bool = True
    identifier_name: str = 'id'

    def get_instance_kwargs(self, **kwargs):
        instance_kwargs = {
            'id': kwargs[self.identifier_name]
        }
        return instance_kwargs

    def get(self, request, **kwargs):
        obj = get_object_or_404(self.model, **self.get_instance_kwargs(**kwargs))
        if self.alternate:
            setattr(obj, self.change_attr, not getattr(obj, self.change_attr))
        else:
            setattr(obj, self.change_attr, self.change_to)
        obj.save()

        redirect_next = request.GET.get('next')

        return HttpResponseRedirect(redirect_next) if redirect_next else redirect(self.redirect_url)
