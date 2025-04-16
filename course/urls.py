from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.CourseListView.as_view(),name='course_list'),
    path('add/',views.TeacherCourseCreateView.as_view(),name='course_create'),
    path('<int:pk>/',views.CourseDetailView.as_view(),name='course_detail'),
    
    path('delete/<int:pk>',views.CourseDeleteView.as_view(),name='course_delete'),
    path('update/<int:pk>',views.CourseUpdateView.as_view(),name='course_change'),
]

htmx_urlpatterns =[
    path('search-course/',views.search_course,name='search-course'),
]

urlpatterns += htmx_urlpatterns