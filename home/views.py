from django.shortcuts import render
from .models import Destination,Feedback
from django.contrib import messages

# Create your views here.
def home(request):
    dests=Destination.objects.all()
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        f=Feedback(name=name,email=email,subject=subject,message=message)
        if f.name and f.email and f.subject and f.message is not None:
            f.save()
            messages.info(request,"Thank You For Your Valuable Feedback")
        else:
            messages.info(request,"Fill all details")
        return render(request,'home.html',{'dests':dests})
    else:
        return render(request,'home.html',{'dests':dests})


