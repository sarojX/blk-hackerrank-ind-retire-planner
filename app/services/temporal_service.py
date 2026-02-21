from bisect import bisect_left, bisect_right
from datetime import timedelta
import heapq

from app.models.schemas import FilterTransactionsResponse, KPeriod, PPeriod, QPeriod, SavingsByDate, Transaction


def _apply_q_periods(transactions: list[Transaction], q_periods: list[QPeriod]) -> list[Transaction]:
    if not q_periods:
        return [Transaction(**tx.model_dump()) for tx in transactions]

    sorted_txs = sorted(transactions, key=lambda t: t.date)
    q_sorted = sorted(
        enumerate(q_periods),
        key=lambda x: x[1].start,
    )

    q_ptr = 0
    active_heap: list[tuple[float, int, object, float]] = []
    out: list[Transaction] = []

    for tx in sorted_txs:
        while q_ptr < len(q_sorted) and q_sorted[q_ptr][1].start <= tx.date:
            idx, period = q_sorted[q_ptr]
            start_key = period.start.timestamp()
            heapq.heappush(active_heap, (-start_key, idx, period.end, period.fixed))
            q_ptr += 1

        while active_heap and active_heap[0][2] < tx.date:
            heapq.heappop(active_heap)

        new_tx = Transaction(**tx.model_dump())
        if active_heap:
            # heap top = latest start; for same start lower original idx wins
            new_tx.remanent = round(active_heap[0][3], 2)
        out.append(new_tx)

    return out


def _apply_p_periods(transactions: list[Transaction], p_periods: list[PPeriod]) -> list[Transaction]:
    if not p_periods:
        return transactions

    sorted_txs = sorted(transactions, key=lambda t: t.date)
    deltas: list[tuple[object, float]] = []
    for period in p_periods:
        deltas.append((period.start, period.extra))
        deltas.append((period.end + timedelta(seconds=1), -period.extra))

    deltas.sort(key=lambda x: x[0])
    delta_ptr = 0
    running_extra = 0.0
    out: list[Transaction] = []

    for tx in sorted_txs:
        while delta_ptr < len(deltas) and deltas[delta_ptr][0] <= tx.date:
            running_extra += deltas[delta_ptr][1]
            delta_ptr += 1

        new_tx = Transaction(**tx.model_dump())
        new_tx.remanent = round(new_tx.remanent + running_extra, 2)
        out.append(new_tx)

    return out


def _group_by_k_periods(transactions: list[Transaction], k_periods: list[KPeriod]) -> list[SavingsByDate]:
    if not k_periods:
        return []

    sorted_txs = sorted(transactions, key=lambda t: t.date)
    dates = [tx.date for tx in sorted_txs]
    prefix = [0.0]
    for tx in sorted_txs:
        prefix.append(prefix[-1] + tx.remanent)

    out: list[SavingsByDate] = []
    for period in k_periods:
        left = bisect_left(dates, period.start)
        right = bisect_right(dates, period.end)
        amount = round(prefix[right] - prefix[left], 2)
        out.append(SavingsByDate(start=period.start, end=period.end, amount=amount))

    return out


def apply_temporal_rules(
    transactions: list[Transaction], q_periods: list[QPeriod], p_periods: list[PPeriod], k_periods: list[KPeriod]
) -> FilterTransactionsResponse:
    q_applied = _apply_q_periods(transactions, q_periods)
    qp_applied = _apply_p_periods(q_applied, p_periods)
    savings = _group_by_k_periods(qp_applied, k_periods)

    return FilterTransactionsResponse(transactions=qp_applied, savings_by_dates=savings)
