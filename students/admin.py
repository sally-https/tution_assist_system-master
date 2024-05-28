from django.contrib import admin
from .models import Student, StudentCampaign

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'student_id', 'full_name', 'user', 'is_verified', 'created_at')
    list_display_links = ('full_name', 'user', 'student_id')
    list_editable = ('is_verified',)
    


class StudentCampaignAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_university','financial_need', 'campaign_status', 'payment_deadline')
    list_display_links = ('user', 'student_university','financial_need',)

    
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentCampaign, StudentCampaignAdmin)