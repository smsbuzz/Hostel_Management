from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime,calendar
from django.core.exceptions import ObjectDoesNotExist


def homepage(request):
    return render(request,'index.html')


def student_registration(request):
    form = UserForm()
    context = ''
    if request.method=='POST':
        print('if')
        form = UserForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            new_user = form.save(commit=False)
            new_user.save()
            Student.objects.create(user=new_user)
            form = UserForm
            user = authenticate(
                request,
                username=data['username'],
                password=data['password1']
            )
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("Canhost:after_reg")
                else:
                    context = 'acc is in active'
            else:
                context = 'Disabled acc'

        else:
            print('else')
            form = UserForm()

    return render(request,'signup.html',{'form':form,'message':context})


@login_required
def student_after_registration(request):
    form = RegistrationForm()
    if request.method=='POST':
        form = RegistrationForm(data=request.POST,instance=request.user.student)
        if form.is_valid():
            form.save()
            return redirect('Canhost:room_select')
        else:
            form = RegistrationForm()
    else:
        form = RegistrationForm()
    return render(request,'after_reg.html',{'form':form})

def user_login(request):
    context = ''
    if request.method=='POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user = authenticate(request,username = username,password = password)
        if user is not None:
            if user.is_warden:
                if user.is_active:
                    login(request,user)
                    return redirect('Canhost:warden_home')

            else:
                if user.is_active:
                    login(request,user)
                    return redirect("Canhost:student_profile")

        else:
            context = 'Disabled acc contact Your warden or Admin'


    return render(request,'Login.html',{'message':context})



@login_required
def warden_homepage(request):
    user = request.user
    if user is not None:
        if  user.is_warden:
            login(request,user)
            room_list = user.warden.hostel.room_set.all().order_by('no')
            print(room_list)
        else:
            return HttpResponse("Invalid Login")

    return render(request,'warden_home.html',{'room':room_list})


def user_logout(request):
    logout(request)
    return render(request, 'index.html')


@login_required
def student_profile(request):
    user = request.user
    if user is not None:
        if user.is_warden:
            return HttpResponse('Invalid Login')
        if user.is_active:
            login(request, user)
            student = request.user.student
            leaves = Leave.objects.filter(student=request.user.student)
            print(request.user.student.room_allotted)
            print(request.user.student.no_dues)
            return render(request, 'Student_profile.html', {'student': student, 'leaves': leaves})

        else:
            return HttpResponse('Disabled account')
    else:
        return HttpResponse('Invalid Login')


@login_required
def select(request):
    form = SelectionForm()
    if request.method=='POST':
        if request.user.student.room:
            room_id_old = request.user.student.room_id
        if not request.user.student.no_dues:
            return HttpResponse("You Have dues contact Your Warden:)")
        form= SelectionForm(data=request.POST,instance=request.user.student)
        if form.is_valid():
            if request.user.student.room_id:
                request.user.student.room_allotted = True
                room_id_new = request.user.student.room_id
                room = Room.objects.get(id=room_id_new)
                room.vacant=False
                room.save()
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except:
                    pass
            else:
                request.user.student.room_allotted = False
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant=True
                    room.save()
                except :
                    pass
            student = form.save()
            student = request.user.student
            leaves = Leave.objects.filter(student=request.user.student)
            return render(request, 'Student_profile.html', {'student': student, 'leaves': leaves})
    return render(request,'room.html',{'form':form})




def leave(request):
    pass


def maintainence(request):
    pass

def Warden_add_room(request):
    pass

