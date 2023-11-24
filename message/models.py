from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.db.models import CASCADE, ForeignKey
# Create your models here.
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from .permissions import CanViewOwnGroup
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

   
Group.add_to_class('view_own_groups', CanViewOwnGroup())


# class CustomUser(AbstractUser):
    # Remove the first_name and last_name fields
    # first_name = None
    # last_name = None

    # Add the name field
    # name = models.CharField(max_length=255)  

class ChapaStatus(models.TextChoices):
    PENDING = 'pending', 'PENDING'
    SUCCESS = 'success', 'SUCCESS'
    CREATED = 'created', 'CREATED'
    FAILED = 'failed', 'FAILED'


class ChapaTransactionMixin(models.Model):
    # "inherit this model and add your own extra fields"
    id = models.UUIDField(primary_key=True, default=uuid4)

    amount = models.FloatField()
    currency = models.CharField(max_length=25, default='ETB')
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.TextField()

    event = models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(max_length=50, choices=ChapaStatus.choices, default=ChapaStatus.CREATED)

    response_dump = models.JSONField(default=dict)  # incase the response is valuable in the future

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.first_name} - {self.last_name} | {self.amount}"
    
    def serialize(self) -> dict:
        return {
            'amount': self.amount,
            'currency': self.currency,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'description': self.description
        }

class ChapaTransaction(ChapaTransactionMixin):
    pass    
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
        return reverse("indexeses", kwargs={"pk": self.pk})
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
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

class Created_Group(models.Model):
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
    
    group_name=models.ForeignKey(Created_Group,on_delete=models.CASCADE,related_name='grs')
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

    
