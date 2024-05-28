from django.db import models
from authentications.models import User
from datetime import date

# Create your models here.
class Contributor(models.Model):
    user = models.OneToOneField(User, related_name='contributor_user', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='Student/profile_pictures', blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = 'Contributor'
        verbose_name_plural = 'Contributors'
    

    def __str__(self):
        return self.user.email
