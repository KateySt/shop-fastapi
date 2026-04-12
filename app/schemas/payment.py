from pydantic import BaseModel


class PaymentUrlResponse(BaseModel):
    url: str


class PaymentSessionRequest(BaseModel):
    success_url: str
    cancel_url: str
