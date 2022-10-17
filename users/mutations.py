import graphene
from graphql_jwt import shortcuts
from allauth.account.forms import SignupForm, AddEmailForm, ChangePasswordForm, SetPasswordForm, ResetPasswordForm, \
    ResetPasswordKeyForm
from django import forms
from graphql_jwt.decorators import login_required

from base.forms import UmsFormMutation


class UMSSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(max_length=30, label='First Name')
        self.fields['last_name'] = forms.CharField(max_length=30, label='Last Name')


class SignupMutation(UmsFormMutation):
    class Meta:
        form_class = UMSSignupForm

    token = graphene.String()

    @classmethod
    def perform_mutate(cls, form, info):
        if form.is_valid():
            user = form.save(info.context)
            # Call the login mutation to get the token
            token = shortcuts.get_token(user)
            return cls(errors=[], token=token, **form.cleaned_data)
        return cls(errors=[], token=None, **form.cleaned_data)


class AddEmailMutation(UmsFormMutation):
    class Meta:
        form_class = AddEmailForm

    @classmethod
    @login_required
    def perform_mutate(cls, form, info):
        form.save(info.context)
        return cls(errors=[], **form.cleaned_data)


class ChangePasswordMutation(UmsFormMutation):
    class Meta:
        form_class = ChangePasswordForm

    @classmethod
    @login_required
    def perform_mutate(cls, form, info):
        form.save(info.context)
        return cls(errors=[], **form.cleaned_data)


class SetPasswordMutation(UmsFormMutation):
    class Meta:
        form_class = SetPasswordForm

    @classmethod
    @login_required
    def perform_mutate(cls, form, info):
        form.save(info.context)
        return cls(errors=[], **form.cleaned_data)


class ResetPasswordMutation(UmsFormMutation):
    class Meta:
        form_class = ResetPasswordForm

    @classmethod
    @login_required
    def perform_mutate(cls, form, info):
        form.save(info.context)
        return cls(errors=[], **form.cleaned_data)


class ResetPasswordKeyMutation(UmsFormMutation):
    class Meta:
        form_class = ResetPasswordKeyForm

    @classmethod
    @login_required
    def perform_mutate(cls, form, info):
        form.save(info.context)
        return cls(errors=[], **form.cleaned_data)
