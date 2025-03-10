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
                return redirect('freelance_dashboard')  # Replace with your actual freelancer dashboard view name
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
                        return redirect('freelance_dashboard')  # Replace with your actual freelancer dashboard view name
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



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return render(request, 'error.html', {'message': 'Profile does not exist'})

    full_name = f"{request.user.first_name} {request.user.last_name}"
    context = {
        'profile': profile,
        'full_name': full_name,
    }

    if profile.account_type == 'freelancer':
        template = 'freelancer_profile.html'
    else:
        template = 'client_profile.html'

    return render(request, template, context)



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages

@login_required
def edit_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return render(request, 'error.html', {'message': 'Profile does not exist'})

    if request.method == 'POST':
        # Update User Fields
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.save()

        # Update Profile Fields
        profile.country = request.POST.get('country', profile.country)
        profile.bio = request.POST.get('bio', profile.bio)
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        if profile.account_type == 'freelancer':
            profile.professional_title = request.POST.get('professional_title', profile.professional_title)
            profile.skills = request.POST.get('skills', profile.skills)
            profile.experience_level = request.POST.get('experience_level', profile.experience_level)
            profile.portfolio = request.POST.get('portfolio', profile.portfolio)
            profile.certifications = request.POST.get('certifications', profile.certifications)
        
        elif profile.account_type == 'client':
            profile.company_name = request.POST.get('company_name', profile.company_name)
            profile.website = request.POST.get('website', profile.website)
            profile.industry = request.POST.get('industry', profile.industry)

        profile.save()
        messages.success(request, "Your profile has been updated successfully!")
        return redirect('profile_view')

    context = {
        'profile': profile
    }
    return render(request, 'edit_profile.html', context)
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Profile


def generate_otp():
    return str(random.randint(100000, 999999))  # Generate a 6-digit OTP


@login_required
def send_otp(request):
    user = request.user
    profile = user.profile

    # Check if the user is already verified
    if profile.verified:
        messages.success(request, "Your account is already verified.")
        return redirect('freelance_profile')

    # Generate OTP
    otp = generate_otp()
    profile.otp = otp  # Save OTP to the profile
    profile.save()

    # Send OTP via email
    subject = "Your Freelenso Verification Code"
    message = f"Your OTP is: {otp}. Enter this code to verify your account."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    messages.info(request, "An OTP has been sent to your email.")
    return redirect('verify_otp')  # Redirect to OTP verification page

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def verify_otp(request):
    if request.method == 'POST':
        input_otp = request.POST.get('otp')
        profile = request.user.profile

        # Check if OTP matches
        if input_otp == profile.otp:
            profile.verified = True
            profile.otp = None  # Clear OTP after successful verification
            profile.save()
            messages.success(request, "Your account has been successfully verified!")

            # Redirect based on user account type
            if profile.account_type == 'freelancer':
                return redirect('prodile_view')
            elif profile.account_type == 'client':
                return redirect('client_profile')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_otp.html')  # Render OTP verification page
