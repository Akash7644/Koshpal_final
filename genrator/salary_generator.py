import random
from config import DEPARTMENTS


def generate_salary(department, experience):

    dept = DEPARTMENTS[department]

    base = dept["base_salary"]
    increment = dept["increment"]
    maximum = dept["max_salary"]

    # Experience-based salary growth
    salary = base + (experience * increment)

    # Performance multiplier (±5%)
    performance_multiplier = random.uniform(0.95, 1.05)

    salary *= performance_multiplier

    # Market correction
    salary += random.randint(-3000, 3000)

    salary = int(round(salary))

    # Keep within band
    salary = max(base, salary)
    salary = min(maximum, salary)

    return salary


if __name__ == "__main__":

    for exp in [1, 5, 10, 15, 20]:

        print(generate_salary("Data Science", exp))