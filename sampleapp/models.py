from django.db import models


class SampleModel(models.Model):
    one_field = models.IntegerField()
    #leaf1 = models.CharField(max_length=32, null=True)
    leaf2 = models.CharField(max_length=32, null=True)