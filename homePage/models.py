from django.db import models


# Create your models here.

class Task(models.Model):
    task_name = models.CharField(max_length=100)
    task_description = models.CharField(max_length=500)
    due_date = models.DateField()
    status = models.CharField(max_length=100)
