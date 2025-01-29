from django.db import models

class Item(models.Model):
    title = models.CharField(max_length=1000)

class Box(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    value = models.CharField(max_length=1000)