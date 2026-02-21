# Test type: Unit Test
# Validation: NPS and Index return calculation, including tax benefit behavior.
# Command: pytest -q

from app.models.schemas import KPeriod, ReturnsRequest
from app.services.returns_service import compute_index_returns, compute_nps_returns


def _base_payload() -> ReturnsRequest:
    return ReturnsRequest(
        age=29,
        wage=50000,
        inflation=0.055,
        transactions=[
            {"date": "2023-10-12 20:15:00", "amount": 250},
            {"date": "2023-02-28 15:49:00", "amount": 375},
            {"date": "2023-07-01 21:59:00", "amount": 620},
            {"date": "2023-12-17 08:09:00", "amount": 480},
        ],
        q=[{"fixed": 0, "start": "2023-07-01 00:00:00", "end": "2023-07-31 23:59:59"}],
        p=[{"extra": 25, "start": "2023-10-01 08:00:00", "end": "2023-12-31 19:59:59"}],
        k=[KPeriod(start="2023-01-01 00:00:00", end="2023-12-31 23:59:59")],
    )


def test_nps_returns_has_tax_benefit_field():
    payload = _base_payload()
    res = compute_nps_returns(payload)

    assert res.transactionsTotalAmount == 1725.0
    assert res.transactionsTotalCeiling == 1900.0
    assert len(res.savingsByDates) == 1
    assert res.savingsByDates[0].amount == 145.0
    assert res.savingsByDates[0].finalAmount > res.savingsByDates[0].amount
    assert res.savingsByDates[0].taxBenefit == 0.0


def test_index_returns_has_zero_tax_benefit():
    payload = _base_payload()
    res = compute_index_returns(payload)

    assert len(res.savingsByDates) == 1
    assert res.savingsByDates[0].taxBenefit == 0.0
    assert res.savingsByDates[0].realValue > 0
