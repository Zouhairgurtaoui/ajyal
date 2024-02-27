

from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('<str:username>/profile',views.profile,name='user_profile'),
    path('students/',views.StudentListView.as_view(),name='student_list'),
    path('edit/profile/',views.edit_profile,name='edit_profile'),
    
]