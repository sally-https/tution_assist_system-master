from django import forms
from .models import Donations


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donations
        fields = ("amount",)


 