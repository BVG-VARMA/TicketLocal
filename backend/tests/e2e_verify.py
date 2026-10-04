import httpx
import json

def run_e2e_verification():
    base = "http://127.0.0.1:8000"
    client = httpx.Client(base_url=base, timeout=20.0)

    print("=== 1. Testing Login ===")
    login_resp = client.post("/api/auth/login", json={"email": "demo@ticketlocal.com", "password": "Demo@1234"})
    print("Login Status:", login_resp.status_code)
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    print("\n=== 2. Fetching Cities & Content ===")
    cities = client.get("/api/cities").json()
    print("Cities found:", [c["name"] for c in cities])
    movies = client.get("/api/content?type=MOVIE").json()
    print("Movies found:", len(movies), "| First Movie:", movies[0]["title"])

    print("\n=== 3. Fetching Shows in Hyderabad ===")
    shows = client.get("/api/shows?city=Hyderabad").json()
    print("Theaters with active shows in Hyderabad:", len(shows))
    target_show = shows[0]["shows"][0]
    show_id = target_show["id"]
    print(f"Selected Show ID: {show_id} for screen {target_show['screen']['name']}")

    print("\n=== 4. Fetching Live 2D Seat Matrix ===")
    matrix = client.get(f"/api/shows/{show_id}/seats", headers=headers).json()
    print(f"Matrix rows: {len(matrix['rows'])} | Available: {matrix['total_available']} | Held: {matrix['total_held']}")
    target_seats = [matrix["rows"][0]["seats"][0]["id"], matrix["rows"][0]["seats"][1]["id"]]
    print(f"Selected Target Seat IDs: {target_seats}")

    print("\n=== 5. Acquiring Atomic 600s Redis Seat Hold ===")
    hold_resp = client.post(f"/api/shows/{show_id}/seats/hold", json={"seat_ids": target_seats}, headers=headers)
    print("Hold Status:", hold_resp.status_code, hold_resp.json())
    assert hold_resp.status_code == 200

    print("\n=== 6. Calculating Cart Quote with Fee & Taxes ===")
    quote_resp = client.post("/api/cart/quote", json={"show_id": show_id, "seat_ids": target_seats}, headers=headers)
    quote = quote_resp.json()
    print(f"Subtotal: Rs.{quote['subtotal']} | Fee (10%): Rs.{quote['convenience_fee']} | GST (18%): Rs.{quote['tax']} | Total: Rs.{quote['total']}")
    assert quote_resp.status_code == 200

    print("\n=== 7. Executing Checkout & Minting QR Ticket (2s async simulation) ===")
    checkout_payload = {
        "show_id": show_id,
        "seat_ids": target_seats,
        "payment": {
            "card_number": "4000123456789010",
            "card_holder": "Demo Citizen",
            "expiry_month": "12",
            "expiry_year": "28",
            "cvv": "123",
        },
    }
    checkout_resp = client.post("/api/checkout", json=checkout_payload, headers=headers)
    print("Checkout Status:", checkout_resp.status_code, checkout_resp.json())
    assert checkout_resp.status_code == 200
    booking_id = checkout_resp.json()["booking_id"]
    ticket_id = checkout_resp.json()["ticket_id"]

    print("\n=== 8. Verifying QR Ticket Download ===")
    qr_resp = client.get(f"/api/tickets/{ticket_id}/qr", headers=headers)
    print(f"QR Download Status: {qr_resp.status_code} | Image Size: {len(qr_resp.content)} bytes")
    assert qr_resp.status_code == 200

    print("\n=== 9. Verifying User Bookings ===")
    my_bookings = client.get("/api/bookings", headers=headers).json()
    print(f"My Bookings count: {len(my_bookings)} | Latest booking ID: {my_bookings[0]['id']} ({my_bookings[0]['status']})")
    assert len(my_bookings) >= 1

    print("\n=== 10. Checking Telemetry & Metrics Lite ===")
    metrics = client.get("/api/metrics-lite").json()
    print("Metrics Lite:\n", json.dumps(metrics, indent=2))

    print("\nSUCCESS: All End-to-End steps verified successfully against live TicketLocal server!")

if __name__ == "__main__":
    run_e2e_verification()
