from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from .models import Room,Topic,Message
from django.contrib import messages
from .forms import RoomForm,MessageForm



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
    messages=requestedroom.message_set.all().order_by('-created')
    participants=requestedroom.participants.all()
    if(request.method=='POST'):
        message=Message.objects.create(
            user=request.user,
            room=requestedroom,
            body=request.POST.get("body")
        )
        requestedroom.participants.add(request.user)
        message.save()
        print(message)
        return redirect(request.path)
    currentroom={'requestedroom':requestedroom,'messages':messages,"participants":participants}
    return render(request,'base/room.html',currentroom)


################ CRUD room ################
@login_required(login_url='login')
def createroom(request):
    if request.method=="POST":
        form =RoomForm(request.POST)
        print(request.POST)
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



################ Registeration ################
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
                print(request.path)
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

################ CRUD Message ################
def deletemessage(request,pk):
    pk=int(pk)
    message=Message.objects.get(id=pk)
    room=message.room.id
    print(room)
    if request.user!=message.user:
        return HttpResponse("You are not allowed to be here")

    if request.method=="POST":
        print('entered post')
        message.delete()
        return redirect('room',pk=room)
    context={'message':message}
    return render(request,'base/delete_message.html',context)

