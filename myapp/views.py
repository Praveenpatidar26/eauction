from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect

from . import emailAPI
from . import models
import time

dt=time.asctime()

#middleware introduction..
def myapp_middleware(get_response):         #get_response
    def middleware(request):
        if request.path=='/login/':
            request.session['snum']=None
            request.session['srol']=None
            response=get_response(request)
        else:
            response=get_response(request)
        return response
    return middleware
            


def home(request):
    return render(request,"home.html")

def about(request):
    return render(request, "about.html")

def service(request):
    return HttpResponse('<h1>service calling</h>')

def contact(request):
    return HttpResponse('<h1>contact calling</h>')

def register(request):
    if request.method=="GET":
        return render(request,'register.html', {'msg' : ''})
    else:
        email=request.POST.get('email')
        elist=models.Register.objects.filter(username=email)                #this is to check email already exist or not..
        if len(elist)>0:
            return render(request,'register.html', {'msg' : 'User Already Exists'})
        else:
            name=request.POST.get('name')
            email=request.POST.get('email')
            password=request.POST.get('password')
            mobile=request.POST.get('mobile')
            city=request.POST.get('city')
            gender=request.POST.get('gender')

            p=models.Register(name=name,username=email,password=password,mobile=mobile,city=city,gender=gender,status=0,role="user",dt=dt)
            p.save()
            emailAPI.sendEmail(email,password)
            return render(request, 'register.html',{'msg' : 'Form Submitted'})


def login(request):
    if request.method=="GET":
        return render(request, "login.html",{'msg' : ''})
    else :
        email=request.POST.get("email")
        password=request.POST.get("password")

        userDetails=models.Register.objects.filter(username=email,password=password,status=1)
        # print(userDetails)
        # print(len(userDetails))
        if len(userDetails)>0:
            # print(userDetails[0].role)
            request.session['snum']=userDetails[0].username   #session implamentation
            request.session['srol']=userDetails[0].role
            # print(request.session['srol'])
            # print(request.session['snum'])
            if userDetails[0].role=="user":
                return redirect("/user/")        
            else:
                return redirect("/myadmin/")
        else:
            return render(request,"login.html",{'msg':'Invalid user plase try again....'})