import stripe
from typing import Optional
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(amount: float, currency: str = "usd", metadata: Optional[dict] = None) -> dict:
    """
    Create a Stripe PaymentIntent
    
    Args:
        amount: Amount in smallest currency unit (cents for USD)
        currency: Currency code (default: usd)
        metadata: Additional metadata to attach
    
    Returns:
        PaymentIntent object
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency=currency,
            metadata=metadata or {},
            automatic_payment_methods={
                "enabled": True,
            },
        )
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id,
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


def confirm_payment_intent(payment_intent_id: str) -> bool:
    """Confirm a payment intent (typically called from webhook)"""
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return intent.status == "succeeded"
    except stripe.error.StripeError:
        return False


def get_payment_intent(payment_intent_id: str) -> dict:
    """Retrieve payment intent details"""
    try:
        return stripe.PaymentIntent.retrieve(payment_intent_id)
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


