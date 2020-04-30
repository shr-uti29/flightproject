from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Profile,Flight,Flightseat,Booking
from datetime import date, datetime
from accounts.forms import EditProfileForm,ProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
j=0
oneway=''
ret1=''
ret2=''
r1=0
r2=0

# Create your views here.
def register(request):
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        Contact = request.POST['Contact']
        Address = request.POST['Address']
        DOB=datetime.strptime(request.POST['DOB'],'%Y-%m-%d').date()
        Gender = request.POST['Gender']
        

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already registered')
                return redirect('register')
            else:     
                user= User.objects.create_user(username=username,password=password1,first_name=first_name,last_name=last_name,email=email)
                user.save()
                prof=Profile(user=user,Contact=Contact,Address=Address,DOB=DOB,Gender=Gender)
                prof.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(request,'Password not matching')
            return redirect('register')
        return redirect('main.html')
    else:
        return render(request,'register1.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('main')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,'login1.html')

def main(request):
    return render(request,'main.html',{'name':request.user.get_username()})

def logout(request):
    auth.logout(request)
    return redirect('home')
    
@login_required
def edit(request):
    
    if request.method == 'POST':
        user=User.objects.get(username=request.user.get_username())
        form= EditProfileForm(request.POST,instance=user)
        profile_form= ProfileForm(request.POST,instance=Profile.objects.get(user=user))

        print(form.errors)
        print(profile_form.errors)
        if form.is_valid and profile_form.is_valid:
            form.save()
            profile_form.save()
            return redirect('main')
    else:
        user=User.objects.get(username=request.user.get_username())
        form= EditProfileForm(instance=user)  
        profile_form= ProfileForm(instance=Profile.objects.get(user=user))
        return render(request,'editprofile.html',{'form':form,'profile_form':profile_form})

def book(request):
    if request.method == 'POST':
        f = request.POST.get('from')
        t = request.POST.get('to')
        d= request.POST.get('departure')
        r= request.POST.get('return1')
        tr= request.POST.get('trip')
        print(f)
        print(t)
        print(d)
        print(r)
        print(tr)
        if r is None:
            r='2000-01-01'
        if (tr == 'round'):
            return HttpResponseRedirect(reverse('availability',kwargs={'fr':str(f),'to':str(t),'dt':str(d),'dt1':str(r)}))
        else:
            return HttpResponseRedirect(reverse('availability_one',kwargs={'fr':str(f),'to':str(t),'dt':str(d)}))
    #print(request.POST)
    return render(request,'bookflight.html')

def availability_one(request,fr,to,dt):
    schedule= Flight.objects.filter(From=fr,To=to,Date=dt)
    if request.method == 'POST':
        fno= request.POST.get('onward')
        print(fno)
        global oneway
        oneway=fno
        #f=Flight.objects.raw('SELECT * FROM accounts_flight WHERE FlightNo = %s', [fno])
        f=Flight.objects.filter(FlightNo=fno)
        print(f)
        return redirect('seat')
    
    return render(request,'book.html',{'schedule':schedule})

def availability(request,fr,to,dt,dt1):
    schedule= Flight.objects.filter(From=fr,To=to,Date=dt)
    print(dt1)
    scheduler=Flight.objects.filter(From=to,To=fr,Date=dt1)
    if request.method == 'POST':
        fno= request.POST.get('onward')
        rno= request.POST.get('ret')
        global ret1
        global ret2
        ret1=fno
        ret2=rno
        print(fno)
        print(rno)
        #f=Flight.objects.raw('SELECT * FROM accounts_flight WHERE FlightNo = %s', [fno])
        f=Flight.objects.filter(FlightNo=fno)
        r=Flight.objects.filter(FlightNo=rno)
        print(f)
        print(r)
        return redirect('seat_ret1')
    
    return render(request,'bookreturn.html',{'schedule':schedule,'scheduler':scheduler})


def mybookings(request):
    f=Booking.objects.filter(Username=request.user.get_username())
    return render(request,'currentbook.html',{'flights':f})

def change_password(request):
    if request.method == 'POST':
        form= PasswordChangeForm(data=request.POST,user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('main')
        else:
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args={'form':form}
        return render(request,'change_password.html',args)

def seat(request):
    for i in range(0,10):
       
        result1=Flightseat.objects.filter(svalue=False).order_by('id')[:6]
        result3=Flightseat.objects.filter(svalue=False).order_by('id')[6:12]
        result4=Flightseat.objects.filter(svalue=False).order_by('id')[12:18]
        result2=Flightseat.objects.filter(svalue=True).order_by('id')[:i+2]
    #print(result1)
    #print(result3)
    #print(result4)
    #print(result2)
    #paginator = Paginator(result1, 6)
    if request.method=='POST':
        seat=request.POST['button']
        #no= int(request.POST.get('number'))
        global j
        j=j+1
        print(seat)
        #print(no)
        print(j)
        

        if Flightseat.objects.filter(seat=seat).exists():
            value=Flightseat.objects.get(seat=seat)
            if value.svalue==False:
                value.svalue=True
                value.save()
                result2=Flightseat.objects.filter(svalue=True).order_by('id')
                result1=Flightseat.objects.filter(svalue=False).order_by('id')[:6]
                result3=Flightseat.objects.filter(svalue=False).order_by('id')[6:12]
                result4=Flightseat.objects.filter(svalue=False).order_by('id')[12:18]
                print("seat is booked")
                return render(request,'seatwc.html',{'result2':result2,'result1':result1,'result3':result3,'result4':result4}) 
            elif value.svalue==True:
                print("seat is already occupied. Please select another seat")
                return render(request,'seatwc.html',{ 'result2':result2,'result1':result1,'result3':result3,'result4':result4})
        else:
            return render(request,'seatwc.html',{'result2':result2,'result1':result1,'result3':result3,'result4':result4})
        
        return redirect('payment')
    else:
          
        return render(request,'seatwc.html',{'result2':result2,'result1':result1,'result3':result3,'result4':result4})

def seat_ret1(request):
    for i in range(0,10):
       
        result1=Flightseat.objects.filter(svalue=False).order_by('id')[:6]
        result3=Flightseat.objects.filter(svalue=False).order_by('id')[6:12]
        result4=Flightseat.objects.filter(svalue=False).order_by('id')[12:18]
        result2=Flightseat.objects.filter(svalue=True).order_by('id')[:i+2]
    #print(result1)
    #print(result3)
    #print(result4)
    #print(result2)
    #paginator = Paginator(result1, 6)
    if request.method=='POST':
        seat=request.POST['button']
        global r1
        r1=r1+1
        print(seat)
        #print(no)
        print(r1)
        
        if Flightseat.objects.filter(seat=seat).exists():
            value=Flightseat.objects.get(seat=seat)
            if value.svalue==False:
                value.svalue=True
                value.save()
                result2=Flightseat.objects.filter(svalue=True).order_by('id')
                result1=Flightseat.objects.filter(svalue=False).order_by('id')[:6]
                result3=Flightseat.objects.filter(svalue=False).order_by('id')[6:12]
                result4=Flightseat.objects.filter(svalue=False).order_by('id')[12:18]
                print("seat is booked")
                return render(request,'seat_ret.html',{'result2':result2,'result1':result1,'result3':result3,'result4':result4}) 
            elif value.svalue==True:
                print("seat is already occupied. Please select another seat")
                return render(request,'seat_ret.html',{ 'result2':result2,'result1':result1,'result3':result3,'result4':result4})
        else:
            return render(request,'seat_ret.html',{'result2':result2,'result1':result1,'result3':result3,'result4':result4})

        return redirect('seat_ret2')
    else:
          
        return render(request,'seat_ret.html',{'result2':result2,'result1':result1,'result3':result3,'result4':result4})
    
def seat_ret2(request):
    for i in range(0,10):
       
        result1=Flightseat.objects.filter(svalue=False).order_by('id')[:6]
        result3=Flightseat.objects.filter(svalue=False).order_by('id')[6:12]
        result4=Flightseat.objects.filter(svalue=False).order_by('id')[12:18]
        result2=Flightseat.objects.filter(svalue=True).order_by('id')[:i+2]
    #print(result1)
    #print(result3)
    #print(result4)
    #print(result2)
    #paginator = Paginator(result1, 6)
    if request.method=='POST':
        seat=request.POST['button']
        global r2
        r2=r2+1

        print(seat)
        print(r2)

        if Flightseat.objects.filter(seat=seat).exists():
            value=Flightseat.objects.get(seat=seat)
            if value.svalue==False:
                value.svalue=True
                value.save()
                result2=Flightseat.objects.filter(svalue=True).order_by('id')
                result1=Flightseat.objects.filter(svalue=False).order_by('id')[:6]
                result3=Flightseat.objects.filter(svalue=False).order_by('id')[6:12]
                result4=Flightseat.objects.filter(svalue=False).order_by('id')[12:18]
                print("seat is booked")
                return render(request,'seat_ret2.html',{'result2':result2,'result1':result1,'result3':result3,'result4':result4}) 
            elif value.svalue==True:
                print("seat is already occupied. Please select another seat")
                return render(request,'seat_ret2.html',{ 'result2':result2,'result1':result1,'result3':result3,'result4':result4})
        else:
            return render(request,'seat_ret2.html',{'result2':result2,'result1':result1,'result3':result3,'result4':result4})

        return redirect('payment_ret')
    else:
          
        return render(request,'seat_ret2.html',{'result2':result2,'result1':result1,'result3':result3,'result4':result4})

def payment(request):
    global oneway
    global j
    fl=Flight.objects.get(FlightNo=oneway)
    p=fl.Price
    print(p)
    cost=p*j
    print(cost)
    b= Booking(Username=request.user.get_username(),FlightNo=oneway,Departure=fl.Departure,Arrival=fl.Arrival,Date=fl.Date,From=fl.From,To=fl.To,Seats=j,Price=cost)
    b.save()
    j=0
    return render(request,'payment.html',{'cost':cost})

def payment_ret(request):
    global ret1
    global ret2
    global r1
    global r2
    fl=Flight.objects.get(FlightNo=ret1)
    fli=Flight.objects.get(FlightNo=ret2)
    p=fl.Price
    pr=fli.Price
    print(p)
    print(pr)
    cost1=p*r1
    cost2=pr*r2
    print(cost1)
    print(cost2)
    cost3=cost2+cost1
    b= Booking(Username=request.user.get_username(),FlightNo=ret1,Departure=fl.Departure,Arrival=fl.Arrival,Date=fl.Date,From=fl.From,To=fl.To,Seats=r1,Price=cost1)
    b.save()
    b1=Booking(Username=request.user.get_username(),FlightNo=ret2,Departure=fli.Departure,Arrival=fli.Arrival,Date=fli.Date,From=fli.From,To=fli.To,Seats=r2,Price=cost2)
    b1.save()
    r1=0
    r2=0
    return render(request,'payment.html',{'cost':cost3})
    

