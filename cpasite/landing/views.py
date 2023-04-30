from django.shortcuts import render, HttpResponse, redirect
from django.template import loader
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Allinstanceprice
from django.db.models import Q


# Create your views here.
def land(request):
    return render(request,'home.html')

def about(request):
    return HttpResponse("This is about page")

def contact(request):
    return HttpResponse("This is contact page")


def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
    
        if len(username)<6:
            messages.error(request, "Username should have at least 6 characters")
            return redirect('land')
        
        if not username.isalnum():
            messages.error(request, "Username should be alphanumeric")
            return redirect('land')
        if pass1!=pass2:
            messages.error(request, "Passwords do not match")
            return redirect('land')
    
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name= lname
        myuser.save()
        messages.success(request, "User created successfully")
        return redirect('land')
    
    else:
        return HttpResponse("404 - Page Not Found")
    
def signin(request):
    if request.method=="POST":
        username=request.POST['loginusername']
        passwd=request.POST['loginpassword']

        user=authenticate(username=username, password=passwd)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("land")
    else:
        return HttpResponse("404 - Page Not Found")
    
def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("home")


def index(request):
    if request.method=='POST':
        instanceType=request.POST.get('instanceType')
        vcpu=request.POST.get("vcpu")
        os_value=request.POST.get("os")
        awsRegion=request.POST.get("awsregion")
        gcpRegion=request.POST.get("gcpregion")
        azRegion=request.POST.get("azregion")
        
        allinstancePrices=Allinstanceprice.objects.all()
        regionList=[]
        if awsRegion!="None":
            regionList.append(awsRegion)
        if gcpRegion!="None":
            regionList.append(gcpRegion)
        if azRegion!="None":
            regionList.append(azRegion)
        if os_value=="Linux":
            filteredInstances=allinstancePrices.filter(vcpu=vcpu, instance_family=instanceType, region__in=regionList).order_by('linux_price')
        else:
            filteredInstances=allinstancePrices.filter(vcpu=vcpu, instance_family=instanceType, region__in=regionList).order_by('windows_price')

        template = loader.get_template('index.html')
        context = {
        'InstancePrices': filteredInstances,
        'os': os_value,
        }
        return HttpResponse(template.render(context, request))
        
        #return render(request, "index.html")
    
    else:
        return render(request, "index.html")