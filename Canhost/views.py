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
            return redirect('Canhost:student_profile')
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
                print('Warden')
                if user.is_active:
                    print('Login')
                    login(request,user)
                    return redirect('Canhost:warden_home')

            else:
                if user.is_active:
                    print("Stident login")
                    login(request,user)
                    return redirect("Canhost:student_profile")

        else:
            print('Student disabled')
            context = 'Disabled acc contact Your warden or Admin'


    return render(request,'Login.html',{'message':context})




def warden_homepage(request):
    return render(request,'warden_home.html')


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
            return render(request, 'Student_profile.html', {'student': student, 'leaves': leaves})
        else:
            return HttpResponse('Disabled account')
    else:
        return HttpResponse('Invalid Login')



def select(request):
    if request.method == 'POST':
        if request.user.student.room:
            room_id_old = request.user.student.room_id

        if not request.user.student.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
        form = SelectionForm(request.POST, instance=request.user.student)
        if form.is_valid():
            if request.user.student.room_id:
                # stud = form.save(commit=False)
                # print(request.user.student.room_id, stud.room_id)
                request.user.student.room_allotted = True
                r_id_after = request.user.student.room_id
                room = Room.objects.get(id=r_id_after)
                room.vacant = False
                room.save()
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            else:
                request.user.student.room_allotted = False
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            student  = form.save()
            print(student.room_id)
            student = request.user.student
            leaves = Leave.objects.filter(student=request.user.student)
            return render(request, 'profile.html', {'student': student, 'leaves': leaves})
    else:
        if not request.user.student.no_dues:
            return HttpResponse('You have dues. Please contact your Hostel Caretaker or Warden')
        form = SelectionForm(instance=request.user.student)
        student_gender = request.user.student.gender
        if student_room_type == 'B':
            # print(student_room_type)
            # for i in range(len(hostel)):
            #     h_id = hostel[i].id
            x = Room.objects.filter(
                hostel__id=hostel, room_type=['S','D'], vacant=True).order_by('no')

            # x = x | a
        else:
            # for i in range(len(hostel)):
            #     h_id = hostel[i].id
            x = Room.objects.filter(
                hostel_id__in=hostel, room_type=student_room_type, vacant=True).order_by('hostel_id','no')
            print(x)
            # x = x | a
        form.fields["room"].queryset = x
        print('x',x)
        return render(request, 'select_room.html', {'form': form})



def leave(request):
    pass


def maintainence(request):
    pass

