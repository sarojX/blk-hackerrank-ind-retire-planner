from app.models.schemas import Expense, ParseTransactionsResponse, Transaction
from app.utils.finance import next_multiple_100, remanent


def build_transactions(expenses: list[Expense]) -> ParseTransactionsResponse:
    txs: list[Transaction] = []
    total_expense = 0.0
    total_ceiling = 0.0
    total_remanent = 0.0

    for item in expenses:
        ceiling = next_multiple_100(item.amount)
        rem = remanent(item.amount)
        tx = Transaction(date=item.date, amount=item.amount, ceiling=ceiling, remanent=rem)
        txs.append(tx)
        total_expense += item.amount
        total_ceiling += ceiling
        total_remanent += rem

    return ParseTransactionsResponse(
        transactions=txs,
        total_expense=round(total_expense, 2),
        total_ceiling=round(total_ceiling, 2),
        total_remanent=round(total_remanent, 2),
    )
