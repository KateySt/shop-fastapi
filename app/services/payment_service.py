from uuid import UUID

from app.db.models import User
from app.schemas.payment import PaymentUrlResponse
from app.services.abstract import AbstractPaymentService
from app.services.impl.payment_service_impl import PaymentServiceImpl


class PaymentService(AbstractPaymentService):
    def __init__(self, impl: PaymentServiceImpl):
        self.impl = impl

    async def create_payment_session(
        self,
        order_id: UUID,
        user: User,
        success_url: str,
        cancel_url: str,
    ) -> PaymentUrlResponse:
        url = await self.impl.create_payment_session(
            order_id, user.id, success_url, cancel_url
        )
        return PaymentUrlResponse(url=url)

    async def handle_webhook(self, payload: bytes, sig_header: str) -> UUID | None:
        event = await self.impl.handle_webhook(payload, sig_header)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            return UUID(session["metadata"]["order_id"])

        return None
