from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
def index(request):
    q = request.GET.get('q')
    if not q:
        q = ''
    topics = Topic.objects.all()
    allRooms = Room.objects.all()
    rooms = Room.objects.filter(Q(name__icontains=q) | Q(topic__name__icontains=q) | Q(host__username__icontains=q)).order_by('-updated')
    roomCount = rooms.count()
    activities = Messages.objects.filter(Q(room__topic__name__icontains=q) | Q(room__host__username__icontains=q)).order_by("-created")[0:7]
    context = {
        'rooms': rooms,
        'topics': topics,
        'roomCount': roomCount,
        'activities': activities,
        'allRooms': allRooms,
        'q': q,
    }
    return render(request, 'Base/index.html', context)

def room(request, id):
    currentRoom = Room.objects.get(id=id)
    roomMessages = Messages.objects.filter(room=currentRoom).order_by('-created')
    roomParticipants = currentRoom.participants.all()
    userStatus = None

    try:
        if request.user in roomParticipants:
            userStatus = True
    except:
        userStatus = False

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('room', currentRoom.id)


        if not request.user in roomParticipants:
            messages.error(request, 'You are not a participant of this room!')
            return redirect('room', currentRoom.id)

        message = request.POST.get('messageBody')
        newMessage = Messages.objects.create(user=request.user, room=currentRoom, message=message)
        return redirect('room', currentRoom.id)
        
    context = {
        'room': currentRoom,
        'roomMessages': roomMessages,
        'participants': roomParticipants,
        'userStatus': userStatus,
    }
    return render(request, 'Base/room.html', context)

@login_required(login_url='login')
def joinRoom(request, id):
    currentRoom = Room.objects.get(id=id)

    currentRoom.participants.add(request.user)
    return redirect('room', currentRoom.id)

@login_required(login_url='login') 
def leaveRoom(request, id):
    currentRoom = Room.objects.get(id=id)
    roomParticipants = currentRoom.participants.all()

    if currentRoom.host == request.user:
        messages.error(request, "You are the owner of this room, you can't leave the room.")
        return redirect('room', currentRoom.id)

    if not request.user in roomParticipants:
        messages.error(request, 'You are not a participant of this room!')
        return redirect('room', currentRoom.id)

    currentRoom.participants.remove(request.user)
    return redirect('index')

@login_required(login_url='login')
def createRoom(request):
    room = RoomForm()
    if request.method == 'POST':
        room = RoomForm(request.POST)
        if room.is_valid():
            form = room.save(commit=False)
            print(form.participants)
            form.host = request.user
            form.save()
            form.participants.add(request.user)
            return redirect('room', form.id)
    context = {
        'form': room,
    }
    return render(request, 'Base/create.html', context)

@login_required(login_url='login')
def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    if request.user != room.host:
        return redirect('room', room.id)

    if request.method == 'POST':
        room.delete()
        return redirect('index')

    context = {
        'obj': room,
    }
    return render(request, 'Base/delete.html', context)

@login_required(login_url='login')
def editRoom(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return redirect('room', room.id)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            newroom = form.save()
            return redirect('room', newroom.id)

    context = {
        'form': form,
        'room': room,
    }    
    return render(request, 'Base/edit-room.html', context)

def loginPage(request):
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'Could not find user')
            return redirect('login')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Incorrect password!')
            return redirect('login')

    context = {
        'form': form
    }
    return render(request, 'Base/login.html', context)

def registerPage(request):
    form = RegisterForm()

    context = {
        'form': form
    }

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.set_password(form.cleaned_data['password'])
            if User.objects.filter(username=user.username):
                messages.error(request, 'Username is already regiestered!')
                return redirect('register')
            form.save()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Email is already registered!')

    return render(request, 'Base/register.html', context) 

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')

def profile(request, username):
    user = User.objects.get(username=username)
    rooms = Room.objects.filter(Q(host=user) | Q(participants=user)).order_by('-updated')
    activities = Messages.objects.filter(user=user)
    print(activities)

    context = {
        'user': user,
        'rooms': rooms,
        'activities': activities,
    }
    return render(request, 'Base/profile.html', context)