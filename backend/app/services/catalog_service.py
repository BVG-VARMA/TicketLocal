from typing import List, Optional, Dict, Any
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import City, Theater, Screen, Seat, Movie, Show

class CatalogService:
    @staticmethod
    async def get_cities(db: AsyncSession) -> List[City]:
        result = await db.execute(select(City).order_by(City.name))
        return list(result.scalars().all())

    @staticmethod
    async def get_movies(db: AsyncSession, featured_only: bool = False) -> List[Movie]:
        query = select(Movie)
        if featured_only:
            query = query.where(Movie.is_featured == True)
        result = await db.execute(query.order_by(Movie.rating.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def get_movie_by_id(db: AsyncSession, movie_id: int) -> Optional[Movie]:
        result = await db.execute(select(Movie).where(Movie.id == movie_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_theaters_by_city(db: AsyncSession, city_name: str) -> List[Theater]:
        result = await db.execute(
            select(Theater)
            .join(City)
            .where(City.name.ilike(f"%{city_name}%"))
            .options(selectinload(Theater.screens))
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_shows(
        db: AsyncSession,
        city: Optional[str] = None,
        date: Optional[str] = None,
        movie_id: Optional[int] = None,
        theater_id: Optional[int] = None,
        format_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Executes multi-table relational join:
        City -> Theater -> Screen -> Show -> Movie
        with dynamic pricing calculation.
        """
        query = (
            select(Show)
            .join(Screen, Show.screen_id == Screen.id)
            .join(Theater, Screen.theater_id == Theater.id)
            .join(City, Theater.city_id == City.id)
            .join(Movie, Show.movie_id == Movie.id)
            .options(
                joinedload(Show.movie),
                joinedload(Show.screen).joinedload(Screen.theater).joinedload(Theater.city),
            )
        )

        filters = []
        if city:
            filters.append(City.name.ilike(f"%{city}%"))
        if date:
            filters.append(Show.show_date == date)
        if movie_id:
            filters.append(Show.movie_id == movie_id)
        if theater_id:
            filters.append(Theater.id == theater_id)
        if format_filter:
            filters.append(Show.format.ilike(f"%{format_filter}%"))

        if filters:
            query = query.where(and_(*filters))

        query = query.order_by(Show.show_date, Show.start_time)
        result = await db.execute(query)
        shows = result.unique().scalars().all()

        output = []
        for show in shows:
            surge = show.surge_multiplier or 1.0
            price_map = {
                "RECLINER": round(450.0 * surge, 2),
                "PRIME": round(280.0 * surge, 2),
                "CLASSIC": round(180.0 * surge, 2),
            }
            show_dict = {
                "id": show.id,
                "screen_id": show.screen_id,
                "movie_id": show.movie_id,
                "show_date": show.show_date,
                "start_time": show.start_time,
                "end_time": show.end_time,
                "language": show.language,
                "format": show.format,
                "surge_multiplier": show.surge_multiplier,
                "movie": show.movie,
                "screen": show.screen,
                "theater": show.screen.theater if show.screen else None,
                "price_range": price_map,
            }
            output.append(show_dict)

        return output
