from django.urls import path
from .views import *


app_name = 'Canhost'

urlpatterns = [
    path('',homepage,name='homepage'),
    path('signup/',student_registration,name='signup'),
    path('warden_login/',warden_login,name='warden_login'),
    path('Student_login/',student_login,name='student_login'),
    path('logout/',user_logout,name='logout'),
    path('student_profile/',student_profile,name='student_profile'),
    path('after_reg/',student_after_registration,name='after_reg'),
    path('leave/',leave,name='leave'),
    path('Room_maintenence/',maintainence,name='Room_maintenence'),

]
