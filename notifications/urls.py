from django.urls import path,include
from . import views

urlpatterns = [
    path('change-stat/<int:pk>/',views.change_stat,name='change-stat'),
    path('create/',views.NotificationCreateView.as_view(),name='notification_create')
]
