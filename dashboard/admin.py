from django.contrib import admin
from .models import Rooms, Availability, RoomBooking

class RoomRef(admin.ModelAdmin):
    list_display = ['room_name','room_occ','room_price','no_of_rooms_avail']
    list_filter = ['room_class']
admin.site.register(Rooms,RoomRef)

class AvailabilityRef(admin.ModelAdmin):
    list_filter = ['room_type','month','date']
    list_display = ['room_type','month','date','rooms_available']
admin.site.register(Availability,AvailabilityRef)

class RoomBookingRef(admin.ModelAdmin):
    list_display = ['user','room','total_days','cost','no_of_rooms','payment_ref']
    list_filter = ['check_in_date','check_out_date','check_in_time','check_out_time','is_cancelled']
admin.site.register(RoomBooking,RoomBookingRef)