from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.CourseListView.as_view(),name='course_list'),
    path('add/',views.TeacherCourseCreateView.as_view(),name='course_create'),
    path('<int:pk>/',views.CourseDetailView.as_view(),name='course_detail'),
]