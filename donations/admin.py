from django.contrib import admin
from .models import Donations

# Register your models here.
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'students', 'ref', 'amount', 'verified', 'created_at')
    list_display_links = ('students', 'user')
    




    
admin.site.register(Donations, DonationAdmin)