from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.catalog_service import CatalogService
from app.schemas import CityOut, MovieOut, TheaterOut, ShowOut

router = APIRouter(tags=["Catalog"])

@router.get("/cities", response_model=List[CityOut])
async def list_cities(db: AsyncSession = Depends(get_db)):
    """
    Returns list of all available cities.
    """
    return await CatalogService.get_cities(db)

@router.get("/movies", response_model=List[MovieOut])
async def list_movies(
    featured: bool = Query(False, description="Filter featured movies only"),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns catalog of movies currently showing or upcoming.
    """
    return await CatalogService.get_movies(db, featured_only=featured)

@router.get("/movies/{movie_id}", response_model=MovieOut)
async def get_movie_detail(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await CatalogService.get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.get("/theaters", response_model=List[TheaterOut])
async def list_theaters(
    city: str = Query("Hyderabad", description="City name"),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns theaters and screens in a given city.
    """
    return await CatalogService.get_theaters_by_city(db, city_name=city)

@router.get("/shows", response_model=List[ShowOut])
async def list_shows(
    city: Optional[str] = Query(None, description="Filter by city name"),
    date: Optional[str] = Query(None, description="Filter by show date YYYY-MM-DD"),
    movie_id: Optional[int] = Query(None, description="Filter by movie ID"),
    theater_id: Optional[int] = Query(None, description="Filter by theater ID"),
    format: Optional[str] = Query(None, description="Filter by format e.g. IMAX 3D, 4DX"),
    db: AsyncSession = Depends(get_db)
):
    """
    FR2.2 Complex Relational Catalog Query:
    Joins across Cities -> Theaters -> Screens -> Shows -> Movies
    Includes dynamic pricing and surge multiplier.
    """
    return await CatalogService.get_shows(
        db=db,
        city=city,
        date=date,
        movie_id=movie_id,
        theater_id=theater_id,
        format_filter=format,
    )
