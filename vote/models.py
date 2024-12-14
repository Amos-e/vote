from django.db import models
from main.models import Member


class Poll(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "%s %s"%(self.id, self.title)


class Eligible(models.Model):
    id = models.BigAutoField(primary_key=True)
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s"%(self.member.full_names)


class Vote(models.Model):
    id = models.BigAutoField(primary_key=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    voter = models.ForeignKey(Eligible, on_delete=models.CASCADE, related_name="voter_member")
    vote = models.ForeignKey(Eligible, on_delete=models.CASCADE)

    def __str__(self):
        return "%s --> %s"%(self.voter , self.vote)

