from django.db import models

class MonthlyEbook(models.Model):
    """Monthly current affairs compilation"""
    title = models.CharField(max_length=200)
    title_bn = models.CharField(max_length=300)
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    pdf_file = models.FileField(upload_to='ebooks/')
    cover_image = models.ImageField(upload_to='ebook_covers/')
    page_count = models.IntegerField()
    is_published = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=True)
    download_count = models.IntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'monthly_ebooks'
        unique_together = ['month', 'year']
