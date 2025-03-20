from django.contrib import admin
from . models import Session, CourseBatch, Course, Attendance


class CourseBatchAdmin(admin.ModelAdmin):
    filter_horizontal = ('students', 'faculty')  

# Register your models here.

admin.site.register(Session)
admin.site.register(Course)
admin.site.register(CourseBatch, CourseBatchAdmin)
admin.site.register(Attendance)