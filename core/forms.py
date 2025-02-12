from django import forms
from .models import Student, Enrollment

BOOTSTRAP_FIELD_CLASSNAME = "form-control w-full px-3 py-2 border border-gray-300 rounded-md"

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': BOOTSTRAP_FIELD_CLASSNAME,
                'placeholder': 'Enter student name'
            }),
            'email': forms.EmailInput(attrs={
                'class': BOOTSTRAP_FIELD_CLASSNAME,
                'placeholder': 'Enter email address'
            })
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']
        widgets = {
            'course': forms.Select(attrs={
                'class': BOOTSTRAP_FIELD_CLASSNAME,
            })
        }
