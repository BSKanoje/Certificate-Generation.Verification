from django.shortcuts import render, redirect
from .models import Company
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from datetime import date
from subscriptions.models import CompanySubscription, PricingPlan

def home_view(request):
    user = request.user

    try:
        subscription = CompanySubscription.objects.get(company=user)
        days_left = (subscription.expiry_date - date.today()).days if subscription.expiry_date else 0
        remaining_certificates = subscription.remaining_certificates()
    except CompanySubscription.DoesNotExist:
        subscription = None
        days_left = 0
        remaining_certificates = 0

    plans = PricingPlan.objects.all()

    context = {
        'company': user,
        'subscription': subscription,
        'plans': plans,
        'days_left': days_left,
        'remaining_certificates': remaining_certificates
    }

    return render(request, 'home.html', context)



# Create your views here.
def about(request):
    return render(request, 'about.html')


def register(request):
    if request.method == 'POST':
        company_name = request.POST['company_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        if Company.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        if Company.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already registered.')
            return redirect('register')

        company = Company.objects.create(
            company_name=company_name,
            email=email,
            phone=phone,
            password=make_password(password)  # securely hash password
        )
        login(request, company)
        return redirect('home')  # or your dashboard URL

    return render(request, 'register.html')





User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('login')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Change to your dashboard/homepage
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset-password')  # Redirect back to reset page

        # Update the user's password
        user = request.user
        user.set_password(new_password)  # Use set_password to hash the password correctly
        user.save()

        # Keep the user logged in after password change
        update_session_auth_hash(request, user)

        # Provide success message
        messages.success(request, "Password updated successfully.")
        # return redirect('home')  # Redirect to the homepage or desired page

    return render(request, 'reset_password.html')
