import pytest
from app.services.auth_service import create_access_token
from app.redis_client import flush_all_seat_locks

@pytest.mark.asyncio
async def test_remaining_ttl_returned_in_matrix(client):
    await flush_all_seat_locks()
    show_id = 1
    seat_id = 20
    user_id = 5

    token = create_access_token({"sub": str(user_id)})
    headers = {"Authorization": f"Bearer {token}"}

    # Hold seat
    hold_res = await client.post(
        f"/api/shows/{show_id}/seats/hold",
        json={"seat_ids": [seat_id]},
        headers=headers,
    )
    assert hold_res.status_code == 200

    # Fetch matrix
    matrix_res = await client.get(f"/api/shows/{show_id}/seats", headers=headers)
    assert matrix_res.status_code == 200
    data = matrix_res.json()

    # Find the held seat in rows
    held_seat = None
    for r in data["rows"]:
        for s in r["seats"]:
            if s["id"] == seat_id:
                held_seat = s
                break

    assert held_seat is not None
    assert held_seat["status"] == "HELD"
    assert held_seat["held_by_me"] is True
    assert held_seat["remaining_ttl_seconds"] is not None
    assert 580 <= held_seat["remaining_ttl_seconds"] <= 600

@pytest.mark.asyncio
async def test_mock_payment_card_failure_retains_hold(client):
    await flush_all_seat_locks()
    show_id = 1
    seat_id = 22
    user_id = 6

    token = create_access_token({"sub": str(user_id)})
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Hold seat
    await client.post(
        f"/api/shows/{show_id}/seats/hold",
        json={"seat_ids": [seat_id]},
        headers=headers,
    )

    # 2. Checkout with test failure card
    fail_card = {
        "card_number": "4000000000000002",
        "card_holder": "Decline User",
        "expiry_month": "11",
        "expiry_year": "29",
        "cvv": "999",
    }

    resp = await client.post(
        "/api/checkout",
        json={
            "show_id": show_id,
            "seat_ids": [seat_id],
            "payment": fail_card,
        },
        headers=headers,
    )
    assert resp.status_code == 402  # Payment required/declined

    # 3. Verify seat is still HELD by user
    matrix_res = await client.get(f"/api/shows/{show_id}/seats", headers=headers)
    assert matrix_res.status_code == 200
    data = matrix_res.json()
    held_seat = None
    for r in data["rows"]:
        for s in r["seats"]:
            if s["id"] == seat_id:
                held_seat = s
                break
    assert held_seat["status"] == "HELD"
    assert held_seat["held_by_me"] is True
