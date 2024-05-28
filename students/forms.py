from django import forms
from .models import Student, StudentCampaign
from authentications.validators import allow_only_images_validator
from university.models import University


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'full_name', 'university', 'profile_picture', 'gender', 'phone_number', 'address']
    
    def __init__(self, *args, **kwargs):
        super(StudentRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'full_name', 'profile_picture', 'gender', 'phone_number', 'address']
    
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DateInput(forms.DateInput):
    input_type = 'date'
    

class StudentCampaignForm(forms.ModelForm):
    student_credentials = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    # payment_deadline = forms.DateField(widget=forms.DateField())
    class Meta:
        model = StudentCampaign
        fields = ['student_credentials', 'financial_need', 'campaign_message', 'payment_deadline']
        widgets = {
            'payment_deadline': DateInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(StudentCampaignForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        
        self.fields['financial_need'].widget.attrs['placeholder'] = 'Amount Needed'
        # self.fields['payment_deadline'].widget.attrs['placeholder'] = 'Deadline Date'
        
        

      