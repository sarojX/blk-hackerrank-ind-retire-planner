import threading
import time

from fastapi import APIRouter

from app.models.schemas import PerformanceResponse

router = APIRouter(prefix="/blackrock/challenge/v1", tags=["performance"])
START_TIME = time.perf_counter()


def _memory_mb() -> float:
    try:
        import resource

        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # Linux reports kilobytes
        return rss / 1024.0
    except Exception:
        return 0.0


@router.get("/performance", response_model=PerformanceResponse)
def performance() -> PerformanceResponse:
    uptime_ms = int((time.perf_counter() - START_TIME) * 1000)
    hours = uptime_ms // 3_600_000
    minutes = (uptime_ms % 3_600_000) // 60_000
    seconds = (uptime_ms % 60_000) // 1000
    millis = uptime_ms % 1000
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"
    return PerformanceResponse(
        time=time_str,
        memory=f"{_memory_mb():.2f} MB",
        threads=threading.active_count(),
        uptime_ms=uptime_ms,
    )
