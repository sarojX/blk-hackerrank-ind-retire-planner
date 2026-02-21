# blk-hacking-ind-micro-savings

Production-grade FastAPI application for automated retirement micro-savings based on expense rounding, temporal investment rules (q/p/k), and long-term return projections.

## Tech Stack
- Python 3.11
- FastAPI + Pydantic
- Uvicorn
- Pytest
- Docker (Linux base image)

## Project Structure

```text
app/
  main.py
  core/config.py
  models/schemas.py
  routers/
    transactions.py
    returns.py
    performance.py
  services/
    transaction_service.py
    validation_service.py
    temporal_service.py
    returns_service.py
  utils/
    finance.py
    date_utils.py
test/
  test_transactions.py
  test_returns.py
Dockerfile
compose.yaml
requirements.txt
README.md
```

## Setup (Local)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 5477
```

Health check:

```bash
curl http://localhost:5477/health
```

## Docker

Build image:

```bash
docker build -t blk-hacking-ind-openai-codex .
```

Run container:

```bash
docker run -d -p 5477:5477 blk-hacking-ind-openai-codex
```

Or with compose:

```bash
docker compose up --build
```

## API Endpoints

- `POST /blackrock/challenge/v1/transactions:parse`
- `POST /blackrock/challenge/v1/transactions:validator`
- `POST /blackrock/challenge/v1/transactions:filter`
- `POST /blackrock/challenge/v1/returns:nps`
- `POST /blackrock/challenge/v1/returns:index`
- `GET /blackrock/challenge/v1/performance`

## Example cURL Requests

### 1) Parse Transactions

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/transactions:parse \
  -H 'Content-Type: application/json' \
  -d '{
    "expenses": [
      {"date": "2023-10-12 20:15:00", "amount": 250},
      {"date": "2023-02-28 15:49:00", "amount": 375}
    ]
  }'
```

### 2) Filter with q/p/k

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/transactions:filter \
  -H 'Content-Type: application/json' \
  -d '{
    "transactions": [
      {"date": "2023-10-12 20:15:00", "amount": 250, "ceiling": 300, "remanent": 50}
    ],
    "q": [{"fixed": 0, "start": "2023-07-01 00:00:00", "end": "2023-07-31 23:59:59"}],
    "p": [{"extra": 25, "start": "2023-10-01 08:00:00", "end": "2023-12-31 19:59:59"}],
    "k": [{"start": "2023-01-01 00:00:00", "end": "2023-12-31 23:59:59"}]
  }'
```

### 3) NPS Returns

```bash
curl -X POST http://localhost:5477/blackrock/challenge/v1/returns:nps \
  -H 'Content-Type: application/json' \
  -d '{
    "age": 29,
    "wage": 50000,
    "inflation": 0.055,
    "transactions": [
      {"date": "2023-10-12 20:15:00", "amount": 250},
      {"date": "2023-02-28 15:49:00", "amount": 375},
      {"date": "2023-07-01 21:59:00", "amount": 620},
      {"date": "2023-12-17 08:09:00", "amount": 480}
    ],
    "q": [{"fixed": 0, "start": "2023-07-01 00:00:00", "end": "2023-07-31 23:59:59"}],
    "p": [{"extra": 25, "start": "2023-10-01 08:00:00", "end": "2023-12-31 19:59:59"}],
    "k": [{"start": "2023-01-01 00:00:00", "end": "2023-12-31 23:59:59"}]
  }'
```

## API Behavior Summary

1. Parse computes ceiling-to-next-100 and remanent per expense, plus totals.
2. Validator checks duplicate timestamps, negative values, and remanent correctness.
3. Filter applies rules in strict order:
   - q periods override remanent (latest start wins, then first listed)
   - p periods add all matching extras
   - k periods aggregate independently using inclusive ranges
4. NPS returns:
   - 7.11% compound annual growth
   - tax benefit from `Tax(income) - Tax(income - min(invested, 10% annual income, 200000))`
   - inflation-adjusted real value
5. Index returns:
   - 14.49% compound annual growth
   - no tax benefit
   - inflation-adjusted real value

## Performance Considerations

- Strict datetime parsing via `%Y-%m-%d %H:%M:%S`.
- Sorting + sweep line interval handling for q and p rules.
- Prefix-sum + binary search for k range aggregation.
- Avoids brute force `O(n*q*p*k)`; achieves scalable `O((n+q+p) log(n+q+p) + k log n)`.

## Assumptions

- Datetimes are naive and interpreted consistently in server local context.
- q/p/k ranges are inclusive.
- `transactions:validator` validates provided transaction fields; it does not recompute from amount.
- Tax slab model follows simplified progressive brackets from challenge statement.
- If age >= 60, projection horizon is fixed to 5 years.

## Testing

```bash
pytest -q
```

Included tests cover:
- rounding logic
- temporal q/p/k order rules
- return and tax behavior
