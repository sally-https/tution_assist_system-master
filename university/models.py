from django.db import models
from django.utils.safestring import mark_safe
from PIL import Image
from authentications.models import User

# Create your models here.
class University(models.Model):
    user = models.OneToOneField(User, related_name='university', on_delete=models.CASCADE)
    university_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    about = models.TextField()
    university_logo = models.ImageField(upload_to='university/logos')
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    account_number = models.IntegerField()
    account_name = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)
    slug = models.SlugField(default="", null=False)
    is_approve = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'
        
    def thumbnail(self):
        return mark_safe("<img src='%s' width='50' height='50' style='object-fit: cover; border-radius: 6px' />" % (self.university_logo.url))
    
    def save(self):
        super().save()

        img = Image.open(self.university_logo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.university_logo.path)
        
        # input_path = img
        # # output_path = 'output.png'
        # input = Image.open(input_path)
        # output = remove(input)
        # output.save(self.university_logo.path)
    
        
    def __str__(self):
        return self.university_name