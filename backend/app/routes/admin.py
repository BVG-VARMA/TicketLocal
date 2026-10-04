from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.admin_service import AdminService
from app.schemas import (
    MovieCreate, MovieUpdate, MovieOut,
    TheaterCreate, TheaterUpdate, TheaterOut,
    ScreenCreate, ScreenOut,
    ShowCreate, ShowOut,
    AdminStatsOut
)

router = APIRouter(prefix="/admin", tags=["Admin Portal"])

@router.get("/stats", response_model=AdminStatsOut)
async def get_admin_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """
    Returns platform statistics: Total Movies, Theaters, Screens, Shows, Bookings, and Total Revenue.
    """
    return await AdminService.get_stats(db)

# --- Movie Operations ---
@router.post("/movies", response_model=MovieOut, status_code=status.HTTP_201_CREATED)
async def add_movie(data: MovieCreate, db: AsyncSession = Depends(get_db)):
    """
    Admin: Add a new movie to the CinePass catalog.
    """
    return await AdminService.create_movie(db, data)

@router.put("/movies/{movie_id}", response_model=MovieOut)
async def update_movie(movie_id: int, data: MovieUpdate, db: AsyncSession = Depends(get_db)):
    """
    Admin: Update movie details.
    """
    movie = await AdminService.update_movie(db, movie_id, data)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.delete("/movies/{movie_id}", status_code=status.HTTP_200_OK)
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    """
    Admin: Delete a movie from CinePass.
    """
    success = await AdminService.delete_movie(db, movie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie successfully deleted", "movie_id": movie_id}

# --- Theater Operations ---
@router.post("/theaters", response_model=TheaterOut, status_code=status.HTTP_201_CREATED)
async def add_theater(data: TheaterCreate, db: AsyncSession = Depends(get_db)):
    """
    Admin: Add a new theater to a city.
    """
    return await AdminService.create_theater(db, data)

@router.put("/theaters/{theater_id}", response_model=TheaterOut)
async def update_theater(theater_id: int, data: TheaterUpdate, db: AsyncSession = Depends(get_db)):
    """
    Admin: Update theater information.
    """
    theater = await AdminService.update_theater(db, theater_id, data)
    if not theater:
        raise HTTPException(status_code=404, detail="Theater not found")
    return theater

@router.delete("/theaters/{theater_id}", status_code=status.HTTP_200_OK)
async def delete_theater(theater_id: int, db: AsyncSession = Depends(get_db)):
    """
    Admin: Delete a theater and associated screens/shows.
    """
    success = await AdminService.delete_theater(db, theater_id)
    if not success:
        raise HTTPException(status_code=404, detail="Theater not found")
    return {"message": "Theater successfully deleted", "theater_id": theater_id}

# --- Screen Operations ---
@router.post("/screens", response_model=ScreenOut, status_code=status.HTTP_201_CREATED)
async def add_screen(data: ScreenCreate, db: AsyncSession = Depends(get_db)):
    """
    Admin: Add a screen to a theater with automatic BookMyShow tiered seat matrix (Recliner, Prime, Classic).
    """
    return await AdminService.create_screen(db, data)

@router.delete("/screens/{screen_id}", status_code=status.HTTP_200_OK)
async def delete_screen(screen_id: int, db: AsyncSession = Depends(get_db)):
    """
    Admin: Delete a screen.
    """
    success = await AdminService.delete_screen(db, screen_id)
    if not success:
        raise HTTPException(status_code=404, detail="Screen not found")
    return {"message": "Screen successfully deleted", "screen_id": screen_id}

# --- Show Operations ---
@router.post("/shows", response_model=ShowOut, status_code=status.HTTP_201_CREATED)
async def schedule_show(data: ShowCreate, db: AsyncSession = Depends(get_db)):
    """
    Admin: Schedule a movie showtime on a theater screen.
    """
    return await AdminService.create_show(db, data)

@router.delete("/shows/{show_id}", status_code=status.HTTP_200_OK)
async def cancel_show(show_id: int, db: AsyncSession = Depends(get_db)):
    """
    Admin: Cancel/Delete a scheduled show.
    """
    success = await AdminService.delete_show(db, show_id)
    if not success:
        raise HTTPException(status_code=404, detail="Show not found")
    return {"message": "Show successfully deleted", "show_id": show_id}
