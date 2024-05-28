from django.db import models
from django.db import models
import secrets
from authentications.models import User
from students.models import Student, StudentCampaign
from university.models import University

from .paystack import PayStack

# Create your models here.
class Donations(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    students = models.ForeignKey(StudentCampaign, blank=True, on_delete=models.CASCADE)
    student_university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='donation_student_university')
    ref = models.CharField(max_length=200)
    amount = models.PositiveIntegerField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self) -> str:
        return f"Donation: {self.amount}"
    
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(20)
            object_with_similar_ref = Donations.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref.upper()
        super().save(*args, **kwargs)
    
    def amount_value(self) -> int:
        return self.amount *100
    
    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False