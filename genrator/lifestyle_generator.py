"""
lifestyle_generator.py

Generates hidden lifestyle variables.
These variables are NOT saved in the dataset.
"""

import random

def generate_housing_status(age):

    choices = [
        "Lives with Parents",
        "Rental",
        "Own House",
        "Company Accommodation"
    ]

    # Younger employees are more likely to live with parents
    if age <= 25:
        probabilities = [0.45, 0.40, 0.05, 0.10]

    elif age <= 35:
        probabilities = [0.15, 0.60, 0.15, 0.10]

    elif age <= 45:
        probabilities = [0.05, 0.45, 0.40, 0.10]

    else:
        probabilities = [0.03, 0.30, 0.60, 0.07]

    return random.choices(
        choices,
        weights=probabilities,
        k=1
    )[0]
    
def generate_marital_status(age):

    if age <= 25:
        return random.choices(
            ["Single","Married"],
            weights=[0.90,0.10]
        )[0]

    elif age <= 35:
        return random.choices(
            ["Single","Married"],
            weights=[0.40,0.60]
        )[0]

    else:
        return random.choices(
            ["Single","Married"],
            weights=[0.15,0.85]
        )[0]
        
def generate_vehicle():

    return random.choices(

        [
            "None",
            "Bike",
            "Car"
        ],

        weights=[0.25,0.45,0.30],

        k=1

    )[0]
    
def generate_lifestyle(age):

    return {

        "Housing": generate_housing_status(age),

        "Marital_Status": generate_marital_status(age),

        "Vehicle": generate_vehicle()

    }
    
if __name__ == "__main__":

    print(generate_lifestyle(23))

    print(generate_lifestyle(32))

    print(generate_lifestyle(50))