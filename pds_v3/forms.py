from django.forms import ModelForm
from pds_v3.models import AppUser, PdSession
from django import forms
from simplemathcaptcha.fields import MathCaptchaField


class CaptchaForm(forms.Form):
    captcha = MathCaptchaField()


class PdSessionForm(ModelForm):
    class Meta:
        model = PdSession
        fields = ['name', 'description']
