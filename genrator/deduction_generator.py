"""
deduction_generator.py

Generates employee payroll deductions.

Outputs:
- Income Tax
- PF Contribution
- Insurance Deduction
- Other Deductions
- Net Salary
"""

import random

def calculate_income_tax(monthly_salary):

    annual_income = monthly_salary * 12

    tax = 0

    slabs = [
        (400000, 0.00),
        (800000, 0.05),
        (1200000, 0.10),
        (1600000, 0.15),
        (2000000, 0.20),
        (2400000, 0.25),
        (float("inf"), 0.30)
    ]

    previous_limit = 0
    remaining_income = annual_income

    for limit, rate in slabs:

        taxable_income = min(remaining_income, limit - previous_limit)

        if taxable_income > 0:
            tax += taxable_income * rate

        remaining_income -= taxable_income
        previous_limit = limit

        if remaining_income <= 0:
            break

    return round(tax / 12)

def calculate_pf(monthly_salary):

    basic_salary = monthly_salary * 0.50

    pf = basic_salary * 0.12

    return round(pf)

def calculate_insurance(monthly_salary):

    if monthly_salary < 60000:
        return random.randint(700,1200)

    elif monthly_salary < 100000:
        return random.randint(1200,2200)

    else:
        return random.randint(2200,4000)
    
def calculate_professional_tax(monthly_salary):

    if monthly_salary < 15000:
        return 0

    return 200

def calculate_other_deductions():

    transport_allowance = random.randint(300,800)

    welfare_fund = random.randint(100,400)

    meal_card = random.randint(0,1200)

    return (
        transport_allowance
        + welfare_fund
        + meal_card
    )

def generate_deductions(monthly_salary):

    income_tax = calculate_income_tax(monthly_salary)

    pf = calculate_pf(monthly_salary)

    insurance = calculate_insurance(monthly_salary)

    professional_tax = calculate_professional_tax(monthly_salary)

    other_deductions = calculate_other_deductions()

    total_other = professional_tax + other_deductions

    net_salary = (
        monthly_salary
        - income_tax
        - pf
        - insurance
        - total_other
    )

    return {

        "Income_Tax": income_tax,

        "PF_Contribution": pf,

        "Insurance_Deduction": insurance,

        "Other_Deductions": total_other,

        "Net_Salary": round(net_salary)

    }

if __name__ == "__main__":

    salary = 120000

    deductions = generate_deductions(salary)

    print("Monthly Salary :", salary)

    print()

    for key, value in deductions.items():

        print(f"{key:<25}: ₹{value:,}")