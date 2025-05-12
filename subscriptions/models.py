from django.db import models
from django.conf import settings
from datetime import date, timedelta

class PricingPlan(models.Model):
    name = models.CharField(max_length=50)
    certificate_limit = models.PositiveIntegerField()
    template_limit = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class CompanySubscription(models.Model):
    company = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(PricingPlan, on_delete=models.SET_NULL, null=True)
    certificates_used = models.PositiveIntegerField(default=0)
    start_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)  # Track active status
    next_plan = models.CharField(max_length=100, blank=True, null=True)  # Store upgraded plan if applicable
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Failed', 'Failed')], default='Pending')
    payment_reference = models.CharField(max_length=100, null=True, blank=True)

    def is_subscription_active(self):
        """ Returns whether the subscription is currently active """
        return self.expiry_date >= date.today()

    def remaining_certificates(self):
        """ Returns the remaining certificates allowed based on the plan """
        if not self.plan:
            return 0
        return self.plan.certificate_limit - self.certificates_used

    def renew(self, days=30):
        """ Function to renew the subscription for additional days """
        self.expiry_date = self.expiry_date + timedelta(days=days)
        self.save()

    def upgrade_plan(self, new_plan: PricingPlan):
        """ Upgrade to a new pricing plan and adjust the expiry date """
        if new_plan != self.plan:
            self.plan = new_plan
            self.next_plan = new_plan.name  # Store the upgraded plan name
            # Extend the expiry date for the new plan (you can adjust the logic as needed)
            self.expiry_date = date.today() + timedelta(days=new_plan.certificate_limit)  # Example, add days from new plan's certificate limit
            self.save()


    def __str__(self):
        return f"{self.company.company_name} - {self.plan.name if self.plan else 'No Plan'}"
