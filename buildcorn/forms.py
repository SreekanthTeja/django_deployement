from django import forms
from buildcorn.models import *
class CheckListCreateForm(forms.ModelForm):
    class Meta:
        model = CheckList
        fields = "__all__"