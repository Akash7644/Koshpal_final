import random
def calculate_savings_rate(
    savings,
    net_salary
):

    if net_salary == 0:
        return 0

    return savings / net_salary

def calculate_investment_rate(
    investments,
    net_salary
):

    if net_salary == 0:
        return 0

    return investments / net_salary

def calculate_expense_ratio(
    total_expenditure,
    net_salary
):

    if net_salary == 0:
        return 1

    return total_expenditure / net_salary

def calculate_emi_ratio(
    emi,
    net_salary
):

    if net_salary == 0:
        return 1

    return emi / net_salary

def calculate_emergency_ratio(
    emergency_fund,
    net_salary
):

    if net_salary == 0:
        return 0

    return emergency_fund / net_salary

def calculate_financial_score(

    savings_rate,

    investment_rate,

    expense_ratio,

    emi_ratio,

    emergency_ratio

):

    score = 0

    # -----------------------
    # Savings
    # -----------------------

    if savings_rate >= 0.25:
        score += 3

    elif savings_rate >= 0.15:
        score += 2

    elif savings_rate >= 0.08:
        score += 1

    # -----------------------
    # Investment
    # -----------------------

    if investment_rate >= 0.15:
        score += 2

    elif investment_rate >= 0.08:
        score += 1

    # -----------------------
    # Expenses
    # -----------------------

    if expense_ratio <= 0.55:
        score += 3

    elif expense_ratio <= 0.70:
        score += 2

    elif expense_ratio <= 0.80:
        score += 1

    # -----------------------
    # EMI
    # -----------------------

    if emi_ratio <= 0.10:
        score += 2

    elif emi_ratio <= 0.20:
        score += 1

    # -----------------------
    # Emergency Fund
    # -----------------------

    if emergency_ratio >= 0.10:
        score += 2

    elif emergency_ratio >= 0.05:
        score += 1

    return score

def assign_class(score):

    if score >= 10:
        return "High"

    elif score >= 6:
        return "Medium"

    else:
        return "Low"
    
import random

def generate_class(

    net_salary,

    total_expenditure,

    emi,

    savings,

    investments,

    emergency_fund

):

    savings_rate = calculate_savings_rate(
        savings,
        net_salary
    )

    investment_rate = calculate_investment_rate(
        investments,
        net_salary
    )

    expense_ratio = calculate_expense_ratio(
        total_expenditure,
        net_salary
    )

    emi_ratio = calculate_emi_ratio(
        emi,
        net_salary
    )

    emergency_ratio = calculate_emergency_ratio(
        emergency_fund,
        net_salary
    )

    score = calculate_financial_score(

        savings_rate,

        investment_rate,

        expense_ratio,

        emi_ratio,

        emergency_ratio

    )

    # Add small realistic uncertainty
    score += random.gauss(0, 0.30)

    financial_class = assign_class(score)

    return {

        "Class": financial_class

    }
    
if __name__ == "__main__":

    result = generate_class(

        net_salary=90000,

        total_expenditure=50000,

        emi=6000,

        savings=18000,

        investments=8000,

        emergency_fund=8000

    )

    print(result)