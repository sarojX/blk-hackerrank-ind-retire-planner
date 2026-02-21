from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.utils.date_utils import parse_timestamp


class Expense(BaseModel):
    date: datetime
    amount: float = Field(ge=0)

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")})

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, datetime):
            return value
        return parse_timestamp(value)


class Transaction(BaseModel):
    date: datetime
    amount: float
    ceiling: float
    remanent: float

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")})

    @field_validator("date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, datetime):
            return value
        return parse_timestamp(value)


class InvalidTransaction(Transaction):
    message: str


class ParseTransactionsRequest(BaseModel):
    expenses: List[Expense]


class ParseTransactionsResponse(BaseModel):
    transactions: List[Transaction]
    total_expense: float
    total_ceiling: float
    total_remanent: float


class ValidateTransactionsRequest(BaseModel):
    wage: float = Field(gt=0)
    transactions: List[Transaction]


class ValidateTransactionsResponse(BaseModel):
    valid: List[Transaction]
    invalid: List[InvalidTransaction]


class QPeriod(BaseModel):
    fixed: float = Field(ge=0)
    start: datetime
    end: datetime

    @field_validator("start", "end", mode="before")
    @classmethod
    def parse_dates(cls, value):
        if isinstance(value, datetime):
            return value
        return parse_timestamp(value)


class PPeriod(BaseModel):
    extra: float = Field(ge=0)
    start: datetime
    end: datetime

    @field_validator("start", "end", mode="before")
    @classmethod
    def parse_dates(cls, value):
        if isinstance(value, datetime):
            return value
        return parse_timestamp(value)


class KPeriod(BaseModel):
    start: datetime
    end: datetime

    @field_validator("start", "end", mode="before")
    @classmethod
    def parse_dates(cls, value):
        if isinstance(value, datetime):
            return value
        return parse_timestamp(value)


class FilterTransactionsRequest(BaseModel):
    transactions: List[Transaction]
    q: List[QPeriod] = Field(default_factory=list)
    p: List[PPeriod] = Field(default_factory=list)
    k: List[KPeriod] = Field(default_factory=list)


class SavingsByDate(BaseModel):
    start: datetime
    end: datetime
    amount: float


class FilterTransactionsResponse(BaseModel):
    transactions: List[Transaction]
    savings_by_dates: List[SavingsByDate]


class ReturnsRequest(BaseModel):
    age: int = Field(ge=0)
    wage: float = Field(gt=0)
    inflation: float = Field(ge=0)
    transactions: List[Expense]
    q: List[QPeriod] = Field(default_factory=list)
    p: List[PPeriod] = Field(default_factory=list)
    k: List[KPeriod] = Field(default_factory=list)


class SavingsReturnBreakdown(BaseModel):
    start: datetime
    end: datetime
    amount: float
    profit: float
    taxBenefit: float
    finalAmount: float
    realValue: float


class ReturnsResponse(BaseModel):
    transactionsTotalAmount: float
    transactionsTotalCeiling: float
    savingsByDates: List[SavingsReturnBreakdown]


class PerformanceResponse(BaseModel):
    time: str
    memory: str
    threads: int
    uptime_ms: Optional[int] = None
