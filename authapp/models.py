from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator

class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Explicitly set role to superadmin for superusers created through manage.py
        extra_fields['role'] = 'superadmin'
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self._create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('admin', 'Admin Bimbel'),
        ('siswa', 'Siswa'),
    )

    username_validator = RegexValidator(
        regex=r'^[\w\s.@+-]+$',
        message='Username hanya boleh berisi huruf, angka, spasi, dan karakter @/./+/-/_.'
    )
    
    username = models.CharField(
        max_length=150,
        unique=False,
        validators=[username_validator],
        error_messages={}
    )
    
    email = models.EmailField(unique=True)
    # Keep default as siswa for security reasons
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='siswa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Field tambahan untuk siswa
    no_telp = models.CharField(max_length=15, null=True, blank=True)
    tanggal_lahir = models.DateField(null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # Use our custom manager
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"