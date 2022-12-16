from django import forms
from datetime import datetime
from django.urls import reverse_lazy,reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from django.forms import ModelForm, Form
from django_jsonform.models.fields import JSONField
import json
from polls.models import EmailJson,TypeEmail,BasicEmail,DataEmail

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

CHOICES=[('email_basic','email basic'),
         ('email_data','email data'),
         ('dataset','dataset'),
         ('connection','connect')]

class TypeForm(forms.ModelForm):
    # emailtype = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = TypeEmail
        fields = "__all__"

class BasicForm(forms.ModelForm):
    class Meta:
        model = BasicEmail
        fields = "__all__"

class DataForm(forms.ModelForm):
    class Meta:
        model = DataEmail
        fields = "__all__"
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'

class EditDataForm(forms.ModelForm):
    class Meta:
        model = DataEmail
        fields = "__all__"
    helper = FormHelper()
    helper.add_input(Submit('update', 'Update', css_class='btn-primary'))
    helper.form_method = 'POST'

class DeleteDataForm(forms.ModelForm):
    class Meta:
        model = DataEmail
        fields = "__all__"
    helper = FormHelper()
    helper.add_input(Submit('delete', 'DELETE', css_class='btn-danger'))
    helper.form_method = 'POST'
