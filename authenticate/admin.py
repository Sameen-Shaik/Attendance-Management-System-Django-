from django.contrib import admin
from .models import MyUser, Student, Faculty

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'user_type', 'joined')
    search_fields = ('username', 'email', 'name')
    list_filter = ('user_type', 'department')

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Faculty)
admin.site.register(Student)
