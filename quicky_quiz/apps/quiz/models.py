from django.db import models

class Quiz(models.Model):
    """Quiz container"""
    QUIZ_TYPES = [
        ('daily', 'Daily Quiz'),
        ('weekly', 'Weekly Challenge'),
        ('monthly', 'Monthly Test'),
        ('category', 'Category Quiz'),
        ('custom', 'Custom Practice'),
    ]
    
    title = models.CharField(max_length=200)
    title_bn = models.CharField(max_length=300)
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPES)
    category = models.CharField(max_length=20, null=True, blank=True)
    duration_minutes = models.IntegerField(default=10)
    total_questions = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'quizzes'


class Question(models.Model):
    """Individual quiz question"""
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    related_news = models.ForeignKey('news.ProcessedNews', on_delete=models.SET_NULL, null=True, blank=True)
    question_text = models.TextField()
    question_text_bn = models.TextField()
    options = models.JSONField()  # [{"id": "A", "text": "...", "text_bn": "..."}]
    correct_answer = models.CharField(max_length=1)
    explanation = models.TextField()
    explanation_bn = models.TextField()
    category = models.CharField(max_length=20)
    difficulty = models.CharField(max_length=10, default='medium')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'questions'


class QuizAttempt(models.Model):
    """User quiz attempt record"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    total_questions = models.IntegerField()
    time_taken_seconds = models.IntegerField(null=True, blank=True)
    answers = models.JSONField(default=dict)  # {"question_id": "selected_option"}
    
    class Meta:
        db_table = 'quiz_attempts'
