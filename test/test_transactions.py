# Test type: Unit Test
# Validation: Rounding/remanent generation and temporal q/p/k processing order.
# Command: pytest -q

from app.models.schemas import Expense, KPeriod, PPeriod, QPeriod
from app.services.temporal_service import apply_temporal_rules
from app.services.transaction_service import build_transactions


def test_rounding_logic_build_transactions():
    expenses = [
        Expense(date="2023-10-12 20:15:00", amount=250),
        Expense(date="2023-02-28 15:49:00", amount=375),
        Expense(date="2023-07-01 21:59:00", amount=620),
    ]
    result = build_transactions(expenses)

    assert [t.ceiling for t in result.transactions] == [300.0, 400.0, 700.0]
    assert [t.remanent for t in result.transactions] == [50.0, 25.0, 80.0]
    assert result.total_remanent == 155.0


def test_temporal_rules_q_then_p_then_k_grouping():
    expenses = [
        Expense(date="2023-10-12 20:15:00", amount=250),
        Expense(date="2023-02-28 15:49:00", amount=375),
        Expense(date="2023-07-01 21:59:00", amount=620),
        Expense(date="2023-12-17 08:09:00", amount=480),
    ]
    txs = build_transactions(expenses).transactions

    q = [QPeriod(fixed=0, start="2023-07-01 00:00:00", end="2023-07-31 23:59:59")]
    p = [PPeriod(extra=25, start="2023-10-01 08:00:00", end="2023-12-31 19:59:59")]
    k = [
        KPeriod(start="2023-03-01 00:00:00", end="2023-11-30 23:59:59"),
        KPeriod(start="2023-01-01 00:00:00", end="2023-12-31 23:59:59"),
    ]

    filtered = apply_temporal_rules(txs, q, p, k)

    by_date = {t.date.strftime('%Y-%m-%d %H:%M:%S'): t.remanent for t in filtered.transactions}
    assert by_date["2023-07-01 21:59:00"] == 0.0
    assert by_date["2023-10-12 20:15:00"] == 75.0
    assert by_date["2023-12-17 08:09:00"] == 45.0

    assert filtered.savings_by_dates[0].amount == 75.0
    assert filtered.savings_by_dates[1].amount == 145.0
