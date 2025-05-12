from django.contrib.auth.decorators import login_required
from .models import PricingPlan, CompanySubscription
from datetime import date, timedelta
from django.utils import timezone
from django.utils.crypto import get_random_string
from .services import get_new_plan_price  
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages

@login_required
def choose_plan(request, id):
    plan = PricingPlan.objects.get(id=id)

    try:
        subscription = CompanySubscription.objects.get(company=request.user)
    except CompanySubscription.DoesNotExist:
        subscription = None

    if subscription:
        if subscription.plan != plan:
            subscription.plan = plan
            subscription.expiry_date = date.today() + timedelta(days=30) 

    else:
        subscription = CompanySubscription(company=request.user)
        subscription.plan = plan
        subscription.certificates_used = 0  # Reset certificate usage for new plan
        subscription.start_date = date.today()
        subscription.expiry_date = timezone.now() + timedelta(days=30)  # Set 30-day expiry for new subscription

    # Save the subscription
    subscription.save()

    # Redirect to dashboard or subscription confirmation page
    return redirect('mock_payment', plan_id=plan.id)  # Replace 'home' with your actual dashboard URL name



@login_required
def plans_view(request):
    plans = PricingPlan.objects.all()
    try:
        subscription = CompanySubscription.objects.get(company=request.user)
    except CompanySubscription.DoesNotExist:
        subscription = None

    context = {
        'plans': plans,
        'subscription': subscription,
    }
    return render(request, 'plans.html', context)






@login_required
def confirm_payment(request, plan_id):
    plan = PricingPlan.objects.get(id=plan_id)
    subscription, created = CompanySubscription.objects.get_or_create(company=request.user)

    # Mock payment logic (you can set the payment status and confirm subscription)
    subscription.payment_status = 'Paid'  # Simulating payment completion
    subscription.save()

    # Redirect to the dashboard
    return redirect('home')


@login_required
def mock_payment(request, plan_id):
    plan = get_object_or_404(PricingPlan, id=plan_id)
    subscription, created = CompanySubscription.objects.get_or_create(
        company=request.user,
        defaults={
        'plan': plan,  # make sure `plan` is defined
        'start_date': timezone.now(),
        'expiry_date': timezone.now() + timedelta(days=30),
        }
        )

    if request.method == "POST":
        # Simulate successful payment
        subscription.plan = plan
        subscription.payment_status = 'Paid'
        subscription.payment_reference = get_random_string(12).upper()
        subscription.start_date = date.today()
        subscription.expiry_date = date.today() + timedelta(days=30)
        subscription.save()
        return redirect('payment_success', id=plan.id)

    return render(request, 'mock_payment.html', {'plan': plan})

@login_required
def payment_success(request, id=None):
    plan = PricingPlan.objects.get(id=id)
    return render(request, 'payment_success.html', {'plan': plan})


# views.py

# views.py

from django.shortcuts import get_object_or_404, render
from .models import CompanySubscription

def renew_subscription(request, subscription_id):
    # Get the subscription object
    subscription = get_object_or_404(CompanySubscription, id=subscription_id)

    # Check if the subscription is active
    
    if subscription.is_subscription_active():  # Correct method call
        # Renew subscription for 30 days
        subscription.renew(30)
        message = f"Your subscription has been renewed. New expiry date: {subscription.expiry_date}"
        success = True
    else:
        message = "Your subscription is not active and cannot be renewed."
        success = False

    # Pass data to the template
    return render(request, 'renew.html', {
        'subscription': subscription,
        'message': message,
        'success': success
    })


def upgrade_plan(request, subscription_id, plan_name):
    subscription = get_object_or_404(CompanySubscription, id=subscription_id)
    plans = PricingPlan.objects.all()

    if request.method == 'POST':
        selected_plan_id = request.POST.get('plan')
        selected_plan = get_object_or_404(PricingPlan, id=selected_plan_id)

        # Update subscription with new plan
        subscription.plan = selected_plan
        subscription.expiry_date = timezone.now() + timezone.timedelta(days=30)  # adjust if your plan has dynamic duration
        subscription.save()

        messages.success(request, f"Subscription upgraded to {selected_plan.name} successfully.")
        return redirect('upgrade_plan', subscription_id=subscription.id, plan_name=selected_plan.name)


    return render(request, 'upgrade_plan.html', {
        'subscription': subscription,
        'plan_name': plan_name,
        'plans': plans
    })

