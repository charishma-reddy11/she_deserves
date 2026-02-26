from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import logging

from accounts1.forms import RegistrationForm, UpdateProfileForm
from accounts1.models import OTP, CustomUser

def send_otp_email(recipient_email, otp_code):
    subject = "Your OTP Code — She Deserves"
    from_email = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER
    context = {
        'otp': otp_code,
        'site_name': 'She Deserves',
        'expiry_minutes': 3,
    }

    html_content = render_to_string('emails/otp_mail.html', context)

    try:
        msg = EmailMessage(subject, html_content, from_email, [recipient_email])
        msg.content_subtype = "html"
        msg.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Mail sending failed: {e}")
        return False

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()

            otp_code = OTP.generate_otp()
            otp_expiry = timezone.now() + timedelta(minutes=3)
            OTP.objects.create(user=user, code=otp_code, expiry_time=otp_expiry)
            request.session['email'] = user.email

            send_otp_email(user.email, otp_code)
            
            # 2. Redirect namespace updated
            return redirect('accounts1:verify_otp')
        else:
            print("Form Errors:", form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'accounts1/register.html', {'form': form})

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts1:login')
    return render(request, 'travel/home.html', {'user': request.user})

def verify_otp_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('accounts1:register')
    
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return redirect('accounts1:register')

    message = None
    if request.method == 'POST':
        code = request.POST.get('otp')
        try:
            otp_obj = OTP.objects.filter(user=user, code=code).latest('created_at')
            if otp_obj.is_expired():
                message = 'OTP is expired'
            else:
                user.is_active = True
                user.save()
                return redirect('accounts1:login')
        except OTP.DoesNotExist:
            message = 'Invalid OTP'
        
    return render(request, 'accounts1/verify_otp.html', {'message': message})
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('travel:home')
            else:
                return render(request, 'accounts1/login.html', {
                    'error': 'Account is not active. Please verify your OTP.'
                })
        else:
            return render(request, 'accounts1/login.html', {
                'error': 'Invalid email or password. Please try again.'
            })

    return render(request, 'accounts1/login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts1:login')