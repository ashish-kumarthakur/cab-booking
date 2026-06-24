from app.tasks.celery_app import celery_app
from weasyprint import HTML
from typing import Optional
import os


@celery_app.task
def generate_receipt_pdf(ride_id: str, rider_name: str, driver_name: str, 
                        fare: float, distance_km: float, duration_min: float) -> Optional[str]:
    """
    Generate PDF receipt for a completed ride
    
    Returns:
        Path to generated PDF file
    """
    try:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 20px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .details {{ margin: 20px 0; }}
                .detail-row {{ display: flex; justify-content: space-between; margin: 10px 0; }}
                .total {{ font-size: 18px; font-weight: bold; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Ride Receipt</h1>
                <p>Ride ID: {ride_id}</p>
            </div>
            <div class="details">
                <div class="detail-row">
                    <span>Rider:</span>
                    <span>{rider_name}</span>
                </div>
                <div class="detail-row">
                    <span>Driver:</span>
                    <span>{driver_name}</span>
                </div>
                <div class="detail-row">
                    <span>Distance:</span>
                    <span>{distance_km:.2f} km</span>
                </div>
                <div class="detail-row">
                    <span>Duration:</span>
                    <span>{duration_min:.1f} minutes</span>
                </div>
                <div class="detail-row total">
                    <span>Total Fare:</span>
                    <span>${fare:.2f}</span>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create receipts directory if it doesn't exist
        os.makedirs("receipts", exist_ok=True)
        pdf_path = f"receipts/receipt_{ride_id}.pdf"
        
        HTML(string=html_content).write_pdf(pdf_path)
        
        return pdf_path
    
    except Exception as e:
        print(f"Error generating receipt: {e}")
        return None


@celery_app.task
def send_receipt_email(ride_id: str, rider_email: str, pdf_path: str):
    """
    Send receipt email to rider
    
    In production, integrate with email service (SendGrid, AWS SES, etc.)
    """
    try:
        # Placeholder for email sending
        # In production, use an email service
        print(f"Sending receipt email to {rider_email} for ride {ride_id}")
        print(f"PDF path: {pdf_path}")
        
        # Example with smtplib or SendGrid:
        # send_email(rider_email, "Your Ride Receipt", pdf_path)
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


