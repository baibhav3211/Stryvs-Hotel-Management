from django.shortcuts import render, redirect
from .models import Rooms, Availability, RoomBooking
from django.contrib import auth, messages
from registration.models import User
import datetime

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def availrooms(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    eco = Rooms.objects.filter(room_class="Economy").all()
    pre = Rooms.objects.filter(room_name="Premium").all()
    # src = Availability.objects.all()
    # print(src)
    return render(request,'rooms_avail.html',{'eco':eco,'pre':pre})
    # return HttpResponse('Rooms available')


def getVacancy(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    if request.method=="POST":
        vacant_date = request.POST["vacant_date"]
        room = request.POST["room"]
        val = Availability.objects.filter(date=vacant_date,room_type__room_name=room)
        if len(val)==0:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'{0} {1} are available on {2}'.format(Rooms.objects.filter(room_name=room)[0].no_of_rooms_avail,room,vacant_date))
            return redirect('/dashboard')
        else:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'{0} {1} are available on {2}'.format(val[0].rooms_available,room,vacant_date))
            return redirect('/dashboard')
    obj = Rooms.objects.all()
    # print(obj)
    return render(request,'check_vacancy.html',{'obj':obj})


def bookroom(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')    
    obj = Rooms.objects.values('room_name')
    return render(request,'book_room.html',{'room_select':False,'obj':obj})

def acceptBooking(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    if request.method=="POST":
        obj = Rooms.objects.filter(room_name=request.POST["room"]).all()[0]
        return render(request,'book_room.html',{'room_select':True,'obj':obj})
    else:
        return redirect('/dashboard/bookroom') 

def confirmBooking(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    if request.method=="POST":
        user = User.objects.filter(username=request.user.username)[0]
        room = Rooms.objects.filter(room_name = request.POST["book_room_type"])[0]
        check_in_date = request.POST["check_in_date"]
        check_in_time = request.POST["check_in_time"]
        check_out_date = request.POST["check_out_date"]
        check_out_time = request.POST["check_out_time"]
        date_booked = datetime.datetime.today().strftime("%Y-%m-%d")
        is_cancelled = False
        total_days = request.POST["days"]
        cost = request.POST["amount"]
        payment_ref = request.POST["payment_id"]
        no_of_rooms = request.POST["rooms_count"]
        #check whether requested rooms available on the days
        start_date = datetime.datetime.strptime(check_in_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(check_out_date, '%Y-%m-%d')
        delta = datetime.timedelta(days=1)
        flag = True 
        while start_date<=end_date:
            val = Availability.objects.filter(date=start_date,month=start_date.month,room_type=room)
            if len(val)!=0:
                if val[0].rooms_available < int(no_of_rooms):
                    flag=False 
                    break
            start_date += delta
        if not flag:
            storage = messages.get_messages(request)
            storage.used = True
            messages.info(request,'{0} {1} are not available between {2} - {3} Kindly Check the Vacancy again'.format(no_of_rooms,room.room_name,check_in_date,check_out_date))
            return redirect('/dashboard')
        obj = RoomBooking.objects.create(user=user,room=room,check_in_date=check_in_date,check_in_time=check_in_time,no_of_rooms=no_of_rooms,
                    check_out_date=check_out_date,check_out_time=check_out_time,date_booked=date_booked,is_cancelled=is_cancelled,
                    total_days=total_days,cost = cost,payment_ref=payment_ref)
        start_date = datetime.datetime.strptime(obj.check_in_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(obj.check_out_date, '%Y-%m-%d')
        delta = datetime.timedelta(days=1)
        while start_date<=end_date:
            val = Availability.objects.filter(date=start_date,month=start_date.month,room_type=obj.room)
            if len(val)==0:
                Availability.objects.create(room_type=obj.room,date=start_date,month=start_date.month,rooms_available=int(obj.room.no_of_rooms_avail)-int(obj.no_of_rooms))
            else:
                avail = Availability.objects.get(date=start_date,month=start_date.month,room_type=obj.room)
                avail.rooms_available=int(avail.rooms_available)-int(obj.no_of_rooms)
                avail.save()
            start_date += delta
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'You have successfully booked rooms.')
        return redirect('/dashboard')


def pastBookings(request):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    obj = RoomBooking.objects.filter(user__username=request.user.username,is_cancelled=False).select_related()
    li_up, li_past = [] , []
    today_date = datetime.date.today()
    for item in obj:
        if item.check_in_date>today_date:
            li_up.append(item)
        else:
            li_past.append(item)
    obj2 = RoomBooking.objects.filter(user__username=request.user.username,is_cancelled=True).select_related()
    len_li_up = len(li_up)
    len_li_past = len(li_past)
    len_obj2 = len(obj2)
    # print(len_li_up)
    # print(len_li_past)
    # print(len_obj2)
    return render(request,'pastBookings.html',{'li_up':li_up,'li_past':li_past,'canc':obj2,'len_li_up':len_li_up,'len_li_past':len_li_past,'len_obj2':len_obj2})


def cancelBooking(request,id):
    if not request.user.is_authenticated:
        storage = messages.get_messages(request)
        storage.used = True
        messages.info(request,'Not Authorized to access that page')
        return redirect('/')
    obj = RoomBooking.objects.get(id=id)
    obj.is_cancelled=True
    obj.cancelled_date=datetime.date.today()
    obj.save()
    start_date = obj.check_in_date
    end_date = obj.check_out_date
    delta = datetime.timedelta(days=1)
    while start_date<=end_date:
        val = Availability.objects.filter(date=start_date,month=start_date.month,room_type=obj.room)
        avail = Availability.objects.get(date=start_date,month=start_date.month,room_type=obj.room)
        avail.rooms_available=int(avail.rooms_available)+int(obj.no_of_rooms)
        avail.save()
        start_date += delta
    storage = messages.get_messages(request)
    storage.used = True
    messages.info(request,'You have successfully Cancelled Rooms of Booking Id BK:'+str(id))
    return redirect('/dashboard')