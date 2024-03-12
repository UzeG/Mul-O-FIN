from web import models
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from web.utils.bootstrap import BootStrapForm, BootStrapModelForm, SelectModelForm


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label='Code',
        widget=forms.TextInput,
        required=True
    )


class RegisterModelForm(BootStrapForm):

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput,
        required=True
    )

    email = forms.CharField(
        label='Email',
        widget=forms.TextInput,
        required=True
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    confirm_password = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput,
        required=True
        # widget = forms.PasswordInput(render_value=True) 密码输入错误后不置空
    )

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd:
            raise ValidationError('Password is inconsistent.')
        # 返回什么，此字段以后保存到数据库就是什么
        return confirm


class ChangeProfileForm(forms.Form):
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput,
        required=True
    )


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput
    )
    new_password = forms.CharField(
        label='New password',
        widget=forms.PasswordInput
    )
    confirm_new_password = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput
    )

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if confirm_new_password != new_password:
            raise ValidationError('Passwords do not match.')
        return confirm_new_password


class OdorModelForm(BootStrapModelForm):
    class Meta:
        model = models.Odor
        fields = '__all__'


# class OdorSelectionModelForm(BootStrapModelForm):
#     class Meta:
#         model = models.OdorSelection
#         fields = '__all__'


class TemplateModelForm(BootStrapModelForm):
    class Meta:
        model = models.Template
        exclude = ['uuid']
        # fields = '__all__'


class RoleModelForm(BootStrapModelForm):
    class Meta:
        model = models.Role
        fields = '__all__'


class RoleSelectionModelForm(BootStrapModelForm):
    class Meta:
        model = models.RoleSelection
        fields = '__all__'


class DeviceModelForm(BootStrapModelForm):
    class Meta:
        model = models.Device
        fields = '__all__'


class EventOdorModelForm(BootStrapModelForm):
    class Meta:
        model = models.EventOdorModel
        fields = '__all__'
