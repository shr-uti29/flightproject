from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Profile,Flight
from datetime import date, datetime
from accounts.forms import EditProfileForm,ProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse



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
    return render(request,'home.html')
    
@login_required
def edit(request):
    user=User.objects.get(request.user)
    profile=Profile.objects.get()
    form = EditProfileForm(request.POST or None,instance=user)
    profile_form = ProfileForm(request.POST or None,instance=request.user)
    if request.method == 'POST':
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect('main') 
        else:
            form = EditProfileForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user)
            args={'form':form,'profile_form':profile_form}
            return render(request,'editprofile.html',args)
    else:
        return HttpResponse(template.render(variables))

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
        if r is None:
            r='2000-01-01'
        return HttpResponseRedirect(reverse('availability',kwargs={'fr':str(f),'to':str(t),'dt':str(d),'dt1':str(r)}))
    #print(request.POST)
    return render(request,'bookflight.html')

def availability(request,fr,to,dt,dt1):
    schedule= Flight.objects.filter(From=fr,To=to,Date=dt)
    print(dt1)
    scheduler=Flight.objects.filter(From=to,To=fr,Date=dt1)
    if request.method == 'POST':
        fno= request.POST.get('Id')
        print(fno)
        #f=Flight.objects.raw('SELECT * FROM accounts_flight WHERE FlightNo = %s', [fno])
        f=Flight.objects.filter(FlightNo=fno)
        print(f)
    return render(request,'book.html',{'schedule':schedule,'scheduler':scheduler})


def mybookings(request):
     return render(request,'currentbook.html')

