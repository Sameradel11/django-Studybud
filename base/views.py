from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .models import Room,Topic
from django.contrib import messages
from .forms import RoomForm



# Create your views here.
# def topic(request):
#     topics=Topic.objects.all()
#     context={"topics":topics}
#     print(context)
#     return render(request,'base/home.html',context)

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!= None else ''
    rooms=Room.objects.filter(
    Q(topic__name__icontains=q)|
    Q(description__icontains=q)|
    Q(name__icontains=q))
    topics=Topic.objects.all()
    context={'rooms':rooms,'topics':topics,'roomcount':len(rooms)}
    return render(request,'base/home.html',context)


def room(request,pk):
    requestedroom=Room.objects.get(id=pk)
    currentroom={'requestedroom':requestedroom}
    return render(request,'base/room.html',currentroom)
    
@login_required(login_url='login')
def createroom(request):
    if request.method=="POST":
        form =RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    form=RoomForm()
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateroom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse("You are not allowed to be here")

    print(room) 
    if request.method=="POST":
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    form=RoomForm(instance=room)
    context={'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def deleteroom(request,pk):
    room=Room.objects.get(id=pk)

    if request.user!=room.host:
        return HttpResponse("You are not allowed to be here")

    if request.method=="POST":
        room.delete()
        return redirect('home')
    context={'room':room}
    return render(request,'base/delete.html',context)

def loginpage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
            print(username)
            print(password)
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else :
                messages.error(request, "There is a problem")
        except:
            messages.error(request, "User not exist")
            print("Except")
    return render(request,'base/login.html')

def logoutpage(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            print(user)
            return redirect('home')
        else :
            messages.error(request, "There is a problem")
    form=UserCreationForm()
    context={'form':form}
    return render(request,'base/register.html',context)