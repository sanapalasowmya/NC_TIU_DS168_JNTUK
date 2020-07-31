from django.contrib import admin
from .models import *
# Register your models here.

admin.site.index_title = "Welcome to the FeePay Admin area"
admin.site.site_header = "FeePay Admin "
admin.site.site_title = "FeePay Admin Area"


class StudentInline(admin.TabularInline):
    model = Student
    extra = 5


class ClassAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['name', 'academicfee']})]
    inlines = [StudentInline]


admin.site.register(Class, ClassAdmin)