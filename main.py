import math
"""
Joel Bratt
Tax Calcualator
"""

firstname = input("Enter your first name:")

print(f'{firstname}')

lastname = input("Enter your last name:")

print(f'{lastname}')

while True:
    try:
        taxable = int(input("Enter your taxable income rounded to the nearest whole number:"))
        break 
    except ValueError:
        print("Invalid input! That is not a whole number. Try again.")


localrate = float(input(f'Enter your local tax rate as a percent: \n Example: "1" for 1% or "2.2" for 2.2%'))

def calculate_ohio_tax(taxable):
    if taxable <= 26050:
        return 0
    elif taxable <= 100000:
        return 342 + (taxable - 26050) *.0275
    else:
        return 2394.32 + (taxable - 100000) *.03125

print(f"Success! Your taxable income: {taxable}")