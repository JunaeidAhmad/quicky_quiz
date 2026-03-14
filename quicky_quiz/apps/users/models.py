from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Extended user model"""
    phone = models.CharField(max_length=15, unique=True)
    exam_type = models.CharField(max_length=20, choices=[
        ('bcs', 'BCS'),
        ('bank', 'Bank Job'),
        ('primary', 'Primary Teacher'),
        ('ntrca', 'NTRCA'),
        ('other', 'Other Government'),
    ], default='bcs')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_premium = models.BooleanField(default=False)
    premium_expiry = models.DateTimeField(null=True, blank=True)
    streak_count = models.IntegerField(default=0)
    last_active = models.DateTimeField(auto_now=True)
    xp_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    referral_code = models.CharField(max_length=10, unique=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'users'


class UserPreference(models.Model):
    """User preferences for personalization"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    preferred_categories = models.JSONField(default=list)  # ['national', 'economy', ...]
    notification_enabled = models.BooleanField(default=True)
    morning_digest_time = models.TimeField(default='07:00')
    language = models.CharField(max_length=5, default='bn', choices=[('en', 'English'), ('bn', 'Bengali')])
    dark_mode = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'user_preferences'
