from fastapi import APIRouter

from app.models.schemas import (
    FilterTransactionsRequest,
    FilterTransactionsResponse,
    ParseTransactionsRequest,
    ParseTransactionsResponse,
    ValidateTransactionsRequest,
    ValidateTransactionsResponse,
)
from app.services.temporal_service import apply_temporal_rules
from app.services.transaction_service import build_transactions
from app.services.validation_service import validate_transactions

router = APIRouter(prefix="/blackrock/challenge/v1", tags=["transactions"])


@router.post("/transactions:parse", response_model=ParseTransactionsResponse)
def parse_transactions(payload: ParseTransactionsRequest) -> ParseTransactionsResponse:
    return build_transactions(payload.expenses)


@router.post("/transactions:validator", response_model=ValidateTransactionsResponse)
def validate(payload: ValidateTransactionsRequest) -> ValidateTransactionsResponse:
    return validate_transactions(payload.transactions)


@router.post("/transactions:filter", response_model=FilterTransactionsResponse)
def filter_transactions(payload: FilterTransactionsRequest) -> FilterTransactionsResponse:
    return apply_temporal_rules(payload.transactions, payload.q, payload.p, payload.k)
