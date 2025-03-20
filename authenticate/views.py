from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login, logout
from .models import MyUser, Student, Faculty
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'authenticate/home.html')

def faculty_login_page(request):
    if request.method=='POST':
        username = request.POST['faculty_id']
        password = request.POST['password']

        user_found = MyUser.objects.filter(username=username.upper()).exists()

        if not user_found:
            messages.error(request, "User not Found")
            return render(request, 'authenticate/faculty_login_page.html')
        
        user = authenticate(request, username=username, password=password)

        if user is not None and user.user_type == MyUser.FACULTY:
            login(request, user)
            return redirect('faculty_dashboard')
        
        else:
            messages.error(request, "You are not an Authorized User")
            return render(request, 'authenticate/faculty_login_page.html')
    
    else:
        return render(request, 'authenticate/faculty_login_page.html')

def student_login_page(request):
    if request.method == 'POST':
        username = request.POST['admission_no']
        password = request.POST['password']
        username = username.upper()

        user = authenticate(request, username=username, password=password)
        print(user)
        
        if user is not None:
            if user.user_type == MyUser.STUDENT:
                login(request, user)
                #request.session.set_expiry(60*60*24) #logout after 1 day
                return redirect('student_dashboard') 
            else:
                messages.error(request, 'You are not a valid student user.')
                return render(request, 'authenticate/student_login_page.html')
        else:
            messages.error(request, 'Invalid credentials.')
            return render(request, 'authenticate/student_login_page.html')

    else:
        return render(request, 'authenticate/student_login_page.html')


def logout_user(request):
    logout(request)
    return redirect('home')