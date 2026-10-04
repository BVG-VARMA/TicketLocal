import json
import logging
from pathlib import Path
import qrcode
from PIL import Image, ImageDraw, ImageFont
from app.config import settings

logger = logging.getLogger("ticketlocal.ticket")

class TicketService:
    @staticmethod
    def generate_qr_ticket(
        ticket_id: str,
        booking_ref: str,
        show_id: int,
        movie_title: str,
        theater_name: str,
        seats: list,
        status: str = "PAID",
        timestamp: str = None
    ) -> str:
        """
        Generates a local QR code PNG file with booking payload,
        saves to static/tickets/{booking_ref}.png and returns the relative/absolute path.
        """
        payload = {
            "ticket_id": ticket_id,
            "booking_ref": booking_ref,
            "show_id": show_id,
            "movie": movie_title,
            "theater": theater_name,
            "seats": seats,
            "status": status,
            "timestamp": timestamp,
            "verifier": "NEXORA-SECURE-V1",
        }

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(payload))
        qr.make(fit=True)

        img = qr.make_image(fill_color="#e11d48", back_color="#0f172a") # Crimson red on dark slate background
        
        file_name = f"ticket_{booking_ref}.png"
        file_path = settings.TICKETS_DIR / file_name
        img.save(str(file_path))
        
        logger.info(f"Generated local QR ticket at {file_path}")
        return f"/static/tickets/{file_name}"
