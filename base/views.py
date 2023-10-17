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
    messages=Message.objects.filter(Q(room__topic__name__icontains=q)) 
    
    context={'rooms':rooms,'topics':topics,'roomcount':len(rooms),"messages":messages}
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
        return redirect(request.path)
    currentroom={'room':requestedroom,'messages':messages,"participants":participants}
    return render(request,'base/room.html',currentroom)


################ CRUD room ################
@login_required(login_url='login')
def createroom(request):
    if request.method=="POST":
        topic_name=request.POST.get("topic")
        topic,created=Topic.objects.get_or_create(name=topic_name)
        print(topic)
        room=Room.objects.create(
            name=request.POST.get("room_name"),
            host=request.user,
            description=request.POST.get("room_about"),
            topic=topic,
        )
        room.participants.add(request.user)
        room.save()
        return redirect('home')
    topics=Topic.objects.all()
    context={'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateroom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse("You are not allowed to be here")

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
    return render(request,'base/delete_room.html',context)



################ Registeration ################
def loginpage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else :
                messages.error(request, "There is a problem")
        except:
            messages.error(request, "User not exist")
    return render(request,'base/login.html')

def logoutpage(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method=="POST":
        if(request.POST.get("password")!=request.POST.get("confirm_password")):
            print("NO")
        else:
            newuser=User.objects.create(
            username=request.POST.get("username"),
            password=request.POST.get("password")
            )
            newuser.save()
            login(request,newuser)
    return render(request,'base/signup.html')

def edituser(request):
    return render(request,'base/edit-user.html')


################ CRUD Message ################
def deletemessage(request,pk):
    pk=int(pk)
    message=Message.objects.get(id=pk)
    room=message.room.id
    if request.user!=message.user:
        return HttpResponse("You are not allowed to be here")

    if request.method=="POST":
        message.delete()
        return redirect('room',pk=room)
    context={'message':message}
    return render(request,'base/delete_message.html',context)

def editmessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse("You are not allowed to be here")
    if request.method=="POST":
        message.body=request.POST.get('body')
        message.save()
        return redirect('room',pk=message.room.id)
    context={'message':message}
    return render(request,'base/edit_message.html',context)

################ profile ################
def profile(request,pk):
    user=User.objects.get(id=pk) 
    rooms=user.room_set.all()
    messages=user.message_set.all()
    topics=Topic.objects.all()
    context={"user":user,"rooms":rooms,"messages":messages,'topics':topics}
    return render(request,'base/profile.html',context)


def settings(request):
    return render(request,'base/settings.html')