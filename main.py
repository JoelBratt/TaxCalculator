import math
import csv
import os
"""
Joel Bratt
Tax Calcualator
Program meant to calculate my own taxes
"""

firstname = input("Enter your first name: ")

lastname = input("Enter your last name: ")

while True:
    status = input("What is your filing status?\n1. Single\n2. Married filing jointly\n3. Married filing separately\n4. Head of Household\nEnter choice (1-4): ").strip()
    if status in ["1", "2", "3", "4"]:
        break
    print("Invalid input! Please enter a number between 1 and 4.")

status_labels = {
    "1": "Single",
    "2": "Married filing jointly",
    "3": "Married filing separately",
    "4": "Head of Household"
}
status_name = status_labels[status]

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

def calculate_federal_tax(fedtaxable, status):
    tax = 0.0
    
    if status == "1":
        if taxable <= 11925:
            tax = taxable * 0.10
        elif taxable <= 48475:
            tax = 1192.50 + (taxable - 11925) * 0.12
        elif taxable <= 103350:
            tax = 5578.50 + (taxable - 48475) * 0.22
        elif taxable <= 197300:
            tax = 17651.00 + (taxable - 103350) * 0.24
        elif taxable <= 250525:
            tax = 40199.00 + (taxable - 197300) * 0.32
        elif taxable <= 626350:
            tax = 57231.00 + (taxable - 250525) * 0.35
        else:
            tax = 188769.75 + (taxable - 626350) * 0.37

    elif status == "2":
        if taxable <= 23850:
            tax = taxable * 0.10
        elif taxable <= 96950:
            tax = 2385.00 + (taxable - 23850) * 0.12
        elif taxable <= 206700:
            tax = 11157.00 + (taxable - 96950) * 0.22
        elif taxable <= 394600:
            tax = 35302.00 + (taxable - 206700) * 0.24
        elif taxable <= 501050:
            tax = 80398.00 + (taxable - 394600) * 0.32
        elif taxable <= 751600:
            tax = 114462.00 + (taxable - 501050) * 0.35
        else:
            tax = 202154.50 + (taxable - 751600) * 0.37

    elif status == "3":
        if taxable <= 11925:
            tax = taxable * 0.10
        elif taxable <= 48475:
            tax = 1192.50 + (taxable - 11925) * 0.12
        elif taxable <= 103350:
            tax = 5578.50 + (taxable - 48475) * 0.22
        elif taxable <= 197300:
            tax = 17651.00 + (taxable - 103350) * 0.24
        elif taxable <= 250525:
            tax = 40199.00 + (taxable - 197300) * 0.32
        elif taxable <= 375800:
            tax = 57231.00 + (taxable - 250525) * 0.35
        else:
            tax = 101077.25 + (taxable - 375800) * 0.37

    elif status == "4":
        if taxable <= 17000:
            tax = taxable * 0.10
        elif taxable <= 64850:
            tax = 1700.00 + (taxable - 17000) * 0.12
        elif taxable <= 103350:
            tax = 7442.00 + (taxable - 64850) * 0.22
        elif taxable <= 197300:
            tax = 15912.00 + (taxable - 103350) * 0.24
        elif taxable <= 250500:
            tax = 38460.00 + (taxable - 197300) * 0.32
        elif taxable <= 626350:
            tax = 55486.00 + (taxable - 250500) * 0.35
        else:
            tax = 187033.50 + (taxable - 626350) * 0.37

    return round(tax, 2)

def resolve_csv_path(user_path, default_filename="tax_summary.csv"):
    cleaned = user_path.strip().strip('"').strip("'")
    if not cleaned:
        cleaned = default_filename
    if os.path.isabs(cleaned):
        return cleaned
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, cleaned)


def import_csv(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: '{file_path}'")
        return None

    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)

    print(f"\nLoaded {len(rows)} rows from '{file_path}'.")
    return rows


def write_report_rows(writer, include_header=True):
    if include_header:
        writer.writerow(["TAX SUMMARY REPORT", ""])
        writer.writerow(["Taxpayer Name", f"{firstname} {lastname}"])
        writer.writerow(["Filing Status", status_name])
        writer.writerow([])
        writer.writerow(["Category", "Base Amount ($)", "Rate / Details", "Calculated Tax ($)"])

    writer.writerow(
        ["Federal Income Tax", f"{fedtaxable:,.2f}", "Progressive Brackets (2025)", f"{fed_tax:,.2f}"]
    )
    writer.writerow(["Ohio State Tax", f"{statetaxable:,.2f}", "Ohio 2025 Brackets", f"{state_tax:,.2f}"])
    writer.writerow(["Local Tax", f"{localtaxable:,.2f}", f"{localrate_input}% Flat", f"{local_tax:,.2f}"])
    writer.writerow([])
    writer.writerow(["TOTAL COMBINED TAX", "", "", f"{total_tax:,.2f}"])
    writer.writerow(["Overall Effective Tax Rate", "", "", f"{effective_rate:.2f}%"])


def export_to_csv(file_path, append=False):
    file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0
    mode = "a" if (append and file_exists) else "w"


    needs_leading_blank = mode == "a"

    with open(file_path, mode=mode, newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if needs_leading_blank:
            writer.writerow([])
            writer.writerow(["--- UPDATED / NEW ENTRY ---", "", "", ""])
        write_report_rows(writer, include_header=not needs_leading_blank)

    action_word = "Appended to" if mode == "a" else "Saved"
    print(f"\nSuccessfully {action_word.lower()} tax report: '{file_path}'")


fed_tax = calculate_federal_tax(fedtaxable, status)
local_tax = calculate_local_tax(localtaxable, localrate_input)
state_tax = calculate_ohio_tax(statetaxable)
total_tax = fed_tax + state_tax + local_tax
effective_rate = (total_tax / fedtaxable * 100) if fedtaxable > 0 else 0.0

print(f"\nGreat job {firstname} {lastname}! Here is your current tax breakdown:")
print(f" - Federal Income Tax: ${fed_tax:,.2f}")
print(f" - Ohio State Tax:     ${state_tax:,.2f}")
print(f" - Local Tax:          ${local_tax:,.2f}")
print(f" - Total Combined Tax: ${total_tax:,.2f}")

imported_path = None
imported_rows = None

while True:
    upload_choice = (
        input("\nY/N would you like to upload an existing CSV to add new rows below it? ")
        .strip()
        .lower()
    )
    if upload_choice == "y":
        raw_path = input(
            "Enter CSV filename or full path (press Enter for 'tax_summary.csv' in script folder): "
        )
        candidate_path = resolve_csv_path(raw_path)
        rows = import_csv(candidate_path)
        if rows is not None:
            imported_path = candidate_path
            imported_rows = rows
            break
    elif upload_choice == "n":
        break
    else:
        print("Invalid input! Please enter Y or N.")

while True:
    exportquestion = input("Y/N would you like to export/update the CSV? ").strip().lower()
    if exportquestion == "y":
        if imported_path:
            target_path = imported_path
            export_to_csv(target_path, append = True)
        else:
            raw_save = input(
                "Enter output CSV filename (press Enter for 'tax_summary.csv' in script folder): "
            )
            target_path = resolve_csv_path(raw_save)
            export_to_csv(target_path, append = False)
        break
    elif exportquestion == "n":
        break
    else:
        print("Invalid input! Please enter a letter that is Y or N")