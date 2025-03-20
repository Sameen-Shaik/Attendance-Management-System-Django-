# forms.py
from django import forms
from .models import Attendance, Student

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'status']

    def __init__(self, *args, **kwargs):
        session = kwargs.pop('session', None)
        super().__init__(*args, **kwargs)
        if session:
            self.fields['student'].queryset = session.course_batch.students.all()