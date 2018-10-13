from django import forms

from .models import *


class MarkListForm(forms.ModelForm):
    class Meta:
        model = MarkList
        fields = ('semester','description', 'document', )
