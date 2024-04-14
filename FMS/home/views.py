from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from datetime import datetime
from home.models import AddSpending
from django.core import serializers
from django.contrib import messages
from django.db.models import Sum
from django.utils.timezone import now, timedelta
import json

from .forms import CreateUserForm

# Create your views here.


def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    username = request.user.username
    seven_days_ago = now() - timedelta(days=14)
    transactions = AddSpending.objects.filter(Date__gte=seven_days_ago,FMSuser=username )
    data2 = {}
    for transaction in transactions:
        date = transaction.Date.strftime('%Y-%m-%d')  
        amount = float(transaction.Amount)  
        if date in data2:
            data2[date] += amount
        else:
            data2[date] = amount
    labels = list(data2.keys())
    amounts = list(data2.values())
    
    data=serializers.serialize("python", AddSpending.objects.filter(FMSuser=username).order_by('-id')[:10])
    tsum=AddSpending.objects.filter(Date=datetime.today(),FMSuser=username).aggregate(tsum=Sum('Amount'))['tsum'] or 0
    current_date = datetime.now()
    month = current_date.month
    year = current_date.year
    spendings = AddSpending.objects.filter(Date__month=month, Date__year=year, FMSuser=username)
    msum = spendings.aggregate(msum=Sum('Amount'))['msum'] or 0
    lmonth = current_date.month-1
    spendings2 = AddSpending.objects.filter(Date__month=lmonth, Date__year=year, FMSuser=username)
    lsum = spendings2.aggregate(lsum=Sum('Amount'))['lsum'] or 0
    context={
        'data':data,
        'tsum':tsum,
        'labels': json.dumps(labels),  
        'amounts': json.dumps(amounts),
        'msum':msum,
        'lsum':lsum,
    }
    return render(request,'index.html',context)

def loginUser(request):
    if not(request.user.is_anonymous):
        return redirect("/")
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Invalid credentials")
            return render(request,'login.html')
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")

def add_spending(request):
    if request.user.is_anonymous:
        return redirect("/login")
    if request.method=="POST":
        FMSuser=request.POST.get("FMSuser")
        PaidTo=request.POST.get("PaidTo")
        Amount=request.POST.get("Amount")
        Reason=request.POST.get("Reason")
        Remarks=request.POST.get("Remarks")
        transaction=AddSpending(PaidTo=PaidTo, Amount=Amount, FMSuser=FMSuser, Date=datetime.today(), Reason=Reason, Remarks=Remarks)
        transaction.save()
        messages.info(request,"Transaction added succesfully")
    return render(request,"add-spending.html")

def register(request):
    if not(request.user.is_anonymous):
        return redirect("/")
    form = CreateUserForm()
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            messages.info(request,"Kindly recheck your details or try a different username")
            return redirect('/register')
    return render(request,'register.html')

def spendings(request):
    if request.user.is_anonymous:
        return redirect("/login")
    username = request.user.username
    data=serializers.serialize("python", AddSpending.objects.filter(FMSuser=username).order_by('-id'))
    context={
        'data':data,
    }
    return render(request,'spendings.html',context)

def my_profile(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'my-profile.html')

