from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import DateInput


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'dob': DateInput(attrs={'type': 'date'}),
            'dateofadmission': DateInput(attrs={'type': 'date'})
        }


class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = '__all__'


class StudentFormForStudent(ModelForm):
    class Meta:
        model = Student
        fields = ['stuclass', 'name', 'fathersname', 'mothersname', 'dob', 'dateofadmission', 'course', 'subject', 'roll', 'phone']
        widgets = {
            'dob': DateInput(attrs={'type': 'date'}),
            'dateofadmission': DateInput(attrs={'type': 'date'})
        }