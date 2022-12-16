from django.urls import path,re_path,include


from . import views
from polls.forms import TypeForm, EmailForm, BasicForm
from polls.views import FormWizard
from .views import HomeView, ArticleView,UpdatePostView,DeletePostView
form_list = (
        ('select_type', TypeForm),
        ('emailbasic', BasicForm),
        ('emailform',EmailForm)
    )

contact_wizard = FormWizard.as_view(form_list)

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', HomeView.as_view(), name='home'),
    # path('data/<int:pk>',views.indexdataedit, name='detail'),
    path('data/<int:pk>',ArticleView.as_view(), name='detail'),
    path('data/', views.indexdata, name='indexdata'),
    path('data/edit/<int:pk>',UpdatePostView.as_view(), name='update_post'),
    path('data/<int:pk>/remove',DeletePostView.as_view(), name='delete_post')
    # path('form/', FormWizard.as_view([TypeForm, BasicForm])),
    # path('data/checkschedule/',views.checkschedule, name='indexsch')
]