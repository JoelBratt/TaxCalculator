import math
"""
Joel Bratt
Tax Calcualator
Program meant to calculate my own taxes
"""

firstname = input("Enter your first name: ")

lastname = input("Enter your last name: ")

while True:
    try:
        taxable = int(input("Enter your taxable income rounded to the nearest whole number: "))
        break 
    except ValueError:
        print("Invalid input! That is not a whole number. Try again.")

statetaxable = taxable
fedtaxable = taxable

while True:
    try:
        localtaxable = int(input("Enter your gross income rounded to the nearest whole number while not including earning and retirement income (please note that this is prompt will need modified depending on where you live): "))
        break 
    except ValueError:
        print("Invalid input! That is not a whole number. Try again.")

localrate_input = float(input(f'Enter your local tax rate as a percent: \nExample: "1" for 1% or "2.2" for 2.2% '))

def calculate_ohio_tax(statetaxable):
    if statetaxable <= 26050:
        return 0
    elif statetaxable <= 100000:
        return 342 + (statetaxable - 26050) *.0275
    else:
        return 2394.32 + (statetaxable - 100000) *.03125

def calculate_local_tax(localtaxable, localrate_input):
    return localtaxable * (localrate_input / 100)

local_tax = calculate_local_tax(localtaxable, localrate_input)
state_tax = calculate_ohio_tax(statetaxable)
print(f'Great job {firstname + " " + lastname} here are some number to verify your formulas so far. \n Local Tax: {local_tax:,.2f} \n Ohio Tax: {state_tax:,.2f} \n Combined so far {state_tax + local_tax:,.2f}')