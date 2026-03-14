from django.db import models

class RawNews(models.Model):
    """Raw scraped news before processing"""
    source = models.CharField(max_length=100)
    url = models.URLField(unique=True)
    title = models.TextField()
    content = models.TextField()
    scraped_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'raw_news'
        indexes = [
            models.Index(fields=['scraped_at', 'is_processed']),
        ]


class ProcessedNews(models.Model):
    """Processed news ready for app"""
    CATEGORY_CHOICES = [
        ('national', 'National'),
        ('international', 'International'),
        ('economy', 'Economy'),
        ('sports', 'Sports'),
        ('science', 'Science & Technology'),
        ('government', 'Government Orders'),
        ('awards', 'Awards & Appointments'),
        ('important_days', 'Important Days'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    raw_news = models.OneToOneField(RawNews, on_delete=models.CASCADE, related_name='processed')
    title = models.CharField(max_length=300)
    title_bn = models.CharField(max_length=500)
    bullet_points = models.JSONField()  # List of English bullet points
    bullet_points_bn = models.JSONField()  # List of Bengali bullet points
    exam_focus = models.TextField()
    exam_focus_bn = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    tags = models.JSONField(default=list)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    exam_relevance = models.JSONField(default=list)  # ['BCS', 'Bank', ...]
    publish_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    bookmark_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'processed_news'
        ordering = ['-publish_date', '-created_at']
        indexes = [
            models.Index(fields=['category', 'publish_date']),
            models.Index(fields=['is_active', 'is_premium']),
        ]


class UserNewsInteraction(models.Model):
    """Track user interactions with news"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    news = models.ForeignKey(ProcessedNews, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    is_bookmarked = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'user_news_interactions'
        unique_together = ['user', 'news']
