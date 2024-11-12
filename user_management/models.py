from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager

# Create your models here.
class User(AbstractBaseUser):
    ROLE_CHOICE= (
        ('Admin', 'Admin'),
        ('Viewer','Viewer'),
        ('Moderator', 'Moderator'),
    )
    first_name= models.CharField(max_length=225, blank=True, null=True)
    last_name= models.CharField(max_length=225, blank=True, null=True)
    email= models.EmailField(max_length=225, unique=True, null=True, blank=True)
    phone_number= models.CharField(max_length=15, unique=True)
    role= models.CharField(max_length=20, choices=ROLE_CHOICE,default='Viewer')
    forget_password_token=models.CharField(max_length=1000, null=True)
    is_superuser= models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    username= None

    USERNAME_FIELD='phone_number'
    REQUIRED_FIELDS=[]

    objects = UserManager()

    def __str__(self):
        return self.first_name
    
    def has_perm(self, perm, obj= None):
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return True