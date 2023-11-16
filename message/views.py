
from typing import Any
import requests
from django.shortcuts import render
from django.core.mail import send_mail

from django.http import HttpResponseRedirect

from django.http import HttpResponse
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect, HttpResponse
from ipaddress import IPv4Address
from pyairmore.request import AirmoreSession
from pyairmore.services.messaging import MessagingService
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.cache import cache_control
from .forms import RegistrationForm,UserLoginForm,PaymentForm
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login,logout
from .token import account_activation_token
from django.urls import reverse
from django.core.mail import EmailMessage
from .models import Profile,SentMessage,Member,Created_Group
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import pandas as pd
from django.shortcuts import get_object_or_404
import matplotlib.pyplot as plt
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.db.models import Count
from .models import UserProfile
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from social_django.models import UserSocialAuth
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from sendsms.config import EMAIL_HOST_USER
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
import paramiko
from datetime import datetime

from bs4 import BeautifulSoup

from django.contrib import messages
from social_django.utils import psa
import time
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
# import airmore.common.utils as airmoreutils
from .forms import ContactForm
from django.contrib.auth.models import Permission
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json   
import random
import string

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt
from .forms import PaymentForm
from django.contrib.auth.models import Group
def index(request):
    return render(request, "message/index.html")
@login_required(login_url='/login/')
def home(request):
    return render(request, "message/home.html")

def connect(request):
    if request.method == 'POST':
        ip_address = request.POST['ip']
        # ip = airmoreutils.IPv4Address(ip_address)
        ip = IPv4Address(ip_address)
        session = AirmoreSession(ip)
        was_accepted = session.request_authorization()
        if was_accepted:
            request.session['ip_address'] = ip_address
            # messages("Connected Successfully!")
            
            messages.add_message(request, messages.SUCCESS, 'connected successfully!')
            service = MessagingService(session)
            template_name='message/formpage.html'

            def sendSms(telephone, message,group_name):
               service.send_message(telephone, message,group_name)
               

            return render(request,template_name,{'ip_address':ip_address})
            # return redirect('home')
        else:
            return HttpResponse("Not connected!")
    else:
        return render(request, 'message/home.html')
# from .models import Group 
@login_required(login_url='/login/')
def send(request):
    if request.method == 'POST':
        ip_address = request.session.get('ip_address')
        
        group_name=request.POST.get('group_name')
        try:
            group = Created_Group.objects.get(group_name=group_name)
        except Group.DoesNotExist:
            # return HttpResponse("Group not found")
            messages.error(request, "Group not found")
            return render(request, 'message/formpage.html')
        if group.user != request.user:
            # return HttpResponse("You can only send messages to the groups you created")
            messages.error(request, "You can only send messages to the groups you created")
            return render(request, 'message/formpage.html')

        
        topic = request.POST.get("topic")
        meet = request.POST.get("meetlink")
        when = request.POST.get("time")
        aspace = request.POST.get("aspace")
        message = request.POST.get("message")
        sign = request.POST.get("sign")
        message_with_info = str(request.POST["message"]) + "\n" + str(topic) + "\ntime: " + str(when) + "\nmeet: " + str(
             meet) + "\n" + str(sign) + "\n" + str(aspace) 

        if not topic or not group_name or not message:
            # return HttpResponse("failure")
            messages.error(request, "Your message is failed to send there are parts left from required contents")
            return render(request, 'message/formpage.html')
        else:
            
            uniqlist = []

            ip = IPv4Address(ip_address)
            session = AirmoreSession(ip)
            service = MessagingService(session)
            
            def sendsms(telephone, message, group_name):
                service.send_message(telephone, message)

            def namesep(firstname):
                return firstname.split(" ")[0]

            def format(phone):
                cln = phone.replace(" ", "").replace("-", "")
                if cln.startswith("251"):
                    return "+" + cln
                elif cln.startswith("9"):
                    return "0" + cln
                else:
                    return cln

           
            group_members = Member.objects.filter(group_name=group)
            
            
            for member in group_members:
                msg_parts = []
                if topic:
                    msg_parts.append("topic:" + topic)
                if when:
                    msg_parts.append("time: " + when)
                if meet:
                    msg_parts.append("meeting link: " + meet)
                if sign:
                    msg_parts.append("sign: " + sign)
                if aspace:
                    msg_parts.append("aspace: " + aspace)
                if message:
                    msg_parts.append(message)

                msg = "hi " + namesep(member.name) + ",\n" + '\n'.join(msg_parts)
                # msg = "Hi " + namesep(member.name) + ",\n" + message_with_info
                number = str(member.phone_number)
                sendsms(number, msg, group_name)
                sentms = SentMessage.objects.create(message=msg,receiver_name=member.name, rec_phone_number=number)
                sentms.save()
                time.sleep(1)
          
            
            return render(request, "message/success.html", {'content': 'Send to: ' + ', '.join(uniqlist)})
            # return render(request, "message/success.html", {'content': 'Send to: ' + receiver_list})
    else:
        return render(request, 'message/home.html')



from django.contrib.auth.models import Group
def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                email = form.cleaned_data['email']
                
                
                # Save the form data to database (assuming contactform is a ModelForm)
                form.save()
                group=Group.objects.get(name="Customer")
                user.groups.add(group)
                # Student.objects.create(user=user)
                
                sender_email=EMAIL_HOST_USER
        
                sender_message = "Welcome to our page! You are successfully registered ."
                send_mail(
                    'Please perform payment to use messagelink',
                    sender_message,
                    sender_email,  
                    [email], 
                    fail_silently=False,
                )
                # return redirect('index')
                # return render(request,'message/index.html')
                return redirect(f"{reverse('index')}#pricing")
        else:
        
          form = RegistrationForm()
        # return render(request, 'message/Login_and_Register.html', {'form': form})
          messages.error(request,'There is some errors')
          return render(request,'message/registration.html', {'form': form})
        # return redirect(f"{reverse('login')}#go")
@login_required
@cache_control(max_age=3600)  # Set cache control to 1 hour
def deactivate_account(request):
    user = request.user
    # Deactivate user's account
    user.is_active = False
    user.save()
    # Logout user
    logout(request)
    return redirect('login')

def logins(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
       if request.method=="POST":
           username=request.POST.get('username')
           password=request.POST.get('password')
           try:
               user=User.objects.get(username=username)
    
           except:
            # print('Username does not exist!')
            
               messages.error(request, " username does not exist")
               return render(request,'message/Login_and_Register.html')

           authenticate(request,username=username,password=password)
           user = authenticate(request, username=username, password=password)
           if user is not None:
               login(request, user)
            # if request.user.is_authenticated and user:
               if user.is_authenticated and user.is_staff and user.is_superuser:
                   messages.success(request,'Authentication is successful')
                   return redirect('message_chart')
               elif user.is_authenticated:
                   return redirect('choice')
            # return render(request,'admin')
            
            # return redirect('/admin/')
               else:
                  return redirect('index')
             


            #   return HttpResponse("doesnot exist")
        
           else:
            
            # print('Username or password incorrect')
               messages.error(request, "Username or password incorrect")
            
               return render(request,'message/Login_and_Register.html')
       else:
        # messages.error(request, "Invalid Username or password.")
           f = UserLoginForm()
           return render(request = request,
                    template_name = "message/Login_and_Register.html",
                context={"f":f})
@login_required(login_url='/login/')   
def choice(request):
    return render(request,'message/choice.html')
@login_required(login_url='/login/')   
def profile(request):
    return render(request,'message/profile.html')



@login_required(login_url='/login/')
def chart_view(request):
    
    data = SentMessage.objects.annotate(date=TruncDate('sent_at')).values('date').annotate(count=Count('id'))
    dates = [d['date'].strftime('%y-%m-%d') for d in data]
    counts = [d['count'] for d in data]

    context = {
        'dates': dates,
        'counts': counts,
    }

    return render(request, 'message/chart.html', context)


@login_required(login_url='/login/')
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")
class CustomPasswordResetView(PasswordResetView):
    success_url = '/login/'

@login_required(login_url='/login/')
class SettingsView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            facebook_login = user.social_auth.get(provider='facebook')
        except UserSocialAuth.DoesNotExist:
            facebook_login = None

        can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

        return render(request, 'registration/settings.html', {
            
            'facebook_login': facebook_login,
            'can_disconnect': can_disconnect
        })


@login_required(login_url='/login/')
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {'form': form}) 
@psa('social:complete')
def auth(request, backend):
    user = request.backend.do_auth(request.GET.get('access_token'))
    if user:
        login(request, user)
    return redirect(request,'message/choice.html')


def Contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Save the form data to database (assuming contactform is a ModelForm)
            form.save()

            # Send email to receiver
            # receiver_email = 'samimokehirpa@gmail.com'  # Replace with the receiver's email address
            receiver_email=EMAIL_HOST_USER
            send_mail(
                'Contact Form Submission from {}'.format(name),
                message,
                email,  # Sender's email
                [receiver_email],
                fail_silently=False,
            )

            # Send a reply email to the sender
            sender_message = "Welcome to our page! We will contact you soon."
            send_mail(
                'Thank you for contacting us',
                sender_message,
                receiver_email,  # Replace with your own email address
                [email],  # Sender's email
                fail_silently=False,
            )

            return render(request, 'message/thanks.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'message/index.html', {'form': form})
@login_required(login_url='/login/')
def admin_view(request):
    return render(request, 'admin/change.html')

@csrf_exempt
def chapa_webhook(request):
    # who knows what kind of request we are getting
    if request.method != 'POST':
        return JsonResponse(
            {
                'errors': 'only POST method allowed'
            },
            status=400,
        )

    try:
        data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse(
            {
                'error': "Invalid Json Body"
            },
            status=400
        )
    
    model = settings.CHAPA_TRANSACTION_MODEL
    # add your webhook events here and also you can override the model
    model.response_dump = data
    model.save()
    # TODO: this method should be class view for customization support
    return JsonResponse(data)

def generate_random_string(length): # Choose from uppercase letters and digits 
    characters = string.ascii_uppercase + string.digits # Use random.choices to select a list of characters randomly 
    random_list = random.choices(characters, k=length) # Join the list into a string and return it
    random_string = ''.join(random_list) 
    return random_string

from django.contrib.auth.models import Group
@csrf_exempt
def checkouts(request):
    # Handle payment request
    
    form=PaymentForm
    

    if request.method == 'POST':
        if form.is_valid():
        # Get the payment details from the form
           amount = request.POST['amount']
           currency = request.POST['currency']
           return_url = request.POST['return_url']
           cancel_url=request.POST['cancel_url']
           username=request.POST['username']
        #    tx_ref=request.Post['text_ref']
           tx_ref = generate_random_string(10)
           
    

        # Make a call to Chapa API to initiate the payment
           response = requests.post(
            'https://api.chapa.com/payments/create',
            json={
                'amount': amount,
                'currency': currency,
                'return_url': return_url,
                'cancel_url':cancel_url,
                'tx_ref':tx_ref,
                'username':username
                
                
                
               }
               )

        # Check if the payment request was successful
           if response.status_code == 200:
                # user=User.objects.get(username=username)
                # user = request.user
               
                # user.is_active = True
                # user.staff_status = True
                # user.save()
                # group=Group.objects.get(name="Customer")
                # user.groups.add(group)
            # Extract the payment URL from the response
            # payment_url = response.json()['checkout']
                 activation_url = f"https://gptgo.ai/activate?user={request.user}"  # Modify this with your own activation URL
                
                 email_subject = 'Activate your account'
                 email_body = f'Please click the following link to activate your account: {activation_url}'
                 email = EmailMessage(
                    email_subject,
                    email_body,
                    to=[request.user.email],  # Assuming the user model has an 'email' field
                   )
                 email.send()
                
                 return HttpResponse('Email sent! Please check your inbox to activate your account.')

            
                #  return render(request,'message/Login_and_Register.html')
    else:
    # Render the payment form
       return render(request, 'message/checkout.html')
    


@login_required
def logouts(request):
    if request.user.is_authenticated:
        last_activity = request.session.get('last_activity')
        if last_activity:
            time_since_last_activity = (timezone.now() - last_activity).seconds
            if time_since_last_activity > 600:
                logout(request)
                return redirect('index')
        request.session['last_activity'] = timezone.now()
    return render(request, 'index.html')
def delete_users():

    current_date = timezone.now()
    thirty_days_ago = current_date - timezone.timedelta(days=30)
    users_to_delete = User.objects.filter(date_joined__lt=thirty_days_ago).exclude(is_superuser=True)
    for user in users_to_delete:
        user.delete()

@csrf_exempt
def checkout(request):
    # form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            currency = form.cleaned_data['currency']
            return_url = form.cleaned_data['return_url']
            # cancel_url = form.cleaned_data['cancel_url']
            username = form.cleaned_data['username']
            email=form.cleaned_data['email']
            tx_ref = generate_random_string(10)
            
            # Make a call to chapa API to initiate the payment
            response = requests.post(
                'https://api.chapa.com/payments/create',
                json={
                    'amount': amount,
                    'currency': currency,
                    'return_url': return_url,
                    # 'cancel_url': cancel_url,
                    'tx_ref': tx_ref,
                    'username': username,
                    'email':email
                }
            )
            
            if response.status_code == 200:
                # Payment request was successful
                                
                # Generate activation token and send activation email
                user = User.objects.get(username=username)
                user.is_active = False  # Mark user as inactive until they activate their account
                user.save()
                
                # Get the current site domain
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                message = render_to_string(
                    'message/account_activation_email.html',
                    {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        'token': default_token_generator.make_token(user),
                    }
                )
                to_email = form.cleaned_data['email']  # Assuming you have an 'email' field in your form
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                
                return HttpResponse('successfully activate your accouont')
    
    # Render the payment form
    return render(request, 'message/checkout.html')

@csrf_exempt
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        # Activate user's account
        user.is_active = True
        user.save()
        
        return HttpResponse('successfully activate your accouont')
    
    else:
        
        return HttpResponse(' activate your accouont is failed')
def go(request):
    return render(request,'message/newform.html')
def fm(request):
    return render(request,'message/fm.html')
