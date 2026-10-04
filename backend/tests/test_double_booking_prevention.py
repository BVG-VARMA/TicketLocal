import pytest
from app.services.auth_service import create_access_token
from app.redis_client import flush_all_seat_locks, acquire_atomic_seat_locks

@pytest.mark.asyncio
async def test_db_unique_constraint_prevents_double_booking_under_redis_wipe(client):
    """
    Test requirement: Redis wiped mid-checkout, then two users attempt to pay for the same seat.
    One succeeds (200 OK), and the second receives 409 Conflict due to the PostgreSQL
    UNIQUE (show_id, seat_id) constraint.
    """
    await flush_all_seat_locks()
    show_id = 1
    target_seat_id = 15

    user1_id = 1
    user2_id = 2

    token1 = create_access_token({"sub": str(user1_id)})
    token2 = create_access_token({"sub": str(user2_id)})

    valid_card = {
        "card_number": "4000123456789010",
        "card_holder": "John Doe",
        "expiry_month": "12",
        "expiry_year": "28",
        "cvv": "123",
    }

    # Step 1: User 1 acquires hold
    await acquire_atomic_seat_locks(show_id, [target_seat_id], str(user1_id))

    # Step 2: User 1 checks out successfully
    resp1 = await client.post(
        "/api/checkout",
        json={
            "show_id": show_id,
            "seat_ids": [target_seat_id],
            "payment": valid_card,
        },
        headers={"Authorization": f"Bearer {token1}"},
    )
    assert resp1.status_code == 200, f"First checkout should succeed, got {resp1.status_code}: {resp1.text}"

    # Step 3: Chaos event - Redis is wiped completely!
    await flush_all_seat_locks()

    # Step 4: User 2 tries to hold or checkout the exact same seat because Redis lock is gone
    # Hold fails because SeatService verifies DB booked status first, returning 423
    hold_resp = await client.post(
        f"/api/shows/{show_id}/seats/hold",
        json={"seat_ids": [target_seat_id]},
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert hold_resp.status_code == 423, "DB check prevented holding already booked seat"

    # And if User 2 bypasses hold or force-locks in Redis and checks out:
    await acquire_atomic_seat_locks(show_id, [target_seat_id], str(user2_id))
    resp2 = await client.post(
        "/api/checkout",
        json={
            "show_id": show_id,
            "seat_ids": [target_seat_id],
            "payment": valid_card,
        },
        headers={"Authorization": f"Bearer {token2}"},
    )

    # Database UNIQUE constraint prevents double-booking, returning 409 Conflict
    assert resp2.status_code == 409, f"Expected 409 Conflict on double booking, got {resp2.status_code}: {resp2.text}"
