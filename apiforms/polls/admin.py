from django.contrib import admin

# Register your models here.
from polls.models import EmailJson,DataEmail

admin.site.register(EmailJson)
admin.site.register(DataEmail)

