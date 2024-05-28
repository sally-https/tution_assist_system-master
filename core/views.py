from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from university.models import University
from authentications.models import User
from students.models import Student, StudentCampaign
from donations.forms import DonationForm
# from students.forms import AmountRaisedForm
from donations.models import Donations


def home(request):
    universities = University.objects.all().order_by('-created_at')[:6]
    students_campaign = StudentCampaign.objects.filter(is_approve=True, campaign_status="Ongoing")[:6]
    context = {
        'universities': universities,
        'students_campaign': students_campaign,
    }
    return render(request, 'frontend/home.html', context)



def aboutUs(request):
    return render(request, 'frontend/about.html')


def contactUs(request):
    return render(request, 'frontend/contactUs.html')


# @login_required(login_url='login')
def studentDetails(request: HttpRequest, id) -> HttpResponse:
    students_campaign = StudentCampaign.objects.filter(is_approve=True, campaign_status="Ongoing")
    student = get_object_or_404(students_campaign, id=id)

    # Calculate the ratio and percentage
    if student.financial_need > 0:
        ratio = student.amount_raised / student.financial_need
        percentage = ratio * 100
    else:
        ratio = 0
        percentage = 0

    amount_left = student.financial_need - student.amount_raised

    context = {
        'student': student,
        'amount_left': amount_left,
        'ratio': ratio,
        'percentage': percentage,
    }
    return render(request, 'frontend/campaignDetails.html', context)

def initiate_payment(request: HttpRequest, id) -> HttpResponse:
    if request.user.is_authenticated:
        students_campaign = StudentCampaign.objects.filter(is_approve=True, campaign_status="Ongoing")
        student = get_object_or_404(students_campaign, id=id)
        if request.method == "POST":
            donation_form = DonationForm(request.POST)
            if donation_form.is_valid():
                donation = donation_form.save(commit=False)
                donation.user = request.user
                donation.students = student
                donation.student_university = student.user.university
                donation.save()
                amm = donation.students.amount_raised
                mdd = donation.amount
                new = amm + mdd
                print(new)
                # StudentCampaign.objects.filter(pk=int(donation.students.id)).update(amount_raised=new)
                return render(request, 'frontend/make_payment.html', {'donation': donation, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
        else:
            donation_form = DonationForm()
    else:
        messages.info(request, "To make a Donation You must be Logged in! ")
        return redirect('two_factor:login')
        
    context = {
        'student': student,
        'donation_form': donation_form,
    }
    
    return render(request, 'frontend/initiate_payment.html', context)


def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    if request.user.is_authenticated:
        donation = get_object_or_404(Donations, ref=ref)
        verified = donation.verify_payment()

        if verified:
            StudentCampaign.objects.filter(pk=int(donation.students.id)).update(amount_raised=donation.amount)
            messages.success(request, "Payment Verification Successful")
        else:
            messages.error(request, "Payment Verification Failed")
        return redirect('myAccount')
    else:
        messages.info(request, "To make a Donation You must be Logged in! ")
        return redirect('two_factor:login')
    
    

def universityDetails(request: HttpRequest, id) -> HttpResponse:
    # university = University.objects.all().order_by('-created_at')[:6]
    # university = University.objects.filter(is_approve=True, campaign_status="Ongoing")
    university = get_object_or_404(University, id=id)
    students = StudentCampaign.objects.filter(is_approve=True, student_university=university)
    
    context = {
        'university': university,
        'students': students,
    }
    return render(request, 'frontend/universityDetails.html', context)
