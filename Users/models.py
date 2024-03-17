from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email,username=None , password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email=email, password=password, **extra_fields)



class CustomUser(AbstractUser):
    
    profile_image = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True, verbose_name='username',
                             blank=True,null=True)
    otp = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    is_tutor=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)
    is_approved=models.BooleanField(default=False)
    is_rejected=models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    
    class Meta:
        verbose_name='CustomUser'
        verbose_name_plural="CustomUsers"


    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set', blank=True)

class Tutor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    state = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    introduction_video = models.URLField(blank=True)
    introduction_description = models.CharField(max_length=250)
    teaching_style = models.CharField(max_length=100)
    certificates = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    

class Slot(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    