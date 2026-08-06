import pandas as pd

from config import NUM_EMPLOYEES

from employee_generator import generate_employee
from salary_generator import generate_salary
from deduction_generator import generate_deductions
from lifestyle_generator import generate_lifestyle
from expense_generator import generate_expenses
from investment_generator import generate_investments
from class_generator import generate_class

def generate_employee_record(index):

    # ---------------------------------
    # Employee Details
    # ---------------------------------

    employee = generate_employee(index)

    # ---------------------------------
    # Salary
    # ---------------------------------

    salary = generate_salary(

        employee["Department"],

        employee["Years_of_Experience"]

    )

    employee["Monthly_Salary"] = salary
    
    # ---------------------------------
    # Deductions
    # ---------------------------------

    deductions = generate_deductions(salary)

    employee.update(deductions)
    
    # ---------------------------------
    # Lifestyle (Hidden Variables)
    # ---------------------------------

    lifestyle = generate_lifestyle(

        employee["Age"]

    )
    
    # ---------------------------------
    # Expenses
    # ---------------------------------

    expenses = generate_expenses(

        net_salary=employee["Net_Salary"],

        persona=employee["Persona"],

        housing=lifestyle["Housing"],

        marital_status=lifestyle["Marital_Status"],

        vehicle=lifestyle["Vehicle"]

    )

    employee.update(expenses)
    
    
    # ---------------------------------
    # Savings & Investments
    # ---------------------------------

    investment = generate_investments(

        net_salary=employee["Net_Salary"],

        total_expenditure=employee["Total_Expenditure"],

        persona=employee["Persona"]

    )

    employee.update(investment)
    
    
    # ---------------------------------
    # Financial Class
    # ---------------------------------

    financial_class = generate_class(

        net_salary=employee["Net_Salary"],

        total_expenditure=employee["Total_Expenditure"],

        emi=employee["EMI_or_Loan_Payment"],

        savings=employee["Savings_Amount"],

        investments=employee["Investments"],

        emergency_fund=employee["Emergency_Fund"]

    )

    employee.update(financial_class)
    
    # ---------------------------------
    # Remove Hidden Columns
    # ---------------------------------

    employee.pop("Persona")

    employee.pop("Emergency_Fund")

    employee.pop("Remaining_Income")

    return employee

def generate_dataset():

    records = []

    for i in range(1, NUM_EMPLOYEES + 1):

        records.append(

            generate_employee_record(i)

        )

    df = pd.DataFrame(records)

    return df

if __name__ == "__main__":

    df = generate_dataset()

    print(df.head())

    print()

    print(df.shape)

    df.to_csv(

        "employee_financial_health.csv",

        index=False

    )

    print()

    print("Dataset Generated Successfully!")