from django.db import models


class EmailMessageModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    to_email = models.EmailField()
    subject = models.CharField(max_length=255)
    body_text = models.TextField()
    body_html = models.TextField()
    event_type = models.CharField(max_length=100)
    status = models.CharField(max_length=32, default="pending")
    retry_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
