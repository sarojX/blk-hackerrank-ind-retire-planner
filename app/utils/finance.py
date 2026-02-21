import math


def next_multiple_100(amount: float) -> float:
    if amount % 100 == 0:
        return float(amount)
    return float(math.ceil(amount / 100.0) * 100)


def remanent(amount: float) -> float:
    return round(next_multiple_100(amount) - amount, 2)


def compound_amount(principal: float, rate: float, years: int) -> float:
    return round(principal * ((1 + rate) ** years), 2)


def inflation_adjusted(amount: float, inflation: float, years: int) -> float:
    return round(amount / ((1 + inflation) ** years), 2)


def tax_for_income(income: float) -> float:
    if income <= 700000:
        return 0.0

    tax = 0.0
    remaining = income

    if remaining > 1500000:
        tax += (remaining - 1500000) * 0.30
        remaining = 1500000
    if remaining > 1200000:
        tax += (remaining - 1200000) * 0.20
        remaining = 1200000
    if remaining > 1000000:
        tax += (remaining - 1000000) * 0.15
        remaining = 1000000
    if remaining > 700000:
        tax += (remaining - 700000) * 0.10

    return round(tax, 2)
