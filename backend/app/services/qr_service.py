import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from starlette.concurrency import run_in_threadpool
import qrcode
from PIL import Image, ImageDraw, ImageFont
from app.config import settings

logger = logging.getLogger("ticketlocal.qr")

def _generate_qr_sync(
    booking_id: int,
    booking_ref: str,
    content_title: str,
    theater_name: str,
    show_time: str,
    seats: List[str],
    total_amount: float,
) -> str:
    """
    Synchronously generates a QR code PNG ticket with visual styling.
    """
    settings.TICKETS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"ticket_booking_{booking_id}.png"
    filepath = settings.TICKETS_DIR / filename

    payload = {
        "app": "TicketLocal",
        "booking_id": booking_id,
        "booking_ref": booking_ref,
        "content": content_title,
        "theater": theater_name,
        "time": show_time,
        "seats": seats,
        "total": total_amount,
        "status": "PAID",
    }
    payload_str = json.dumps(payload)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(payload_str)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#111827", back_color="#FFFFFF").convert("RGBA")

    # Add header/card frame
    card_width = img.width + 40
    card_height = img.height + 120
    card = Image.new("RGBA", (card_width, card_height), "#0F172A")
    draw = ImageDraw.Draw(card)

    # Draw rounded rectangle for QR background
    draw.rounded_rectangle(
        [(15, 80), (card_width - 15, card_height - 20)],
        radius=12,
        fill="#FFFFFF",
    )

    # Paste QR image inside card
    card.paste(img, (20, 90), img)

    # Draw Ticket Title
    draw.text((25, 20), "TICKETLOCAL PASS", fill="#F43F5E")
    draw.text((25, 45), f"Booking #{booking_id} • {content_title[:22]}", fill="#F8FAFC")

    card.save(filepath, "PNG")
    return str(filepath)

async def generate_ticket_qr(
    booking_id: int,
    booking_ref: str,
    content_title: str,
    theater_name: str,
    show_time: str,
    seats: List[str],
    total_amount: float,
) -> str:
    """
    Asynchronously generates the QR code PNG ticket using threadpool execution.
    """
    return await run_in_threadpool(
        _generate_qr_sync,
        booking_id=booking_id,
        booking_ref=booking_ref,
        content_title=content_title,
        theater_name=theater_name,
        show_time=show_time,
        seats=seats,
        total_amount=total_amount,
    )
