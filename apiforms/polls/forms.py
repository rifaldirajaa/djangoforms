from django import forms
from datetime import datetime
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, Form
from django_jsonform.models.fields import JSONField
import json
from polls.models import EmailJson

class EmailForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('index')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit','Submit'))

    SUBJECT_CHOICES = (
        (1, 'Web'),
        (2, 'Programming'),
        (3, 'Data Engineering'),
    )
    TYPE_CHOICES = (
        (1, 'email_basic'),
        (2, 'email_data'),
        (3, 'dataset'),
    )


    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.RadioSelect()
    )
    receiver_email = forms.CharField()
    receiver_table = forms.CharField()
    
    subject_email = forms.CharField()
    body_email = forms.CharField()
    # date_of_birth = forms.DateField(
    #     widget=forms.DateInput(attrs={'type':'date', 'max':datetime.now().date()})
    # )

class JsonForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = EmailJson
        fields = "__all__"
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


