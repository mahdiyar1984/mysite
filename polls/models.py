from django.contrib import admin
from django.utils import timezone
import datetime
from django.utils import timezone
from django.db import models


class Question(models.Model):
    objects = models.Manager()
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,  # نمایش به صورت تیک سبز/قرمز به جای True/False
        ordering="pub_date",  # امکان مرتب‌سازی بر اساس pub_date
        description="Published recently?",  # عنوان ستون در ادمین
    )

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    objects = models.Manager()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

