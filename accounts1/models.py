from django.db import models
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import AbstractUser
import random
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True)

  
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number'] 

    def __str__(self):
        return self.email
class OTP(models.Model):
        user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
        code=models.CharField(max_length=6,unique=True)
        created_at=models.DateTimeField(auto_now_add=True)
        expiry_time=models.DateTimeField()
        attempts=models.IntegerField(default=0)

        def is_expired(self):
           return timezone.now()>self.expiry_time
        
        @staticmethod
        def generate_otp():
            return str(random.randint(100000,999999))
         