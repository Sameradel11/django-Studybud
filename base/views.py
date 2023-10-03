from django.shortcuts import render,redirect

from django.http import HttpResponse

from .models import Room

from .forms import RoomForm



# Create your views here.

def home(request):

    rooms=Room.objects.all()

    context={'rooms':rooms}

    return render(request,'base/home.html',context)


def room(request,pk):

    requestedroom=Room.objects.get(id=pk)

    currentroom={'requestedroom':requestedroom}

    return render(request,'base/room.html',currentroom)

def createroom(request):
    if request.method=="POST":
        form =RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    form=RoomForm()
    context={'form':form}
    return render(request,'base/room_form.html',context)

def updateroom(request,pk):
    room=Room.objects.get(id=pk)
    print(room) 
    if request.method=="POST":
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    form=RoomForm(instance=room)
    context={'form':form}
    return render(request,'base/room_form.html',context)


    
def deleteroom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=="POST":
        room.delete()
        return redirect('home')
    context={'room':room}
    return render(request,'base/delete.html',context)