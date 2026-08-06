import random
import numpy as np

# -------------------------------
# Random Seed
# -------------------------------

RANDOM_STATE = 42

random.seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)

# -------------------------------
# Dataset Size
# -------------------------------

NUM_EMPLOYEES = 10000

# -------------------------------
# Departments
# -------------------------------

DEPARTMENTS = {
    "HR": {
        "base_salary": 40000,
        "max_salary": 70000,
        "increment": 1200
    },

    "Sales": {
        "base_salary": 45000,
        "max_salary": 85000,
        "increment": 1600
    },

    "Marketing": {
        "base_salary": 50000,
        "max_salary": 90000,
        "increment": 1700
    },

    "Operations": {
        "base_salary": 50000,
        "max_salary": 95000,
        "increment": 1800
    },

    "Customer Support": {
        "base_salary": 35000,
        "max_salary": 60000,
        "increment": 1000
    },

    "Finance": {
        "base_salary": 70000,
        "max_salary": 130000,
        "increment": 2200
    },

    "IT": {
        "base_salary": 80000,
        "max_salary": 150000,
        "increment": 2500
    },

    "Data Science": {
        "base_salary": 90000,
        "max_salary": 170000,
        "increment": 3000
    },

    "Cyber Security": {
        "base_salary": 95000,
        "max_salary": 180000,
        "increment": 3200
    },

    "Product Management": {
        "base_salary": 120000,
        "max_salary": 220000,
        "increment": 3500
    }
}

# -------------------------------
# Persona Distribution
# -------------------------------

PERSONA_MAPPING = {

    "HR": {
        "Balanced Planner":0.40,
        "Frugal Saver":0.25,
        "High Earner High Spender":0.15,
        "Debt Burdened":0.15,
        "Aggressive Investor":0.05
    },

    "Sales":{
        "Balanced Planner":0.30,
        "High Earner High Spender":0.35,
        "Frugal Saver":0.10,
        "Debt Burdened":0.20,
        "Aggressive Investor":0.05
    },

    "Marketing":{
        "Balanced Planner":0.40,
        "High Earner High Spender":0.25,
        "Frugal Saver":0.15,
        "Debt Burdened":0.15,
        "Aggressive Investor":0.05
    },

    "Operations":{
        "Balanced Planner":0.35,
        "Frugal Saver":0.25,
        "Debt Burdened":0.20,
        "High Earner High Spender":0.15,
        "Aggressive Investor":0.05
    },

    "Customer Support":{
        "Balanced Planner":0.30,
        "Debt Burdened":0.30,
        "Frugal Saver":0.20,
        "High Earner High Spender":0.15,
        "Aggressive Investor":0.05
    },

    "Finance":{
        "Balanced Planner":0.40,
        "Frugal Saver":0.30,
        "Aggressive Investor":0.15,
        "High Earner High Spender":0.10,
        "Debt Burdened":0.05
    },

    "IT":{
        "Balanced Planner":0.40,
        "Aggressive Investor":0.20,
        "Frugal Saver":0.20,
        "High Earner High Spender":0.15,
        "Debt Burdened":0.05
    },

    "Data Science":{
        "Balanced Planner":0.45,
        "Aggressive Investor":0.20,
        "Frugal Saver":0.20,
        "High Earner High Spender":0.10,
        "Debt Burdened":0.05
    },

    "Cyber Security":{
        "Balanced Planner":0.40,
        "Aggressive Investor":0.25,
        "Frugal Saver":0.20,
        "High Earner High Spender":0.10,
        "Debt Burdened":0.05
    },

    "Product Management":{
        "Balanced Planner":0.35,
        "High Earner High Spender":0.30,
        "Aggressive Investor":0.20,
        "Frugal Saver":0.10,
        "Debt Burdened":0.05
    }

}

# -------------------------------
# Age Limits
# -------------------------------

MIN_AGE = 22
MAX_AGE = 60