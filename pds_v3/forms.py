from django.forms import ModelForm
from pds_v3.models import AppUser, PdSession
from django import forms
from simplemathcaptcha.fields import MathCaptchaField


class CaptchaForm(forms.Form):
    captcha = MathCaptchaField()


class AppUserForm(ModelForm):
    class Meta:
        module = AppUser
        fields = ['']


class PdSessionForm(ModelForm):
    class Meta:
        model = PdSession
        fields = ['name', 'description']



class UploadFileForm(forms.Form):
    audio_file = forms.FileField()
