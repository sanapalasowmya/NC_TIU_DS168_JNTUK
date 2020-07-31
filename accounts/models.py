from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.


class Class(models.Model):
    name = models.CharField(max_length=200)
    academicfee = models.FloatField(default=100000)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    stuclass = models.ForeignKey(Class, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=True)
    fathersname = models.CharField(max_length=150, null=True)
    mothersname = models.CharField(max_length=150, null=True)
    dob = models.DateField(null=True)
    dateofadmission = models.DateField(null=True)
    course = models.CharField(max_length=150, null=True)
    subject = models.CharField(max_length=150, null=True)
    roll = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=100, null=True)
    fee_paid = models.FloatField(default=0, max_length=10, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)
