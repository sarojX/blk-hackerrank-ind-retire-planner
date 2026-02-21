from app.models.schemas import InvalidTransaction, Transaction, ValidateTransactionsResponse


def validate_transactions(transactions: list[Transaction]) -> ValidateTransactionsResponse:
    seen_dates = set()
    valid: list[Transaction] = []
    invalid: list[InvalidTransaction] = []

    for tx in transactions:
        message = None
        date_key = tx.date.isoformat()

        if date_key in seen_dates:
            message = "duplicate timestamp"
        elif tx.amount < 0 or tx.ceiling < 0 or tx.remanent < 0:
            message = "negative values are not allowed"
        elif round(tx.ceiling - tx.amount, 2) != round(tx.remanent, 2):
            message = "remanent mismatch (ceiling - amount)"

        if message:
            invalid.append(InvalidTransaction(**tx.model_dump(), message=message))
        else:
            seen_dates.add(date_key)
            valid.append(tx)

    return ValidateTransactionsResponse(valid=valid, invalid=invalid)
