from django.db import models
from registration.models import User

# Create your models here.
class Rooms(models.Model):
    room_name = models.CharField(max_length=50)
    room_desc = models.CharField(max_length=200)
    room_occ = models.IntegerField()
    room_price = models.IntegerField()
    no_of_rooms_avail = models.IntegerField()
    select =(('Economy','Economy'),('Premium','Premium'))
    room_class = models.CharField(max_length=10,choices=select) 
    room_img = models.ImageField(upload_to = 'room_pics/')

class Availability(models.Model):
    room_type = models.ForeignKey(Rooms, on_delete = models.CASCADE)
    date = models.DateField()
    month = models.CharField(max_length=20)
    rooms_available = models.IntegerField()
    

class RoomBooking(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE)
    check_in_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_date = models.DateField()
    check_out_time = models.TimeField()
    date_booked = models.DateField()
    is_cancelled = models.BooleanField()
    cancelled_date = models.DateField(null=True)
    total_days = models.IntegerField()
    cost = models.IntegerField()
    no_of_rooms = models.IntegerField(default=1)
    payment_ref = models.CharField(max_length=50)
