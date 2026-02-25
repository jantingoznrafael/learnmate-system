from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

QUESTION_STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
]

STRAND_CHOICES = [
    ('ALL', 'All'),
    ('HUMSS', 'HUMSS'),
    ('ABM', 'ABM'),
    ('TVL', 'TVL'),
    ('GAS', 'GAS'),
]

class Question(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    strand = models.CharField(max_length=10, choices=STRAND_CHOICES, default='ALL')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    status = models.CharField(max_length=10, choices=QUESTION_STATUS_CHOICES, default='PENDING')
    is_reported = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('questions:detail', kwargs={'pk': self.pk})

    @property
    def answer_count(self):
        return self.answers.count()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Answer to: {self.question.title}"


class ReportedQuestion(Question):
    class Meta:
        proxy = True
        verbose_name = 'Reported Question'
        verbose_name_plural = 'Reported Questions'

    @property
    def report_reason(self):
        return "Inappropriate content"
