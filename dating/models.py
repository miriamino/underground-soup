import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    class Importance(models.IntegerChoices):
        NOT_IMPORTANT = 0, _('doesn\'t matter at all')
        SLIGHTLY = 1, _('a little')
        MEDIUM = 50, _('average')
        VERY_IMPORTANT = 250, _('very important')
        MANDATORY = 300, _('mandatory')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_self = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    answer_other = models.ManyToManyField(Choice, related_name='answer_other')
    importance = models.IntegerField(choices=Importance.choices, default=50)
    public_self = models.BooleanField(default=False)
    public_other = models.BooleanField(default=False)
    answer_date = models.DateTimeField('date answered', default=timezone.now)

    def __str__(self):
        return f'{self.user.username}: {self.question.question_text}'

class Matching(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    other_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='other_user')
    forward_score = models.DecimalField(default=0, decimal_places=1, max_digits=5)
    backward_score = models.DecimalField(default=0, decimal_places=1, max_digits=5)
    combined_score = models.DecimalField(default=0, decimal_places=1, max_digits=5)
