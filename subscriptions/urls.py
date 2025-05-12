# urls.py

from django.urls import path
from . import views  # Import your views file

urlpatterns = [
    # URL for renewing the subscription
    path('renew/<int:subscription_id>/', views.renew_subscription, name='renew'),

    # URL for upgrading the subscription
    path('upgrade_plan/<int:subscription_id>/<str:plan_name>/', views.upgrade_plan, name='upgrade_plan'),
    # You can add other URL routes for subscription-related views here
]
