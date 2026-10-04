import asyncio
import logging
from datetime import datetime, timedelta, time
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import AsyncSessionLocal, engine, Base
from app.models import (
    User, City, Theater, Screen, Seat, Content, Show,
    PricingRule, ContentType, SeatType
)
from app.services.auth_service import get_password_hash

logger = logging.getLogger("ticketlocal.seed")

async def seed_database(session: AsyncSession):
    # 1. Check if database already seeded
    res = await session.execute(select(User).where(User.email == "demo@ticketlocal.com"))
    if res.scalar_one_or_none():
        logger.info("Database already seeded with demo user. Skipping.")
        return

    logger.info("Seeding database with fresh TicketLocal data...")

    # 2. Pricing Rules
    pricing_rules = [
        PricingRule(seat_type=SeatType.STANDARD, multiplier=1.0, weekend_surge=1.25, prime_time_surge=1.15),
        PricingRule(seat_type=SeatType.PREMIUM, multiplier=1.4, weekend_surge=1.25, prime_time_surge=1.15),
        PricingRule(seat_type=SeatType.RECLINER, multiplier=1.8, weekend_surge=1.25, prime_time_surge=1.15),
    ]
    session.add_all(pricing_rules)

    # 3. Demo User & Admin
    demo_user = User(
        name="Demo Citizen",
        email="demo@ticketlocal.com",
        password_hash=get_password_hash("Demo@1234"),
    )
    admin_user = User(
        name="Cinema Admin",
        email="admin@ticketlocal.com",
        password_hash=get_password_hash("Admin@1234"),
    )
    session.add_all([demo_user, admin_user])
    await session.flush()

    # 4. Cities
    hyderabad = City(name="Hyderabad")
    bangalore = City(name="Bangalore")
    mumbai = City(name="Mumbai")
    session.add_all([hyderabad, bangalore, mumbai])
    await session.flush()

    # 5. Theaters & Screens & Seats
    theaters_data = [
        # Hyderabad
        {"city": hyderabad, "name": "PVR Forum Sujana Mall", "address": "Kukatpally, Hyderabad"},
        {"city": hyderabad, "name": "Prasads Multiplex & IMAX", "address": "Necklace Road, Hyderabad"},
        {"city": hyderabad, "name": "AMB Cinemas", "address": "Gachibowli, Hyderabad"},
        # Bangalore
        {"city": bangalore, "name": "PVR Vega City Mall", "address": "Bannerghatta Rd, Bangalore"},
        {"city": bangalore, "name": "INOX Garuda Mall", "address": "Magrath Rd, Bangalore"},
        {"city": bangalore, "name": "Cinepolis Forum Shantiniketan", "address": "Whitefield, Bangalore"},
        # Mumbai
        {"city": mumbai, "name": "PVR ICON Phoenix Palladium", "address": "Lower Parel, Mumbai"},
        {"city": mumbai, "name": "INOX Megaplex R-City", "address": "Ghatkopar, Mumbai"},
        {"city": mumbai, "name": "Carnival Moviestar", "address": "Andheri West, Mumbai"},
    ]

    screens_list = []
    for t_data in theaters_data:
        theater = Theater(city_id=t_data["city"].id, name=t_data["name"], address=t_data["address"])
        session.add(theater)
        await session.flush()

        # Add 2-3 screens per theater
        for s_idx in range(1, 4):
            rows_cnt = 8 if s_idx == 1 else 10
            cols_cnt = 10 if s_idx == 1 else 12
            screen = Screen(
                theater_id=theater.id,
                name=f"Screen {s_idx} ({'IMAX Laser' if s_idx == 1 else 'Dolby Atmos 4K' if s_idx == 2 else 'VIP Luxe'})",
                rows=rows_cnt,
                cols=cols_cnt,
                layout_config={"recliner_rows": ["A"], "premium_rows": ["B", "C", "D"], "standard_rows": ["E", "F", "G", "H", "I", "J"]},
            )
            session.add(screen)
            await session.flush()
            screens_list.append(screen)

            # Generate seats for screen
            row_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"][:rows_cnt]
            seats_to_add = []
            for r_idx, r_label in enumerate(row_letters):
                if r_label == "A":
                    s_type = SeatType.RECLINER
                elif r_label in ["B", "C", "D"]:
                    s_type = SeatType.PREMIUM
                else:
                    s_type = SeatType.STANDARD

                for num in range(1, cols_cnt + 1):
                    seats_to_add.append(
                        Seat(
                            screen_id=screen.id,
                            row_label=r_label,
                            seat_number=num,
                            seat_type=s_type,
                        )
                    )
            session.add_all(seats_to_add)

    await session.flush()

    # 6. Content (8+ Movies, 3+ Events)
    contents_data = [
        # Movies
        Content(
            type=ContentType.MOVIE,
            title="Dune: Part Two",
            description="Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.",
            language="English",
            genre="Sci-Fi / Adventure",
            duration_min=166,
            poster_url="http://127.0.0.1:8000/storage/posters/dune2.jpg",
            rating=9.1,
        ),
        Content(
            type=ContentType.MOVIE,
            title="Kalki 2898 AD",
            description="A modern-day avatar of Vishnu descends upon Earth to protect the world from evil forces in a futuristic post-apocalyptic world.",
            language="Telugu / Hindi",
            genre="Sci-Fi / Mythological",
            duration_min=181,
            poster_url="http://127.0.0.1:8000/storage/posters/kalki.jpg",
            rating=8.9,
        ),
        Content(
            type=ContentType.MOVIE,
            title="Oppenheimer",
            description="The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.",
            language="English",
            genre="Biography / Drama",
            duration_min=180,
            poster_url="http://127.0.0.1:8000/storage/posters/oppenheimer.jpg",
            rating=9.3,
        ),
        Content(
            type=ContentType.MOVIE,
            title="Interstellar (Re-Release)",
            description="When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot is tasked to pilot a spacecraft with a team of researchers.",
            language="English",
            genre="Sci-Fi / Epic",
            duration_min=169,
            poster_url="http://127.0.0.1:8000/storage/posters/interstellar.jpg",
            rating=9.4,
        ),
        Content(
            type=ContentType.MOVIE,
            title="Jawan",
            description="A high-octane action thriller outlining the emotional journey of a man set out to rectify the wrongs in society.",
            language="Hindi",
            genre="Action / Thriller",
            duration_min=169,
            poster_url="http://127.0.0.1:8000/storage/posters/jawan.jpg",
            rating=8.4,
        ),
        Content(
            type=ContentType.MOVIE,
            title="Spirited Away (Ghibli Fest)",
            description="A 10-year-old girl wanders into a world ruled by gods, witches, and spirits where humans are changed into beasts.",
            language="Japanese / English",
            genre="Animation / Fantasy",
            duration_min=125,
            poster_url="http://127.0.0.1:8000/storage/posters/spiritedaway.png",
            rating=9.2,
        ),
        Content(
            type=ContentType.MOVIE,
            title="The Dark Knight",
            description="When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of the greatest psychological and physical tests.",
            language="English",
            genre="Action / Crime",
            duration_min=152,
            poster_url="http://127.0.0.1:8000/storage/posters/darkknight.jpg",
            rating=9.5,
        ),
        Content(
            type=ContentType.MOVIE,
            title="Spider-Man: Beyond the Spider-Verse",
            description="Miles Morales catapults across the Multiverse to encounter a team of Spider-People charged with protecting its very existence.",
            language="English",
            genre="Animation / Action",
            duration_min=140,
            poster_url="http://127.0.0.1:8000/storage/posters/spiderman.jpg",
            rating=9.0,
        ),
        # Events
        Content(
            type=ContentType.EVENT,
            title="Coldplay: Music of the Spheres Live",
            description="Experience Coldplay's iconic stadium show live concert tour with laser lights, cosmic visuals, and greatest hits.",
            language="English",
            genre="Live Concert / Music",
            duration_min=150,
            poster_url="http://127.0.0.1:8000/storage/posters/coldplay.jpg",
            rating=9.7,
        ),
        Content(
            type=ContentType.EVENT,
            title="Zakir Khan: Live Comedy Special",
            description="India's favorite standup comedian brings his brand-new hilarious storytelling special 'Tathastu' live on stage.",
            language="Hindi",
            genre="Standup Comedy",
            duration_min=110,
            poster_url="http://127.0.0.1:8000/storage/posters/zakirkhan.jpg",
            rating=9.2,
        ),
        Content(
            type=ContentType.EVENT,
            title="Sunburn Arena EDM Fest 2026",
            description="The premier electronic dance music festival featuring top international DJs, pyro shows, and immersive audio.",
            language="English",
            genre="EDM / Festival",
            duration_min=240,
            poster_url="https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=600&q=80",
            rating=9.4,
        ),
    ]
    session.add_all(contents_data)
    await session.flush()

    # 7. Shows (7 days for each screen across movies and events)
    base_date = datetime.utcnow().date()
    shows_to_add = []
    
    show_times = [
        (time(10, 0), time(12, 45)),
        (time(13, 30), time(16, 15)),
        (time(18, 0), time(20, 45)),   # Prime time
        (time(21, 15), time(23, 45)),  # Prime time
    ]

    for day_offset in range(7):
        current_date = base_date + timedelta(days=day_offset)
        
        for screen_idx, screen in enumerate(screens_list):
            content_choice = contents_data[(screen_idx + day_offset) % len(contents_data)]
            base_p = 250.0 if content_choice.type == ContentType.EVENT else 180.0

            for st_start, st_end in show_times:
                s_start = datetime.combine(current_date, st_start)
                s_end = datetime.combine(current_date, st_end)

                shows_to_add.append(
                    Show(
                        screen_id=screen.id,
                        content_id=content_choice.id,
                        start_time=s_start,
                        end_time=s_end,
                        base_price=base_p,
                        is_active=True,
                    )
                )

    session.add_all(shows_to_add)
    await session.commit()
    logger.info(f"Database seeded successfully with {len(screens_list)} screens, {len(contents_data)} contents, and {len(shows_to_add)} shows.")

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await seed_database(session)

if __name__ == "__main__":
    asyncio.run(main())
