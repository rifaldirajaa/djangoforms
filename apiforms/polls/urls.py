from django.urls import path,re_path


from . import views
from polls.forms import TypeForm, EmailForm, BasicForm
from polls.views import FormWizard
form_list = (
        ('select_type', TypeForm),
        ('emailbasic', BasicForm),
        ('emailform',EmailForm)
    )

contact_wizard = FormWizard.as_view(form_list)

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^data/$', views.indexdata, name='index'),
    re_path(r'^form/$', FormWizard.as_view([TypeForm, BasicForm])),
    # re_path(r'^form/(?P<step>.+)/$', contact_wizard),
    # path('form/', contact_wizard),
]