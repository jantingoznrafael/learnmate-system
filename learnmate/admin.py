from django.contrib import admin
from django.contrib.auth.models import Group

# Unregister Group model to hide it from admin
admin.site.unregister(Group)

admin.site.site_header = 'LearnMate Administration'
admin.site.site_title = 'LearnMate Admin'
admin.site.index_title = 'Welcome to LearnMate Administration'

