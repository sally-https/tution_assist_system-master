from django.urls import path, include
from . import views


urlpatterns = [
    path('Dashboard/', views.UniversityDashboard, name='universityDashboard'),
    path('profile/', views.universityProfile, name='universityProfile'),
    path('add-students/', views.universityAddStudent, name='universityAddStudents'),
    path('students/', views.universityAllStudent, name='universityStudents'),
    path('donations/', views.universityDonations, name='universityDonations'),
    path('students-campaign/', views.UniversityStudentsCampaign, name='universityStudentCampaign'),
    
    path('students-awaiting-approval/', views.students_awaiting_approval, name='students-awaiting-approval'),
    path("students-awaiting-approval/detail/<int:student_id>", views.students_awaiting_approval_details, name='students-awaiting-approval-detail'),
    path("approve-student/<int:student_id>", views.approval_student, name='approval-student'),
    path('campaign-awaiting-approval/', views.students_campaign_awaiting_approval, name='campaign-awaiting-approval'),
    path("approve-campaign/<int:campaign_id>", views.approve_campaign, name='approve-campaign'),
    
    path("student/detail/<int:student_id>/", views.universityViewStudent, name='student_detail'),
    path("student/delete/<int:student_id>/", views.universityDeleteStudent, name='delete_student'),
    path('add-campaign/<int:student_id>/', views.UniversityAddStudentsCampaign, name='add-student-campaign'),
    path("student/edit/<int:id>", views.edit_student, name='edit_student'),
]