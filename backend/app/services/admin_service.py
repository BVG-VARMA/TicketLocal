import re
from typing import List, Optional
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Movie, Theater, Screen, Seat, Show, City, Booking
from app.schemas import (
    MovieCreate, MovieUpdate, TheaterCreate, TheaterUpdate, 
    ScreenCreate, ShowCreate, AdminStatsOut
)

class AdminService:
    @staticmethod
    def slugify(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        return re.sub(r'[-\s]+', '-', text)

    @staticmethod
    async def get_stats(db: AsyncSession) -> AdminStatsOut:
        m_count = await db.scalar(select(func.count(Movie.id)))
        t_count = await db.scalar(select(func.count(Theater.id)))
        s_count = await db.scalar(select(func.count(Screen.id)))
        sh_count = await db.scalar(select(func.count(Show.id)))
        b_count = await db.scalar(select(func.count(Booking.id)))
        revenue = await db.scalar(select(func.sum(Booking.total_amount))) or 0.0

        return AdminStatsOut(
            total_movies=m_count or 0,
            total_theaters=t_count or 0,
            total_screens=s_count or 0,
            total_shows=sh_count or 0,
            total_bookings=b_count or 0,
            total_revenue=float(revenue)
        )

    # --- Movies ---
    @staticmethod
    async def create_movie(db: AsyncSession, data: MovieCreate) -> Movie:
        base_slug = AdminService.slugify(data.title)
        slug = base_slug
        count = 1
        while (await db.execute(select(Movie).where(Movie.slug == slug))).scalar_one_or_none():
            slug = f"{base_slug}-{count}"
            count += 1

        movie = Movie(
            title=data.title,
            slug=slug,
            synopsis=data.synopsis,
            poster_url=data.poster_url,
            backdrop_url=data.backdrop_url or data.poster_url,
            duration_min=data.duration_min,
            rating=data.rating,
            certificate=data.certificate,
            genres=data.genres,
            languages=data.languages,
            release_date=data.release_date,
            is_featured=data.is_featured
        )
        db.add(movie)
        await db.commit()
        await db.refresh(movie)
        return movie

    @staticmethod
    async def update_movie(db: AsyncSession, movie_id: int, data: MovieUpdate) -> Optional[Movie]:
        res = await db.execute(select(Movie).where(Movie.id == movie_id))
        movie = res.scalar_one_or_none()
        if not movie:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, val in update_data.items():
            setattr(movie, key, val)

        await db.commit()
        await db.refresh(movie)
        return movie

    @staticmethod
    async def delete_movie(db: AsyncSession, movie_id: int) -> bool:
        res = await db.execute(select(Movie).where(Movie.id == movie_id))
        movie = res.scalar_one_or_none()
        if not movie:
            return False
        await db.delete(movie)
        await db.commit()
        return True

    # --- Theaters ---
    @staticmethod
    async def create_theater(db: AsyncSession, data: TheaterCreate) -> Theater:
        # Find or create City
        city_res = await db.execute(select(City).where(City.name == data.city_name))
        city = city_res.scalar_one_or_none()
        if not city:
            city_slug = AdminService.slugify(data.city_name)
            city = City(name=data.city_name, state="India", slug=city_slug)
            db.add(city)
            await db.flush()

        theater = Theater(
            city_id=city.id,
            name=data.name,
            address=data.address,
            amenities=data.amenities or "Parking, Food Court, Wheelchair Access, M-Ticket, Dolby Atmos",
            latitude=data.latitude or 17.3850,
            longitude=data.longitude or 78.4867
        )
        db.add(theater)
        await db.commit()
        await db.refresh(theater)
        return theater

    @staticmethod
    async def update_theater(db: AsyncSession, theater_id: int, data: TheaterUpdate) -> Optional[Theater]:
        res = await db.execute(select(Theater).where(Theater.id == theater_id))
        theater = res.scalar_one_or_none()
        if not theater:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, val in update_data.items():
            setattr(theater, key, val)

        await db.commit()
        await db.refresh(theater)
        return theater

    @staticmethod
    async def delete_theater(db: AsyncSession, theater_id: int) -> bool:
        res = await db.execute(select(Theater).where(Theater.id == theater_id))
        theater = res.scalar_one_or_none()
        if not theater:
            return False
        await db.delete(theater)
        await db.commit()
        return True

    # --- Screens & BMS Seat Generation ---
    @staticmethod
    async def create_screen(db: AsyncSession, data: ScreenCreate) -> Screen:
        # Calculate total seats
        total_rows = data.rows_recliner + data.rows_prime + data.rows_classic
        total_seats = total_rows * data.seats_per_row

        screen = Screen(
            theater_id=data.theater_id,
            name=data.name,
            format=data.format,
            total_seats=total_seats
        )
        db.add(screen)
        await db.flush()

        # Generate BookMyShow Realistic Tiered Seat Matrix
        # Row letters: A, B, C, D, E, F, G, H, J, K...
        row_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P"]
        current_row_idx = 0

        # 1. Recliner Seats (Top Tier, e.g. Row A-B)
        for _ in range(data.rows_recliner):
            if current_row_idx < len(row_letters):
                r = row_letters[current_row_idx]
                for num in range(1, data.seats_per_row + 1):
                    seat = Seat(
                        screen_id=screen.id,
                        row=r,
                        number=num,
                        seat_type="RECLINER",
                        base_price=350.0
                    )
                    db.add(seat)
                current_row_idx += 1

        # 2. Prime Seats (Middle Tier, e.g. Row C-F)
        for _ in range(data.rows_prime):
            if current_row_idx < len(row_letters):
                r = row_letters[current_row_idx]
                for num in range(1, data.seats_per_row + 1):
                    seat = Seat(
                        screen_id=screen.id,
                        row=r,
                        number=num,
                        seat_type="PRIME",
                        base_price=220.0
                    )
                    db.add(seat)
                current_row_idx += 1

        # 3. Classic Seats (Standard Tier, e.g. Row G-J)
        for _ in range(data.rows_classic):
            if current_row_idx < len(row_letters):
                r = row_letters[current_row_idx]
                for num in range(1, data.seats_per_row + 1):
                    seat = Seat(
                        screen_id=screen.id,
                        row=r,
                        number=num,
                        seat_type="CLASSIC",
                        base_price=150.0
                    )
                    db.add(seat)
                current_row_idx += 1

        await db.commit()
        await db.refresh(screen)
        return screen

    @staticmethod
    async def delete_screen(db: AsyncSession, screen_id: int) -> bool:
        res = await db.execute(select(Screen).where(Screen.id == screen_id))
        screen = res.scalar_one_or_none()
        if not screen:
            return False
        await db.delete(screen)
        await db.commit()
        return True

    # --- Shows ---
    @staticmethod
    async def create_show(db: AsyncSession, data: ShowCreate) -> Show:
        show = Show(
            movie_id=data.movie_id,
            screen_id=data.screen_id,
            show_date=data.show_date,
            start_time=data.start_time,
            end_time=data.end_time,
            language=data.language,
            format=data.format,
            surge_multiplier=data.surge_multiplier
        )
        db.add(show)
        await db.commit()
        await db.refresh(show)
        return show

    @staticmethod
    async def delete_show(db: AsyncSession, show_id: int) -> bool:
        res = await db.execute(select(Show).where(Show.id == show_id))
        show = res.scalar_one_or_none()
        if not show:
            return False
        await db.delete(show)
        await db.commit()
        return True
