"""
employee_generator.py

Generates:
- Employee ID
- Employee Name
- Age
- Years of Experience
- Department
- Persona
"""

import random
import numpy as np

from config import (
    DEPARTMENTS,
    PERSONA_MAPPING,
    MIN_AGE,
    MAX_AGE
)

# --------------------------------------------------
# Sample Indian Names
# --------------------------------------------------

FIRST_NAMES = [

    # Male
    "Aarav","Vivaan","Aditya","Arjun","Ayaan","Atharv","Vihaan","Krishna",
    "Sai","Ishaan","Rohan","Rahul","Amit","Akash","Nikhil","Karan","Harsh",
    "Ayush","Yash","Siddharth","Ankit","Abhishek","Mohit","Varun","Rajat",
    "Manish","Rakesh","Vivek","Deepak","Prateek","Shubham","Gaurav","Mayank",
    "Saurabh","Tarun","Rishabh","Lokesh","Dev","Vikram","Ravi","Sumit",
    "Hemant","Ashish","Nitin","Pankaj","Rohit","Aakash","Shivam","Aman",
    "Kunal","Anurag","Lakshay","Dhruv","Parth","Yuvraj","Tushar","Kartik",

    # Female
    "Priya","Anjali","Sneha","Neha","Riya","Shreya","Sakshi","Tanvi",
    "Aisha","Nisha","Ritika","Pooja","Megha","Kavya","Ananya","Diya",
    "Khushi","Ishita","Simran","Palak","Muskan","Aditi","Nandini",
    "Shruti","Swati","Komal","Rashmi","Payal","Preeti","Bhavna",
    "Vaishnavi","Mansi","Rupal","Garima","Sonali","Divya","Namrata",
    "Jyoti","Monika","Reema","Pallavi","Sonia","Nikita","Charu",
    "Sanya","Trisha","Avantika","Saloni","Vidhi","Prachi"

]

LAST_NAMES = [

    "Sharma","Verma","Gupta","Agarwal","Khandelwal","Singh","Patel",
    "Joshi","Jain","Kapoor","Mehta","Bansal","Kulkarni","Reddy",
    "Nair","Iyer","Malhotra","Chopra","Yadav","Mishra","Pandey",
    "Tiwari","Dubey","Shukla","Saxena","Srivastava","Trivedi",
    "Chaudhary","Chauhan","Rathore","Solanki","Rajput","Saini",
    "Purohit","Maheshwari","Somani","Daga","Bajaj","Goel","Mittal",
    "Arora","Seth","Khanna","Nagpal","Kohli","Bedi","Gill","Sandhu",
    "Bhardwaj","Rawat","Tomar","Parmar","Jadhav","More","Shinde",
    "Pawar","Deshmukh","Naidu","Shetty","Menon","Pillai","Thomas",
    "George","Mathew","Fernandes","D'Souza","Das","Bose","Mukherjee",
    "Chatterjee","Roy","Banerjee","Ghosh","Pradhan","Mohanty",
    "Swain","Behera","Sahu","Soni","Kumawat","Lodha","Bohra",
    "Mundra","Porwal","Lakhotia","Bagri","Jindal","Tayal","Narang",
    "Wadhwa","Sabharwal","Suri","Bhatia","Khurana","Ahuja"

]

# --------------------------------------------------
# Employee ID
# --------------------------------------------------

def generate_employee_id(index):

    return f"EMP{index:05d}"

# --------------------------------------------------
# Employee Name
# --------------------------------------------------

def generate_employee_name():

    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)

    # 15% chance of having a middle name
    if random.random() < 0.15:
        middle = random.choice(FIRST_NAMES)
        return f"{first} {middle} {last}"

    return f"{first} {last}"

# --------------------------------------------------
# Age
# --------------------------------------------------

def generate_age():

    return random.randint(MIN_AGE, MAX_AGE)

# --------------------------------------------------
# Experience
# --------------------------------------------------

def generate_experience(age):
    if age <= 25:
        return random.randint(0, 3)

    elif age <= 30:
        return random.randint(2, 7)

    elif age <= 35:
        return random.randint(5, 12)

    elif age <= 40:
        return random.randint(8, 18)

    elif age <= 50:
        return random.randint(15, 28)

    else:
        return random.randint(22, 38)

# --------------------------------------------------
# Department
# --------------------------------------------------

DEPARTMENT_WEIGHTS = {
    "IT": 0.18,
    "Data Science": 0.08,
    "Cyber Security": 0.05,
    "Finance": 0.10,
    "HR": 0.08,
    "Sales": 0.18,
    "Marketing": 0.10,
    "Operations": 0.13,
    "Customer Support": 0.07,
    "Product Management": 0.03
}
    
def assign_department():

    departments = list(DEPARTMENT_WEIGHTS.keys())
    weights = list(DEPARTMENT_WEIGHTS.values())

    return random.choices(
        departments,
        weights=weights,
        k=1
    )[0]

# --------------------------------------------------
# Persona
# --------------------------------------------------

def assign_persona(department):

    personas = list(PERSONA_MAPPING[department].keys())

    probabilities = list(PERSONA_MAPPING[department].values())
  
    return str(np.random.choice(personas, p=probabilities))

# --------------------------------------------------
# Generate Employee
# --------------------------------------------------

def generate_employee(index):

    age = generate_age()

    experience = generate_experience(age)

    department = assign_department()

    persona = assign_persona(department)

    employee = {

        "EmployeeID": generate_employee_id(index),

        "EmployeeName": generate_employee_name(),

        "Age": age,

        "Years_of_Experience": experience,

        "Department": department,

        "Persona": persona

    }

    return employee

# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    for i in range(1,11):

        print(generate_employee(i))