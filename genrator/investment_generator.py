"""
investment_generator.py

Generates:
- Savings Amount
- Investments
- Remaining Cash
"""

import random

from expense_generator import PERSONA_PROFILE

def calculate_remaining_income(
    net_salary,
    total_expenditure
):

    remaining_income = (
        net_salary -
        total_expenditure
    )

    return max(0, round(remaining_income))

def calculate_savings(
    remaining_income,
    profile
):

    saving_rate = random.uniform(
        *profile["saving_rate"]
    )

    savings = round(
        remaining_income *
        saving_rate
    )

    return savings

def calculate_investments(
    remaining_after_savings,
    profile
):

    investment_rate = random.uniform(
        *profile["investment_rate"]
    )

    investments = round(
        remaining_after_savings *
        investment_rate
    )

    return investments

def calculate_emergency_fund(
    remaining_income,
    savings,
    investments
):

    emergency_fund = (

        remaining_income
        - savings
        - investments

    )

    return round(
        max(0, emergency_fund)
    )
    
def generate_investments(

    net_salary,

    total_expenditure,

    persona

):

    profile = PERSONA_PROFILE[persona]

    remaining_income = calculate_remaining_income(

        net_salary,

        total_expenditure

    )

    savings = calculate_savings(

        remaining_income,

        profile

    )

    remaining_after_savings = (

        remaining_income

        - savings

    )

    investments = calculate_investments(

        remaining_after_savings,

        profile

    )

    emergency_fund = calculate_emergency_fund(

        remaining_income,

        savings,

        investments

    )

    return {

        "Remaining_Income": remaining_income,

        "Savings_Amount": savings,

        "Investments": investments,

        "Emergency_Fund": emergency_fund

    }
    
if __name__ == "__main__":

    result = generate_investments(

        net_salary=90000,

        total_expenditure=52000,

        persona="Balanced Planner"

    )

    for key, value in result.items():

        print(f"{key:<25}: ₹{value:,}")