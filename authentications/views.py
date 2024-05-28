from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import User
from .forms import UserForm
from students.forms import StudentForm, StudentRegisterForm
from contributors.forms import ContributorsForm
from django.contrib.auth import login


# Restrict the vendor from accessing the customer page
def check_role_student(user):
    if user.user_type == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page
def check_role_contributor(user):
    if user.user_type == 2:
        return True
    else:
        raise PermissionDenied



def check_role_university(user):
    if user.user_type == 3:
        return True
    else:
        raise PermissionDenied



def registerStudent(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        s_form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid() and s_form.is_valid:
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.user_type = User.STUDENT
            user.is_active = True  # Set the user as active
            user.save()
            student = s_form.save(commit=False)
            student.user = user
            student_id = s_form.cleaned_data['student_id']
            full_name = s_form.cleaned_data['full_name']
            profile_picture = s_form.cleaned_data['profile_picture']
            gender = s_form.cleaned_data['gender']
            phone_number = s_form.cleaned_data['phone_number']
            address = s_form.cleaned_data['address']
            university = s_form.cleaned_data['university']
            student.save()

            # Automatically login the user after registration
            login(request, user)

            messages.success(request, 'Your account has been registered successfully!')
            return redirect('myAccount')
        else:
            print('invalid form')
            print(form.errors)
            messages.error(request, form.errors)
    else:
        form = UserForm()
        s_form = StudentRegisterForm()

    context = {
        'form': form,
        's_form': s_form,
    }

    return render(request, 'authentications/registerStudent.html', context)



    
# Create your views here.
def registerContributor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        c_form = ContributorsForm(request.POST)
        if form.is_valid() and c_form.is_valid():
            ######### Create the user using create_user method #########
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user.user_type = User.CONTRIBUTOR
            user.save()
            contributor = c_form.save(commit=False)
            contributor.user = user
            full_name = c_form.cleaned_data['full_name']
            profile_picture = c_form.cleaned_data['profile_picture']
            phone_number = c_form.cleaned_data['phone_number']
            contributor.save()

            messages.success(request, 'Your account has been registered successfully !')
            return redirect('two_factor:login')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        c_form = ContributorsForm()
    context = {
        'form': form,
        'c_form': c_form,
    }
    return render(request, 'authentications/registerContributor.html', context)





###################################################################
########################## LOGOUT FUNCTION #########################
###################################################################
def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('two_factor:login')



@login_required(login_url='two_factor:login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)




def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'authentications/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('two_factor:login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('two_factor:login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'authentications/reset_password.html')

