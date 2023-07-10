from django.shortcuts import render, redirect 
from .registration_form import UserRegistrationForm
from .models import UserDetails
from django.contrib import messages
import re
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate, login



#user registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        uname = request.POST.get('username')
        if UserDetails.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists')
        else:
            if form.is_valid():
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                confirmpassword = form.cleaned_data['confirmpassword']

                # 1. Check if email already exists
                if UserDetails.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                # 2. Phone number validation
                elif not re.match(r'^[0-9]{10}$', phone):
                    messages.error(request, 'Invalid phone number')
                # 3. Check if username already exists and validate username format
                elif not re.match(r'^[A-Za-z]', username):
                    messages.error(request, 'Username must start with an alphabet')
                elif len(username) < 5:
                    messages.error(request, 'Username must contain at least 5 characters')
                # 4. Validate password and confirm password
                elif password != confirmpassword:
                    messages.error(request, 'Password does not match')
                elif len(password) < 5:
                    messages.error(request, 'Password must be at least 5 characters long')
                else:
                    try:
                        fullname = form.cleaned_data['fullname']
                        user = UserDetails.objects.create_user(fullname=fullname, email=email, phone=phone, username=username, password=password)
                        current_site = get_current_site(request)
                        mail_subject = "Please activate your account"
                        message = render_to_string("account/email_verify.html", {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': default_token_generator.make_token(user),
                        })
                        to_email = email
                        send_mail = EmailMessage(mail_subject, message, to=[to_email])
                        send_mail.send()
                        user.save()
                        return redirect('emailnotification')
                    except Exception as e:
                        messages.error(request, f"An error occurred during registration: {str(e)}")
            else:
                messages.error(request, "Invalid form data")
    else:
        form = UserRegistrationForm()
    return render(request, 'account/registration.html', {'form': form})



# email notification
def emailnotification(request):

    return render(request,'account/emailnotification.html')



#email activation
def activate(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = UserDetails.objects.get(pk=uid)
    try:
        if user is not None and default_token_generator.check_token(user, token):
            user.mail_activation=True
            user.save()
            messages.success(request, 'Account activated successfully you can now login')
            return redirect('login')
        else:
            messages.error(request, 'Invalid activation link')
    except :
        messages.error(request, 'Invalid activation link')
    return redirect('login')




# login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user.mail_activation == True:
            if user is not None:
                try:
                    login(request, user)
                    messages.success(request, 'Login successful')
                    return redirect('login')
                except Exception as e:
                    messages.error(request, f"An error occurred during login: {str(e)}")
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request,'you need to verify your email,by clicking the verification link')
    return render(request, 'account/login.html')


# forgot password first page for email
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = UserDetails.objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = "Password/username Reset"
            message = render_to_string("account/password_resetemail.html", {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()
            return render(request, 'account/emailnotification.html')
        except UserDetails.DoesNotExist:
            messages.error(request, 'Invalid email address')
    return render(request, 'account/forgotpassword.html')


# reset password
def resetpasswordorusername (request, uidb64, token):
    if request.method=='POST':
        newvalue=request.POST['password']
        confirmnewvalue=request.POST['confirmpassword']
        drop_down = request.POST['dropdown']
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserDetails.objects.get(pk=uid)
        try:
            if user is not None and default_token_generator.check_token(user, token):
                if drop_down == 'username':
                    user.username = newvalue
                    user.save()
                    return redirect('emailnotification')
                elif drop_down == 'password':
                    if newvalue == confirmnewvalue and len(newvalue)>4:
                        user.mail_activation=True
                        user.set_password(newvalue)
                        user.save()
                        messages.success(request, 'Password changed successfully')
                        return redirect('emailnotification')
                    else:
                        if newvalue != confirmnewvalue:
                            messages.error(request,'password not matching')
                        else:
                            messages.error(request,'password length must atleast 5 characters')
                else:
                    messages.error(request,'Select an option username or password')

            else:
                messages.error(request, 'Invalid activation link')
        except :
            messages.error(request, 'Invalid activation link')
    return render(request,'account/resetpassword.html')

# Create your views here.
