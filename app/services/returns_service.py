from app.models.schemas import ReturnsRequest, ReturnsResponse, SavingsReturnBreakdown
from app.services.temporal_service import apply_temporal_rules
from app.services.transaction_service import build_transactions
from app.utils.finance import compound_amount, inflation_adjusted, tax_for_income

NPS_RATE = 0.0711
INDEX_RATE = 0.1449


def retirement_years(age: int) -> int:
    return 5 if age >= 60 else 60 - age


def compute_nps_returns(payload: ReturnsRequest) -> ReturnsResponse:
    tx_result = build_transactions(payload.transactions)
    filtered = apply_temporal_rules(tx_result.transactions, payload.q, payload.p, payload.k)
    years = retirement_years(payload.age)
    annual_income = payload.wage * 12

    breakdown: list[SavingsReturnBreakdown] = []
    for item in filtered.savings_by_dates:
        final_amount = compound_amount(item.amount, NPS_RATE, years)
        profit = round(final_amount - item.amount, 2)
        deduction = min(item.amount, 0.10 * annual_income, 200000)
        tax_benefit = round(
            tax_for_income(annual_income) - tax_for_income(max(annual_income - deduction, 0.0)),
            2,
        )
        real_value = inflation_adjusted(final_amount, payload.inflation, years)
        breakdown.append(
            SavingsReturnBreakdown(
                start=item.start,
                end=item.end,
                amount=item.amount,
                profit=profit,
                taxBenefit=tax_benefit,
                finalAmount=final_amount,
                realValue=real_value,
            )
        )

    return ReturnsResponse(
        transactionsTotalAmount=tx_result.total_expense,
        transactionsTotalCeiling=tx_result.total_ceiling,
        savingsByDates=breakdown,
    )


def compute_index_returns(payload: ReturnsRequest) -> ReturnsResponse:
    tx_result = build_transactions(payload.transactions)
    filtered = apply_temporal_rules(tx_result.transactions, payload.q, payload.p, payload.k)
    years = retirement_years(payload.age)

    breakdown: list[SavingsReturnBreakdown] = []
    for item in filtered.savings_by_dates:
        final_amount = compound_amount(item.amount, INDEX_RATE, years)
        profit = round(final_amount - item.amount, 2)
        real_value = inflation_adjusted(final_amount, payload.inflation, years)
        breakdown.append(
            SavingsReturnBreakdown(
                start=item.start,
                end=item.end,
                amount=item.amount,
                profit=profit,
                taxBenefit=0.0,
                finalAmount=final_amount,
                realValue=real_value,
            )
        )

    return ReturnsResponse(
        transactionsTotalAmount=tx_result.total_expense,
        transactionsTotalCeiling=tx_result.total_ceiling,
        savingsByDates=breakdown,
    )
