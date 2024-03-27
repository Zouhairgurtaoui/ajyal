

from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('<str:username>/profile',views.profile,name='user_profile'),
    path('students/',views.StudentListView.as_view(),name='student_list'),
    path('edit/profile/',views.edit_profile,name='edit_profile'),
    path('contact/',views.contact,name='contact_us')
    
]

htmx_urlpatterns =[
    path('search-student/',views.search_student,name='search-student'),
]

urlpatterns += htmx_urlpatterns