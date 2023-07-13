
from typing import Any
import requests
from django.shortcuts import render
from django.core.mail import send_mail

from django.http import HttpResponseRedirect


from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect, HttpResponse
from ipaddress import IPv4Address
from pyairmore.request import AirmoreSession
from pyairmore.services.messaging import MessagingService
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site

from .forms import RegistrationForm,UserLoginForm
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login,logout
from .token import account_activation_token
from django.urls import reverse
from django.core.mail import EmailMessage
from .models import Profile,SentMessage,Member,Group
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import pandas as pd
import matplotlib.pyplot as plt
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





from django.contrib import messages
from social_django.utils import psa
import time
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from .forms import ContactForm
from django.contrib.auth.models import Permission
   

def index(request):
    return render(request, "message/index.html")
@login_required(login_url='/login/')
def home(request):
    return render(request, "message/home.html")

def connect(request):
    if request.method == 'POST':
        ip_address = request.POST['ip']
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


def send(request):
    if request.method == 'POST':
        ip_address = request.session.get('ip_address')
        
        group_name=request.POST.get('group_name')
        try:
            group = Group.objects.get(group_name=group_name)
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

            # for i in txtfh.split('\n'):
                # if i in uniqlist:
                #     pass
                # else:
                #     uniqlist.append(namesep(i.split(",")[0]) + "," + format(i.split(",")[-1]))
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




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            
            user.save()
            # try:
            #    customer_group = Group.objects.get(group_name='Customer')
            # except Group.DoesNotExist:
            #     print('group not exist')
            # group = Group.objects.get(group_name='Customer')
            # group.user_set.add(user)
           
            return render(request,'message/index.html')  
    else:
        form = RegistrationForm()
    return render(request, 'message/registration.html', {'form': form})
def logins(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
    
        except:
             print('Username does not exist!')
           

        authenticate(request,username=username,password=password)

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # if request.user.is_authenticated and user:
            if user.is_authenticated and user.is_staff and user.is_superuser:
                return redirect('message_chart')
            elif user.is_authenticated:
                return redirect('choice')
            # return render(request,'admin')
            
            # return redirect('/admin/')
            else:
              return redirect('index')
        
        else:
            
            print('Username or password incorrect')
        
            return render(request,'registration/Login_and_Register.html')
    else:
        # messages.error(request, "Invalid Username or password.")
        f = UserLoginForm()
        return render(request = request,
                    template_name = "registration/Login_and_Register.html",
                context={"f":f})
@login_required    
def choice(request):
    return render(request,'message/choice.html')
def profile(request):
    return render(request,'message/profile.html')



@login_required
def chart_view(request):
    
    data = SentMessage.objects.annotate(date=TruncDate('sent_at')).values('date').annotate(count=Count('id'))
    dates = [d['date'].strftime('%y-%m-%d') for d in data]
    counts = [d['count'] for d in data]

    context = {
        'dates': dates,
        'counts': counts,
    }

    return render(request, 'message/chart.html', context)


def send_message(request):
    if request.method == 'POST':
        # Get the IP address of Airmore
        ip_address = "192.168.137.30"

        # Retrieve the phone numbers from the database
        phone_number = Member.objects.filter(company='church')

        # Compose the message you want to send
        # message = "Your message goes here"
        
        message = request.POST.get("message")
        sentms=SentMessage.objects.create(message=message)
        sentms.save()

        # Iterate through each phone number and send the message
        for number in phone_number:
            phone_number = number.phone_number

            # Construct the URL for sending the message
            url = f"http://{ip_address}:2333/sms/sendgr"

            # Prepare the payload for the POST request
            payload = {
                "phone": phone_number,
                "content": message
            }
            time.sleep(1)
            try:
                # Send the POST request to Airmore API
                response = requests.post(url, data=payload)
                if response.status_code == 200:
                    print("Message sent successfully!")
                    print(f"message sent to {phone_number}")
                else:
                    print(f"Failed to send message to {phone_number}!")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while sending message to {phone_number}: {str(e)}")

        return render(request,"message/success.html")
    else:
        return render(request, 'message/index.html')
@login_required
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")
class CustomPasswordResetView(PasswordResetView):
    success_url = '/login/'


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


@login_required
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
@login_required
def admin_view(request):
    return render(request, 'admin/change.html')

