from django.db import models
from datetime import datetime
# Create your models here.
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime

class RoomModel(models.Model):
    CHOICES = (
        ("focus", "focus"),
        ("team", "team"),
        ("conference", "conference"),
    )
    name = models.CharField(max_length=500)
    type = models.CharField(max_length=100, choices=CHOICES)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name
    

class BookRoomModel(models.Model):
    resident = models.CharField(max_length=500)
    room_id = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    
    def __str__(self):
        return self.resident[23:-4]
    