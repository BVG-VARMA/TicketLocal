import asyncio
import pytest
from app.services.auth_service import create_access_token
from app.redis_client import flush_all_seat_locks

@pytest.mark.asyncio
async def test_50_concurrent_users_single_seat_contention(client):
    """
    Test requirement: 50 simultaneous users try to hold the same seat.
    Exactly ONE succeeds (200 OK), and the remaining 49 get 423 Locked.
    """
    await flush_all_seat_locks()

    show_id = 1
    target_seat_id = 1
    num_users = 50

    async def attempt_hold(user_id: int):
        token = create_access_token({"sub": str(user_id)})
        headers = {"Authorization": f"Bearer {token}"}
        resp = await client.post(
            f"/api/shows/{show_id}/seats/hold",
            json={"seat_ids": [target_seat_id]},
            headers=headers,
        )
        return resp.status_code, resp.json()

    # Fire all 50 concurrent requests simultaneously using asyncio.gather
    tasks = [attempt_hold(uid) for uid in range(1, num_users + 1)]
    results = await asyncio.gather(*tasks)

    status_codes = [r[0] for r in results]
    success_count = status_codes.count(200)
    locked_count = status_codes.count(423)

    assert success_count == 1, f"Expected exactly 1 winner, but got {success_count} (statuses: {status_codes})"
    assert locked_count == num_users - 1, f"Expected {num_users - 1} 423s, but got {locked_count}"

@pytest.mark.asyncio
async def test_same_user_idempotent_hold(client):
    """
    Holds by the same user should be idempotent.
    """
    await flush_all_seat_locks()
    show_id = 1
    target_seat_id = 5
    user_id = 10

    token = create_access_token({"sub": str(user_id)})
    headers = {"Authorization": f"Bearer {token}"}

    # First hold
    resp1 = await client.post(
        f"/api/shows/{show_id}/seats/hold",
        json={"seat_ids": [target_seat_id]},
        headers=headers,
    )
    assert resp1.status_code == 200

    # Second hold (same user)
    resp2 = await client.post(
        f"/api/shows/{show_id}/seats/hold",
        json={"seat_ids": [target_seat_id]},
        headers=headers,
    )
    assert resp2.status_code == 200
    assert resp2.json()["success"] is True

@pytest.mark.asyncio
async def test_release_and_reacquire(client):
    await flush_all_seat_locks()
    show_id = 1
    target_seat_id = 8

    token1 = create_access_token({"sub": "11"})
    token2 = create_access_token({"sub": "12"})

    # User 1 holds seat
    r1 = await client.post(
        f"/api/shows/{show_id}/seats/hold",
        json={"seat_ids": [target_seat_id]},
        headers={"Authorization": f"Bearer {token1}"},
    )
    assert r1.status_code == 200

    # User 2 gets 423
    r2 = await client.post(
        f"/api/shows/{show_id}/seats/hold",
        json={"seat_ids": [target_seat_id]},
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r2.status_code == 423

    # User 1 releases
    r_del = await client.request(
        "DELETE",
        f"/api/shows/{show_id}/seats/hold",
        json={"seat_ids": [target_seat_id]},
        headers={"Authorization": f"Bearer {token1}"},
    )
    assert r_del.status_code == 200

    # User 2 can now hold successfully
    r3 = await client.post(
        f"/api/shows/{show_id}/seats/hold",
        json={"seat_ids": [target_seat_id]},
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert r3.status_code == 200
