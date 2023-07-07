from django.shortcuts import render, redirect , get_object_or_404
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


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        mail = request.POST.get('email', '')
        if UserDetails.objects.filter(email=mail).exists():
            messages.error(request, 'email already exists')
        else:
            if form.is_valid():
                fullname = form.cleaned_data['fullname']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                confirmpassword = form.cleaned_data['confirmpassword']

                if len(username)>=5:
                    if password == confirmpassword: 
                        if re.match(r'^[A-Za-z]', username):
                            user= UserDetails.objects.create_user(fullname=fullname,email=email,phone=phone,username=username,password=password)
                            user.save()
                            messages.success(request,'Registration successfull ')

                            # User verification through mail
                            # current_site = get_current_site(request)
                            # mail_subject = "Please activate your account"
                            # message = render_to_string("account/email_verify.html",{
                            #     'user': user,
                            #     'domain': current_site,
                            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            #     'token': default_token_generator.make_token(user),
                            # })
                            # to_mail = email
                            # send_mail = EmailMessage(mail_subject,message,to=[to_mail])
                            # send_mail.send()
                            # messages.success(request,'Please verify your email ')
                            return redirect('login')  # Redirect to the login
                        else:
                            messages.error(request,"Username must start with alphabet")
                    else:
                        messages.error(request,'Password not maching')
                else:
                    messages.error(request,"Username must contain atleast 5 characters")

            else:

                username = request.POST.get('username', '')
                if UserDetails.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists')

    else:
        form = UserRegistrationForm()
    return render(request, 'account/registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # if user is None:
        #     print(username)
        #     user = authenticate(request, email=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('login')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request,'account/login.html')


# Create your views here.
