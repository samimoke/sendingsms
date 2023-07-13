from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.db.models import CASCADE, ForeignKey
# Create your models here.
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from .permissions import CanViewOwnGroup
from django.utils.translation import gettext_lazy as _
   
Group.add_to_class('view_own_groups', CanViewOwnGroup())


       
class Profile(models.Model):
    bio=models.TextField(max_length=1000)
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    # last_name=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=100,null=True)
    phone_number=models.CharField(max_length=20,null=True)
    image=models.ImageField(upload_to="image/profile/",null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self) :
        return self.user.first_name
    def get_absolute_url(self):
        return reverse("indexes", kwargs={"pk": self.pk})
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return self.user.first_name

class Receiver(models.Model):
    name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=12)

class SentMessage(models.Model):
    # topic=models.CharField(max_length=500)
    # meet=models.CharField(max_length=200)
    # time=models.CharField(max_length=30)
    # aspace=models.CharField(max_length=100)
    # sign=models.CharField(max_length=100)
    # receiver=models.ManyToManyField( Receiver,related_name='receivers')
    sent_at=models.DateTimeField(auto_now_add=True)
    message=models.TextField()
    receiver_name=models.CharField(max_length=50)
    rec_phone_number=models.CharField(max_length=12)
    # ip_address=models.CharField(max_length=50)

    def __str__(self):
        return self.message
class Contacts(models.Model):
    name=models.CharField(("my contacts"), max_length=50)
    def __str__(self):
        return self.name
    
def get_default_user_id():
    return get_user_model().objects.get(id=1)

class Group(models.Model):
    user = models.ForeignKey(get_user_model(),default=get_default_user_id, on_delete=models.CASCADE)
    
    group_name=models.CharField('group name',max_length=100)
   
    company=models.CharField(max_length=100)
 
    def __str__(self):
        return self.group_name
    def get_members(self):
        return self.grs.all()
class Member(models.Model):
    # ip_address=models.CharField(max_length=30)
    group_id=models.CharField(max_length=5)
    
    group_name=models.ForeignKey(Group,on_delete=models.CASCADE,related_name='grs')
    name=models.CharField(max_length=100)
    company=models.CharField(max_length=100)
    phone_number=models.IntegerField()
    def __str__(self):
        return self.name
class Contact_List(models.Model):
    mycontact=models.ForeignKey(Contacts,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    company=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=12)

    def __str__(self):
        return self.name
class Sender(models.Model):
    sender_name=models.CharField(max_length=50)
    # ip_address=models.CharField(max_length=50)
    sender_number=models.CharField(max_length=12)

class Contactus(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,null=True)
    subject=models.CharField(max_length=300)
    message=models.CharField(max_length=1000)
    def __str__(self):
        return self.name

    
