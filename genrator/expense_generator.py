"""
expense_generator.py

Generates monthly expenses based on
employee financial behaviour.
"""

import random

PERSONA_PROFILE = {

    "Frugal Saver": {
        "expenses": {
            "rent": (0.18,0.24),
            "grocery": (0.08,0.12),
            "emi": (0.00,0.08),
            "entertainment": (0.02,0.05),
            "other": (0.02,0.05)
        },
        "saving_rate": (0.50,0.70),
        "investment_rate": (0.15,0.25)
    },

    "Balanced Planner": {
        "expenses": {
            "rent": (0.22,0.28),
            "grocery": (0.10,0.14),
            "emi": (0.08,0.15),
            "entertainment": (0.05,0.08),
            "other": (0.04,0.07)
        },
        "saving_rate": (0.35,0.50),
        "investment_rate": (0.15,0.25)
    },

    "High Earner High Spender": {
        "expenses": {
            "rent": (0.28,0.35),
            "grocery": (0.10,0.14),
            "emi": (0.18,0.30),
            "entertainment": (0.10,0.18),
            "other": (0.06,0.10)
        },
        "saving_rate": (0.10,0.25),
        "investment_rate": (0.10,0.20)
    },

    "Debt Burdened": {
        "expenses": {
            "rent": (0.22,0.30),
            "grocery": (0.10,0.14),
            "emi": (0.30,0.45),
            "entertainment": (0.02,0.05),
            "other": (0.04,0.08)
        },
        "saving_rate": (0.00,0.10),
        "investment_rate": (0.00,0.05)
    },

    "Aggressive Investor": {
        "expenses": {
            "rent": (0.20,0.26),
            "grocery": (0.08,0.12),
            "emi": (0.05,0.12),
            "entertainment": (0.04,0.07),
            "other": (0.03,0.06)
        },
        "saving_rate": (0.20,0.35),
        "investment_rate": (0.40,0.60)
    }

}

def calculate_rent(net_salary, housing, ratios, spending_factor):

    if housing == "Lives with Parents":
        return 0

    elif housing == "Own House":
        return 0

    elif housing == "Company Accommodation":

        return round(
            net_salary *
            random.uniform(0.05, 0.12)
        )

    else:

        return round(
            net_salary *
            random.uniform(*ratios["rent"]) *
            spending_factor
        )
        
def calculate_grocery(
    net_salary,
    marital_status,
    ratios,
    spending_factor
):

    grocery_ratio = random.uniform(
        *ratios["grocery"]
    )

    if marital_status == "Married":
        grocery_ratio += 0.04

    return round(
        net_salary *
        grocery_ratio *
        spending_factor
    )
    
def calculate_emi(
    net_salary,
    housing,
    vehicle,
    ratios,
    spending_factor
):
    """
    Calculate EMI based on housing and vehicle ownership.

    Priority:
    1. Home Loan
    2. Car Loan
    3. Bike Loan
    4. Personal Loan (persona based)

    Returns:
        EMI amount (int)
    """

    emi = 0

    # -----------------------------
    # Home Loan EMI
    # -----------------------------
    if housing == "Own House":

        if random.random() < 0.80:

            emi = round(
                net_salary *
                random.uniform(0.18, 0.35)
            )

    # -----------------------------
    # Car Loan EMI
    # -----------------------------
    elif vehicle == "Car":

        if random.random() < 0.70:

            emi = round(
                net_salary *
                random.uniform(0.08, 0.18)
            )

    # -----------------------------
    # Bike Loan EMI
    # -----------------------------
    elif vehicle == "Bike":

        if random.random() < 0.40:

            emi = round(
                net_salary *
                random.uniform(0.03, 0.08)
            )

    # -----------------------------
    # Personal Loan EMI
    # -----------------------------
    else:

        if random.random() < 0.20:

            emi = round(
                net_salary *
                random.uniform(
                    *ratios["emi"]
                ) *
                spending_factor
            )

    # Safety Check
    emi = min(emi, round(net_salary * 0.45))

    return emi

def calculate_entertainment(
    net_salary,
    marital_status,
    ratios,
    spending_factor
):

    entertainment_ratio = random.uniform(
        *ratios["entertainment"]
    )

    if marital_status == "Single":
        entertainment_ratio += 0.03

    return round(
        net_salary *
        entertainment_ratio *
        spending_factor
    )
    
def calculate_other_expenses(
    net_salary,
    ratios,
    spending_factor
):

    return round(

        net_salary *

        random.uniform(
            *ratios["other"]
        )

        * spending_factor

    )
    
def generate_expenses(
    net_salary,
    persona,
    housing,
    marital_status,
    vehicle
):

    profile = PERSONA_PROFILE[persona]

    ratios = profile["expenses"]

    spending_factor = random.uniform(
        0.90,
        1.10
    )

    rent = calculate_rent(
        net_salary,
        housing,
        ratios,
        spending_factor
    )

    grocery = calculate_grocery(
        net_salary,
        marital_status,
        ratios,
        spending_factor
    )

    emi = calculate_emi(
        net_salary,
        housing,
        vehicle,
        ratios,
        spending_factor
    )

    entertainment = calculate_entertainment(
        net_salary,
        marital_status,
        ratios,
        spending_factor
    )

    other = calculate_other_expenses(
        net_salary,
        ratios,
        spending_factor
    )

    total = (
        rent
        + grocery
        + emi
        + entertainment
        + other
    )

    return {

        "Rent_Expense": rent,

        "Grocery_Expense": grocery,

        "EMI_or_Loan_Payment": emi,

        "Entertainment_Expense": entertainment,

        "Other_Expenses": other,

        "Total_Expenditure": total

    }  

if __name__ == "__main__":

    result = generate_expenses(

        net_salary=90000,

        persona="Balanced Planner",

        housing="Rental",

        marital_status="Single",

        vehicle="Bike"

    )

    for key, value in result.items():

        print(f"{key:<30}: ₹{value:,}")