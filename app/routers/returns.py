from fastapi import APIRouter

from app.models.schemas import ReturnsRequest, ReturnsResponse
from app.services.returns_service import compute_index_returns, compute_nps_returns

router = APIRouter(prefix="/blackrock/challenge/v1", tags=["returns"])


@router.post("/returns:nps", response_model=ReturnsResponse)
def returns_nps(payload: ReturnsRequest) -> ReturnsResponse:
    return compute_nps_returns(payload)


@router.post("/returns:index", response_model=ReturnsResponse)
def returns_index(payload: ReturnsRequest) -> ReturnsResponse:
    return compute_index_returns(payload)
