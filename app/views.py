from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

def index(request):
    return render (request, "index.html")

def register(request):
    print(request.POST)

    errors=User.objects.register_validator(request.POST)
    print(errors)

    if len(errors)>0:
        print('these are the errors')
    
        for key, value in errors.items():
            messages.error(request, value, key)
        
        return redirect('/')
    else:
        
        print(request.POST['password'])
        hash_browns = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print('hash_browns: ', hash_browns)
        
        new_user = User.objects.create(
            email=request.POST['email'],
            password=hash_browns,
        )
        
        request.session['user_id'] = new_user.id
        request.session['email'] = new_user.email
        print('*'*50)
        print(new_user.password)

    

    return redirect('/dashboard')

def login(request):
    print(request.POST)
    #errors=User.objects.login_validator(username=request.POST['login_email'])
    potential_users=User.objects.filter(email=request.POST['login_email'])

    if len(potential_users)==0:
        print('email doesnt exist')
        messages.error(request,"please check email and password")

        return redirect('/')
    if not bcrypt.checkpw(
        request.POST["login_password"].encode(),
        potential_users[0].password.encode(),
        
    ):
        print('bad password')

        messages.error(request,'Please check your email and password')

        return redirect ('/')

    request.session['user_id'] = potential_users[0].id


    return redirect('/dashboard')

def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    context ={
        'all_workouts': Workout.objects.all(),
        'this_user':User.objects.get(id=request.session['user_id'])
    }
    return render (request, 'dashboard.html', context)

def new_workout(request):
    return render(request, 'new_workout.html')

def add_workout(request):
    added_workout = Workout.objects.create(
        name= request.POST["name"],
        description= request.POST["description"],
        workout_creator= User.objects.get(id=request.session['user_id']),
        set1= request.POST["set1"],
        weight1= request.POST['weight1'],
        set2= request.POST["set2"],
        weight2= request.POST['weight2'],
        set3= request.POST["set3"],
        weight3= request.POST['weight3'],
        set4= request.POST["set4"],
        weight4= request.POST['weight4'],
        set5= request.POST["set5"],
        weight5= request.POST['weight5'],
    )
    return redirect ('/dashboard')

def workout_details (request, workout_id):
    context={
        'this_workout': Workout.objects.get(id=workout_id),
    }
    return render (request,'workout_details.html', context)

def profile (request, user_id):
    context={
        'this_user': User.objects.get(id=user_id)
    }
    return render (request,'profile.html',context)

def edit_workout (request, workout_id):
    return render (request,'edit_workout.html')

def delete (request, workout_id):
    Workout.objects.get(id=workout_id).delete()
    return redirect ('/dashboard')