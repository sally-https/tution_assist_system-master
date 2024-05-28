from django.db import models
from django.utils.safestring import mark_safe
from PIL import Image
from authentications.models import User
from university.models import University
from django.utils import timezone
from datetime import date

# Create your models here.
class Student(models.Model):
    GENDER = [
        ("Male", "Male"),
        ("Female", "Female")
    ]
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    student_id = models.CharField(max_length=50)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='student_university_id')
    full_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(default='default.png', upload_to='Student/profile_pictures', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    phone_number = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    
    def thumbnail(self):
        return mark_safe("<img src='%s' width='50' height='50' style='object-fit: cover; border-radius: 6px' />" % (self.profile_picture.url))
    
    
    
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return self.user.email



class StudentCampaign(models.Model):
    CAMPAIGN_STATUS = (
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(Student, related_name='campaign_student', on_delete=models.CASCADE)
    student_credentials = models.ImageField(upload_to='student/credentials')
    student_university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='campaign_student_university')    
    financial_need = models.DecimalField(max_digits=10, decimal_places=2)
    amount_raised = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    amount_left = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    campaign_message = models.TextField()
    campaign_status = models.CharField(max_length=15, choices=CAMPAIGN_STATUS, default='Ongoing')
    payment_deadline = models.DateField()
    is_approve = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Student Campaign'
        verbose_name_plural = 'Student Campaigns'
        
    # Add helper function for Admin display 
    def full_name(self):
        return f'{self.user.full_name}'
    
    @property
    def days_remaining(self):
        today = date.today()
        remaining = self.payment_deadline.date() - today
        return remaining
    

    def __str__(self):
        return f'{self.user.full_name}'
    