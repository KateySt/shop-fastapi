from uuid import UUID

import stripe

from app.config import stripe_config
from app.exception import ForbiddenError, NotFoundError
from app.repo.order_repository import OrderRepository

stripe.api_key = stripe_config.STRIPE_SECRET_KEY


class PaymentServiceImpl:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    async def create_payment_session(
        self,
        order_id: UUID,
        user_id: UUID,
        success_url: str,
        cancel_url: str,
    ) -> str:
        order = await self.repo.get_with_items(order_id)

        if not order:
            raise NotFoundError("Order not found")
        if order.user_id != user_id:
            raise ForbiddenError("Access denied")
        if order.is_closed:
            raise ForbiddenError("Cannot pay for a closed order")

        total = sum(item.price * item.quantity for item in order.items)

        if total < 15:
            raise ValueError(
                f"Order total {total} UAH is too low for payment processing"
            )

        line_items = [
            {
                "price_data": {
                    "currency": "uah",
                    "product_data": {
                        "name": item.item.name,
                        "description": item.item.description,
                    },
                    "unit_amount": int(item.price * 100),
                },
                "quantity": item.quantity,
            }
            for item in order.items
        ]

        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=order.user.email,
            metadata={
                "order_id": str(order_id),
                "user_id": str(user_id),
            },
        )

        return session["url"]

    @staticmethod
    async def handle_webhook(payload: bytes, sig_header: str) -> dict:
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, stripe_config.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            raise ValueError("Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise ForbiddenError("Invalid signature")

        return event
