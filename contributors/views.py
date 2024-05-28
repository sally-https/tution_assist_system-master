from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from authentications.views import check_role_contributor
# from accounts.forms import UserInfoForm, UserProfileForm
from .models import Contributor
from .forms import ContributorsForm
from django.contrib import messages


# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_contributor)
def contributorDashboard(request):
    return render(request, 'contributors/contributorDashboard.html')



@login_required(login_url='login')
@user_passes_test(check_role_contributor)
def contributorProfile(request):
    contributor = get_object_or_404(Contributor, user=request.user)
    if request.method == 'POST':
        c_form = ContributorsForm(request.POST, request.FILES, instance=contributor)
        if c_form.is_valid():
            c_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('contributorProfile')
        else:
            print(c_form.errors)
            print(c_form.errors)
            messages.error(request, c_form.errors)
    else:
        c_form = ContributorsForm(instance=contributor)

    context = {
        'c_form': c_form,
        'contributor': contributor,
    }
    return render(request, 'contributors/contributorProfile.html', context)
