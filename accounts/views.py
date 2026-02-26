from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, UpdateProfileForm
from django.contrib.auth import authenticate, login, logout
from accounts.models import OTP, CustomUser
from django.utils import timezone
# from orders.models import Order
from datetime import timedelta
# Create your views here.
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import logging


def send_otp_email(recipient_email, otp_code):
    """
    Sends OTP email using only HTML template.
    """
    subject = "Your OTP Code — My Ecom Site"
    from_email = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER
    context = {
        'otp': otp_code,
        'site_name': 'My Ecom Site',
        'expiry_minutes': 3,
    }

    html_content = render_to_string('emails/otp_mail.html', context)

    try:
        msg = EmailMessage(subject, html_content, from_email, [recipient_email])
        msg.content_subtype = "html"  
        msg.send(fail_silently=False)
        # logger.info("OTP email sent to %s", recipient_email)
        return True
    except Exception as e:
        print("Mail didn't sent")
        # logger.exception("Failed to send OTP email to %s: %s", recipient_email, e)
        return False

def register_view(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print("valid check")
        print(form)
        
        if form.is_valid():
            print('form is valid')
            user = form.save(commit=False)
            print(form.cleaned_data)
            user.username = user.email
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()
            print("user created")

            # generate otp code over here
            otp_code = OTP.generate_otp()
            otp_expiry = timezone.now()+timedelta(minutes=3)
            OTP.objects.create(user=user, code=otp_code, expiry_time = otp_expiry)
            request.session['email'] = user.email

            send_otp_email(user.email, otp_code)
            


            return redirect('accounts:verify_otp')
        else:
            print('form is not valid')
            print(form.errors)
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form':form})



def home_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'accounts/home.html',{'user':request.user})

def verify_otp_view(request):
    
    email = request.session.get('email')
    print(request.session)
    if not email:
        return redirect('accounts:register')
    
    user = CustomUser.objects.get(email = email)
    if request.method=='POST':
        print("here")
        code = request.POST.get('otp')
        print(code)
        try:
            otp_obj = OTP.objects.filter(user=user, code=code).latest('created_at')
            if otp_obj.is_expired():
                message = 'OTP is expired'
            else:
                
                user.is_active = True
                user.save()
                return redirect('accounts:login')
        except OTP.DoesNotExist:
            message = 'Invalid OTP'
        return render(request, 'accounts/verify_otp.html',{'message':message})
    return render(request, 'accounts/verify_otp.html')



def login_view(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("here")
        print(email, password)
        user = authenticate(request, email = email, password=password)

      
        if user:
            print("logged in")
            login(request, user)
            return redirect('accounts:home_view')
    return render(request, 'accounts/login.html')

    

def logout_view(request):
    logout(request)
    return redirect('accounts:login')


# # @login_required
# def profile_view(request):
#     if request.method=='POST':
#         form = UpdateProfileForm(request.post, instance = request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('accounts:profile')
#     else:
#         form = UpdateProfileForm(instance=request.user)
    
#     orders = Order.objects.filter(user=request.user)


#     return render(request, 'accounts/profile.html',{
#         'form':form,
#         'orders':orders,
#     })