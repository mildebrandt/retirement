import sys
import yaml


with open('income_brackets.yaml', 'r') as f:
    brackets = yaml.safe_load(f)["brackets"]


def calculate_taxes(income, region, filing_status):
    total = 0
    for bracket in brackets[region][filing_status]:
        if income < bracket["lower"]:
            break
        total += min(
                bracket["upper"] - bracket["lower"],
                income - bracket["lower"]
            ) * bracket["rate"]

    return total


def calculate_required_income(base_expenses, state, filing_status):
    lower_guess = base_expenses
    upper_guess = base_expenses * 2
    guess = base_expenses
    while upper_guess - lower_guess > 1:
        total_taxes = (
            calculate_taxes(guess, "federal", filing_status) +
            calculate_taxes(guess, state, filing_status)
        )
        total_income_needed = base_expenses + total_taxes
        if abs(guess - total_income_needed) < 1:
            break
        if guess > total_income_needed:
            guess = guess - (guess - total_income_needed) / 2
        else:
            guess = guess + (total_income_needed - guess) / 2

    return guess


base = int(sys.argv[1])
required_income = calculate_required_income(base,
                                            "california",
                                            "married_filing_jointly")
taxes = required_income - base
tax_rate = (taxes / required_income) * 100

print(f"Base income:\t\t${base:,.2f}")
print(f"Required income:\t${required_income:,.2f}")
print(f"Total taxes:\t\t${taxes:,.2f}")
print(f"Tax rate:\t\t{tax_rate:.2f}%")
