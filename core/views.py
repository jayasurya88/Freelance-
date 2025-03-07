from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')


def account_selection(request):
    return render(request,'account_selection.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Profile

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            profile = Profile.objects.get(user=user)
            if profile.account_type == 'freelancer':
                return redirect('freelancer_dashboard')  # Replace with your actual freelancer dashboard view name
            else:
                return redirect('client_dashboard')  # Replace with your actual client dashboard view name
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Profile
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        country = request.POST['country']
        account_type = request.GET.get('type', 'freelancer')

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error': 'Email is already taken'})
            else:
                user = User.objects.create_user(username=email, email=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                profile = Profile(user=user, country=country, account_type=account_type)
                profile.save()

                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    if account_type == 'freelancer':
                        return redirect('freelancer_dashboard')  # Replace with your actual freelancer dashboard view name
                    else:
                        return redirect('client_dashboard')  # Replace with your actual client dashboard view name

        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

    account_type = request.GET.get('type', 'freelancer')
    context = {'account_type': account_type}
    return render(request, 'register.html', context)


    account_type = request.GET.get('type', 'freelancer')
    context = {'account_type': account_type}
    return render(request, 'register.html', context)


def home(request):
    return render(request,'register.html')


def freelance_dashboard(request):
    return render(request,'freelance_dashboard.html')



def client_dashboard(request):
    return render(request,'client_dashboard.html')



from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')  # Replace 'home' with your actual home view name
