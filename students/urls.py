from django.urls import path, include
from . import views


urlpatterns = [
    path('studentDashboard/', views.studentDashboard, name='studentDashboard'),
    path('studentProfile/', views.studentProfile, name='studentProfile'),
    path('studentEditProfile/', views.studentEditProfile, name='studentEditProfile'),
    path('studentCampaign/', views.studentCampaign, name='studentCampaign'),
    path('studentCreateCampaign/', views.studentCreateCampaign, name='studentCreateCampaign'),
]