from django.shortcuts import render, HttpResponse
from django.template import loader
from .models import Allinstanceprice
from django.db.models import Q


# Create your views here.
def land(request):
    return HttpResponse("This is landing page")

def login(request):
    return render(request, 'login.html')

def about(request):
    return HttpResponse("This is about page")

def contact(request):
    return HttpResponse("This is contact page")

def home(request):
    return render(request, 'home.html')


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
        filteredInstances=allinstancePrices.filter(vcpu=vcpu, instance_family=instanceType, region__in=regionList)
        template = loader.get_template('index.html')
        context = {
        'InstancePrices': filteredInstances,
        'os': os_value,
        }
        return HttpResponse(template.render(context, request))
        
        #return render(request, "index.html")
    
    else:
        return render(request, "index.html")