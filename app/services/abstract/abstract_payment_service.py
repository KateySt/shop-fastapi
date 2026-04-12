from abc import ABC, abstractmethod
from uuid import UUID

from app.db.models import User
from app.schemas.payment import PaymentUrlResponse


class AbstractPaymentService(ABC):

    @abstractmethod
    async def create_payment_session(
        self, order_id: UUID, user: User, success_url: str, cancel_url: str
    ) -> PaymentUrlResponse: ...

    @abstractmethod
    async def handle_webhook(
        self,
        payload: bytes,
        sig_header: str,
    ) -> UUID | None: ...
