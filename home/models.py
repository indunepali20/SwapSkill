from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_have = models.CharField(max_length=100)
    skill_want = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.skill_have} - {self.user.username}"