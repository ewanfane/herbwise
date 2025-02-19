from django.db import models

class Record(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict)
