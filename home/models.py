from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_have = models.CharField(max_length=100)
    skill_want = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.skill_have



        