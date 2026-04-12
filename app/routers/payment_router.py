from uuid import UUID

from fastapi import APIRouter, Depends, Request

from app.db.models import User
from app.dependencies.auth import get_current_user
from app.schemas.payment import PaymentSessionRequest, PaymentUrlResponse
from app.services import OrderServiceDep, PaymentServiceDep

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/{order_id}", response_model=PaymentUrlResponse)
async def pay_for_order(
    order_id: UUID,
    data: PaymentSessionRequest,
    service: PaymentServiceDep,
    user: User = Depends(get_current_user),
):
    return await service.create_payment_session(
        order_id, user, data.success_url, data.cancel_url
    )


@router.post("/webhook", include_in_schema=False)
async def stripe_webhook(
    request: Request,
    payment_service: PaymentServiceDep,
    order_service: OrderServiceDep,
):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    order_id = await payment_service.handle_webhook(payload, sig_header)

    if order_id:
        await order_service.close_order(order_id)

    return {"status": "ok"}
