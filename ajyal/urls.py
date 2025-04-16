"""
URL configuration for ajyal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings

from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import forms as user_forms, views

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',include('users.urls')),
    path('quiz/',include('quiz.urls')),
    path('course/',include('course.urls')),
    path('notifications/',include('notifications.urls')),
    path('login/',auth_views.LoginView.as_view(template_name='login.html',authentication_form=user_forms.UserLoginForm),name='user-login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='user-logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html',form_class=user_forms.UserSetPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('store_reading_time/<int:pk>/',views.store_reading_time,name='time_reading'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
