from django import forms

from . import models


class IOSRegisterForm(forms.ModelForm):

    class Meta:
        model = models.IOSDevice


class AndroidRegisterForm(forms.ModelForm):

    class Meta:
        model = models.AndroidDevice
