def get_new_plan_price(new_plan):
    # Example: Return pricing based on the plan name
    plan_prices = {
        'basic': 10.00,
        'premium': 20.00,
        'enterprise': 50.00,
    }
    return plan_prices.get(new_plan, 0.00)  # Return 0 if the plan is invalid
