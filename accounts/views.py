from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views.generic import View
from payfee.utils import render_to_pdf
from django.template import Context, loader
from django.http import HttpResponse
from django.urls import reverse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import StudentForm, ClassForm, CreateUserForm, StudentFormForStudent
from .filters import StudentFilter
from .decorators import admin_only
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

import stripe
stripe.api_key = "sk_test_51HB1wGGbmEw5gYBcjVBWu9yKTldsAVBH0uCIrKWzxngJ8kdN6ZsH8BPucb1t8EiadllDcjCOmYvn3kFZj8BUOuWd00fKG680vw"


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        student = request.user.student
        if student.stuclass is None:
            template = loader.get_template("accounts/warnmessage.html")
            return HttpResponse(template.render())
        feepaid = student.fee_paid
        if feepaid < request.user.student.stuclass.academicfee:
            template = loader.get_template("accounts/warnpayment.html")
            return HttpResponse(template.render())
        template = get_template('invoice.html')
        context = {
            "invoice_id": 123,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
            "student": request.user.student
        }
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "TC_%s.pdf" %("1")
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")



@login_required(login_url='login')
@admin_only
def home(request):
    classnames = Class.objects.all()
    context = {'classnames': classnames}
    return render(request, 'accounts/dashboard.html', context)


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='student')
            student = Student.objects.create(user=user)
            user.groups.add(group)
            student.stuclass = None
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect Username or Password')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def classDetails(request, pk):
    myfilter = StudentFilter()
    classDet = Class.objects.get(id=pk)
    students = classDet.student_set.all()
    if request.method == 'GET':
        myfilter = StudentFilter(request.GET, queryset=students)
        students = myfilter.qs
    context = {'students': students, 'filter': myfilter}
    return render(request, 'accounts/student_details.html', context)


@login_required(login_url='login')
def updateStudent(request, pk):
    student = Student.objects.get(id=pk)
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = StudentForm(instance=student)
    context = {'form': form}
    return render(request, 'accounts/details_update.html', context)


@login_required(login_url='login')
def updateStudentForStudent(request, pk):
    student = Student.objects.get(id=pk)
    form = StudentFormForStudent(instance=student)
    if request.method == 'POST':
        form = StudentFormForStudent(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/details_update.html', context)


@login_required(login_url='login')
def deleteStudent(request, pk):
    student = Student.objects.get(id=pk)
    user = student.user
    if request.method == 'POST':
        student.delete()
        user.delete()
        return redirect('/')
    context = {'student': student}
    return render(request, 'accounts/delete_student.html', context)


@login_required(login_url='login')
def studentPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
def createClass(request):
    form = ClassForm()
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'accounts/create_class.html', context)


@login_required(login_url='login')
def createUser(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create-student')
    context = {'form': form}
    return render(request, 'accounts/create_student_user.html', context)


@login_required(login_url='login')
def createStudent(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'accounts/create_student.html', context)


@login_required(login_url='login')
def deleteClass(request, pk):
    classname = Class.objects.get(id=pk)
    if request.method == 'POST':
        classname.delete()
        return redirect('home')
    context = {'classname': classname}
    return render(request, 'accounts/delete_class.html', context)


@login_required(login_url='login')
def updateClass(request, pk):
    classname = Class.objects.get(id=pk)
    form = ClassForm(instance=classname)
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            return redirect('home')
    context = {'classname': classname, 'form': form}
    return render(request, 'accounts/update_class.html', context)


@login_required(login_url='login')
def studentProfile(request, pk):
    student = Student.objects.get(id=pk)
    if student.stuclass is not None:
        diff = student.stuclass.academicfee - student.fee_paid
    else:
        diff = 0
    context = {'student': student, 'diff': diff}
    return render(request, 'accounts/student_profile.html', context)


@login_required(login_url='login')
def contactForm(request):
    if request.method == 'POST':
        message = request.POST['message']
        subject = request.POST['subject']
        send_mail(subject, message, settings.EMAIL_HOST_USER, ['testsihfee@gmail.com'], fail_silently=False)
        return redirect('home')
    return render(request, 'accounts/contactform.html')


@login_required(login_url='login')
def payfee(request):
    student = request.user.student
    if student is None or student.stuclass is None:
        template = loader.get_template("accounts/warnmessage.html")
        return HttpResponse(template.render())
    context = {}
    return render(request, 'accounts/feeform.html', context)


@login_required(login_url='login')
def charge(request):
    if request.method == 'POST':
        print('Data:', request.POST)
        description = request.POST['description']
        amount = int(request.POST['amount'])
        line1 = request.POST['line1']
        postal_code = request.POST['postal_code']
        city = request.POST['city']
        state = request.POST['state']

        customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['nickname'],
            address={
                'line1': line1,
                'postal_code': postal_code,
                'city': city,
                'state': state,
                'country': 'IN',
            },
            source=request.POST['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='inr',
            description=description
        )

    return redirect(reverse('success', args=[amount]))


@login_required(login_url='login')
def successMsg(request, args):
    amount = args
    student = request.user.student
    student.fee_paid = student.fee_paid + float(args)
    student.save()
    print(student.fee_paid)
    return render(request, 'accounts/success.html', {'amount': amount})

