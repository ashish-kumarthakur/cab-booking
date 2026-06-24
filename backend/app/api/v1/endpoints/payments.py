from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime
import stripe

from app.core.database import get_db
from app.core.config import settings
from app.core.security import get_current_user
from app.models.payment import Payment, PaymentStatus
from app.models.ride import Ride
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment import create_payment_intent

router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/create-intent", response_model=dict)
async def create_payment_intent_endpoint(
    payment_data: PaymentCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Ride).where(
            Ride.id == payment_data.ride_id,
            Ride.rider_id == user.id
        )
    )
    ride = result.scalar_one_or_none()
    
    if not ride:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ride not found",
        )
    
    if ride.status.value not in ["completed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ride must be completed before payment",
        )
    
    payment = Payment(
        ride_id=payment_data.ride_id,
        amount=payment_data.amount,
        status=PaymentStatus.PENDING,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    
    try:
        intent_data = create_payment_intent(
            amount=payment_data.amount,
            metadata={
                "ride_id": str(payment_data.ride_id),
                "payment_id": str(payment.id),
                "user_id": str(user.id),
            }
        )
        
        payment.stripe_payment_intent_id = intent_data["payment_intent_id"]
        await db.commit()
        
        return {
            "client_secret": intent_data["client_secret"],
            "payment_intent_id": intent_data["payment_intent_id"],
            "payment_id": str(payment.id),
        }
    
    except Exception as e:
        payment.status = PaymentStatus.FAILED
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create payment intent: {str(e)}",
        )


@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook secret not configured",
        )
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payload",
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid signature",
        )
    
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        intent_id = payment_intent["id"]
        
        result = await db.execute(
            select(Payment).where(Payment.stripe_payment_intent_id == intent_id)
        )
        payment = result.scalar_one_or_none()
        
        if payment:
            payment.status = PaymentStatus.SUCCEEDED
            payment.completed_at = datetime.utcnow()
            await db.commit()
    
    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]
        intent_id = payment_intent["id"]
        
        result = await db.execute(
            select(Payment).where(Payment.stripe_payment_intent_id == intent_id)
        )
        payment = result.scalar_one_or_none()
        
        if payment:
            payment.status = PaymentStatus.FAILED
            await db.commit()
    
    return {"status": "success"}


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Payment)
        .join(Ride)
        .where(
            Payment.id == payment_id,
            (Ride.rider_id == user.id) | (Ride.driver_id == user.id)
        )
    )
    payment = result.scalar_one_or_none()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )
    
    return payment
