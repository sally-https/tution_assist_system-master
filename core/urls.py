"""
URL configuration for core project.

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
from django.urls import path, include
from two_factor.urls import urlpatterns as tf_urls
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(tf_urls)),
    
    path('', views.home, name='home'),
    path('about/', views.aboutUs, name='about'),
    path('contact-us/', views.contactUs, name='contact-us'),
    path('<int:id>/', views.studentDetails, name='studentDetails'),
    path('university/<int:id>/', views.universityDetails, name='universityDetails'),
    
    path('initiate_payment/<int:id>/', views.initiate_payment, name='initiate_payment'),
    path('<str:ref>/', views.verify_payment, name='verify-payment'),
    
    
    path('accounts/', include('authentications.urls')),
    
    path('university/', include('university.urls')),
    path('contributor/', include('contributors.urls')),
    path('student/', include('students.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
