from django import forms
from .models import Contributor
# from authentications.validators import allow_only_images_validator
from university.models import University


class ContributorsForm(forms.ModelForm):
    class Meta:
        model = Contributor
        fields = ['full_name', 'profile_picture', 'phone_number']
    
    def __init__(self, *args, **kwargs):
        super(ContributorsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

