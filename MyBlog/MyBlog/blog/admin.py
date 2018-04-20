from django.contrib import admin

# Register your models here.
from .models import ckeditorBlog,MyPhoto,user_profile,studyNote

admin.site.register(ckeditorBlog)
admin.site.register(MyPhoto)
admin.site.register(user_profile)
admin.site.register(studyNote)