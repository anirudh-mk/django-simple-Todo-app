from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Task
from datetime import date
from django.contrib.auth.decorators import login_required


# Create your views here.

# RegistrationPage Request

def register(request):
    if request.method == 'POST':

        # Accept data from Registration page

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        # if user enter username password email...
        if username and email and password and confirm_password is not None:

            if password == confirm_password:

                # Check user is existed
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'username is already existed')
                    return redirect('/register')

                # Check mail is existed
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'email is already taken')
                    return redirect('/register')

                # Push data to server
                else:
                    user = User.objects.create_user(username=username, email=email, password=password,
                                                    first_name=first_name, last_name=last_name)
                    user.save()

            else:
                messages.info(request, 'Password is miss match')
                # return render(request, 'register.html')
                return redirect('/register')

            # Return to login page
            return redirect('/login')

        # if user not enter username password email...
        else:
            messages.info(request, 'Please provide valid information')
            return render(request, 'register.html')

    else:
        return render(request, 'register.html')


# LoginPage Request

def login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        # Check is user is not non
        if user is not None:
            auth.login(request, user)
            return redirect('/home')

        # if user is none
        else:
            messages.info(request, 'invalid username or password')
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')


# HomePage Request

@login_required(login_url='/login')
def home(request):
    if request.method == 'POST':

        task_name = request.POST['task_name']
        task_description = request.POST['task_description']
        due_date = request.POST['due_date']
        status = 'pending'

        # Push Data Server
        task = Task(task_name=task_name, task_description=task_description, due_date=due_date, status=status)
        task.save()

        # Redirect Page
        return redirect('/home')

    else:
        # Access all data from server
        tasks = Task.objects.all()

        # access all database dictionary
        database = tasks.values()

        # Access Today Date
        today = date.today()

        # convert List to dictionary
        for database_dict in database:

            if database_dict['status'] == 'pending':
                task_date = database_dict['due_date']

                # Compare Current Date with Due date
                if today > task_date:
                    print(database_dict['task_name'])

                    # Make Tasks status as expired
                    for _ in database_dict:
                        Task.objects.filter(id=database_dict['id']).update(status='expired')

        return render(request, 'home.html', {'tasks': tasks})


# Logout request

def logout(request):
    auth.logout(request)
    return redirect('/login')


# Task Complete Request

def complete(request):
    # Get Button ID using GET Methode
    button_id = request.GET.get('id')

    # Change Task Status to Complete
    Task.objects.filter(id=button_id).update(status='complete')

    return redirect('/home')


# Task Delete Request

def delete(request):
    # Get Button ID using GET Methode
    button_id = request.GET.get('id')

    # Delete Task
    Task.objects.filter(id=button_id).delete()

    return redirect('/home')
