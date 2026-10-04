import logging
from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import City, Theater, Screen, Seat, Movie, Show, User

logger = logging.getLogger("ticketlocal.seed")

async def seed_database(db: AsyncSession):
    """
    Seeds initial catalog hierarchy and seat layout if database is empty.
    """
    # Check if data already exists
    count_res = await db.execute(select(func.count(City.id)))
    if (count_res.scalar() or 0) > 0:
        logger.info("Database already contains catalog data, skipping seed.")
        return

    logger.info("Seeding initial database catalog and seat maps...")

    # 1. Cities
    cities_data = [
        {"name": "Hyderabad", "state": "Telangana", "slug": "hyderabad"},
        {"name": "Bengaluru", "state": "Karnataka", "slug": "bengaluru"},
        {"name": "Mumbai", "state": "Maharashtra", "slug": "mumbai"},
        {"name": "Delhi-NCR", "state": "Delhi", "slug": "delhi-ncr"},
        {"name": "Chennai", "state": "Tamil Nadu", "slug": "chennai"},
    ]
    city_objs = {}
    for c in cities_data:
        obj = City(**c)
        db.add(obj)
        city_objs[c["name"]] = obj
    await db.flush()

    # 2. Theaters
    theaters_data = [
        # Hyderabad
        {"city": "Hyderabad", "name": "Prasads Multiplex: Large Screen", "address": "NTR Gardens, Khairatabad, Hyderabad", "amenities": "IMAX Laser, Dolby Atmos, Massive Parking, Food Court"},
        {"city": "Hyderabad", "name": "AMB Cinemas: Gachibowli", "address": "Sarath City Capital Mall, Gachibowli, Hyderabad", "amenities": "Dolby Atmos, VIP Lounge, M-Ticket, Recliner VIP"},
        {"city": "Hyderabad", "name": "PVR Inox: Forum Sujana Mall", "address": "Kukatpally, Hyderabad", "amenities": "4DX, Dolby 7.1, Gourmet Food, Wheelchair Access"},
        # Bengaluru
        {"city": "Bengaluru", "name": "PVR: Forum Mall Koramangala", "address": "Hosur Road, Koramangala, Bengaluru", "amenities": "IMAX with Laser, Dolby Atmos, Gold Class"},
        {"city": "Bengaluru", "name": "Cinepolis: Orion Mall", "address": "Dr Rajkumar Road, Rajajinagar, Bengaluru", "amenities": "4DX, VIP Lounge, Dolby Atmos, M-Ticket"},
        # Mumbai
        {"city": "Mumbai", "name": "PVR ICON: Phoenix Palladium", "address": "Lower Parel, Mumbai", "amenities": "IMAX Laser, Luxe Dining, Recliner Service"},
        {"city": "Mumbai", "name": "PVR: Inorbit Mall Malad", "address": "Link Road, Malad West, Mumbai", "amenities": "4DX, Dolby Atmos, Food Court"},
    ]
    theater_objs = []
    for t in theaters_data:
        city_obj = city_objs[t["city"]]
        t_obj = Theater(
            city_id=city_obj.id,
            name=t["name"],
            address=t["address"],
            amenities=t["amenities"]
        )
        db.add(t_obj)
        theater_objs.append(t_obj)
    await db.flush()

    # 3. Screens and Seats for each Theater
    screen_objs = []
    seat_objs = []
    for theater in theater_objs:
        # Screen 1: IMAX 3D
        s1 = Screen(theater_id=theater.id, name="Screen 1 (IMAX with Laser)", format="IMAX 3D", total_seats=60)
        # Screen 2: Dolby Atmos
        s2 = Screen(theater_id=theater.id, name="Screen 2 (Dolby Atmos 4K)", format="Dolby Atmos", total_seats=60)
        db.add_all([s1, s2])
        screen_objs.extend([s1, s2])
    await db.flush()

    # Generate 2D Matrix of seats for each screen: Rows A to F, 10 seats per row
    # Row A, B: RECLINER (Base ₹450)
    # Row C, D: PRIME (Base ₹280)
    # Row E, F: CLASSIC (Base ₹180)
    for screen in screen_objs:
        for row in ["A", "B", "C", "D", "E", "F"]:
            if row in ["A", "B"]:
                stype = "RECLINER"
                price = 450.0
            elif row in ["C", "D"]:
                stype = "PRIME"
                price = 280.0
            else:
                stype = "CLASSIC"
                price = 180.0
            
            for num in range(1, 11):
                seat = Seat(
                    screen_id=screen.id,
                    row=row,
                    number=num,
                    seat_type=stype,
                    base_price=price
                )
                db.add(seat)
    await db.flush()

    # 4. Movies
    movies_data = [
        {
            "title": "Kalki 2898 AD",
            "slug": "kalki-2898-ad",
            "synopsis": "A modern avatar of Vishnu, a Hindu god, is believed to have descended to the earth to protect the world from evil forces in a dystopian post-apocalyptic future.",
            "poster_url": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=1200&auto=format&fit=crop&q=80",
            "duration_min": 181,
            "rating": 8.9,
            "certificate": "UA",
            "genres": "Action, Sci-Fi, Mythological",
            "languages": "Telugu, Hindi, English, Tamil",
            "release_date": "2026-06-27",
            "is_featured": True
        },
        {
            "title": "Dune: Part Two",
            "slug": "dune-part-two",
            "synopsis": "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.",
            "poster_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&auto=format&fit=crop&q=80",
            "duration_min": 166,
            "rating": 9.1,
            "certificate": "UA",
            "genres": "Sci-Fi, Adventure, Drama",
            "languages": "English, Hindi",
            "release_date": "2026-03-01",
            "is_featured": True
        },
        {
            "title": "Interstellar: 10th Anniversary IMAX Edition",
            "slug": "interstellar-imax",
            "synopsis": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft along with a team of researchers to find a new planet.",
            "poster_url": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1200&auto=format&fit=crop&q=80",
            "duration_min": 169,
            "rating": 9.4,
            "certificate": "UA",
            "genres": "Sci-Fi, Adventure, Drama",
            "languages": "English",
            "release_date": "2026-09-10",
            "is_featured": True
        },
        {
            "title": "Stree 2: Sarkate Ka Aatank",
            "slug": "stree-2",
            "synopsis": "After the events of Stree, the town of Chanderi is being haunted again. This time by a headless entity known as Sarkata.",
            "poster_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=1200&auto=format&fit=crop&q=80",
            "duration_min": 147,
            "rating": 8.4,
            "certificate": "UA",
            "genres": "Comedy, Horror",
            "languages": "Hindi",
            "release_date": "2026-08-15",
            "is_featured": False
        },
        {
            "title": "Devara: Part 1",
            "slug": "devara-part-1",
            "synopsis": "An epic action saga set across coastal lands where power, honor, and fear collide as a fearless warrior takes a stand.",
            "poster_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=600&auto=format&fit=crop&q=80",
            "backdrop_url": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1200&auto=format&fit=crop&q=80",
            "duration_min": 178,
            "rating": 8.7,
            "certificate": "A",
            "genres": "Action, Drama, Thriller",
            "languages": "Telugu, Hindi, Tamil",
            "release_date": "2026-09-27",
            "is_featured": False
        }
    ]
    movie_objs = []
    for m in movies_data:
        m_obj = Movie(**m)
        db.add(m_obj)
        movie_objs.append(m_obj)
    await db.flush()

    # 5. Shows across today and the next 4 days
    today = datetime.now()
    dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(5)]
    
    showtimes = [
        ("10:00", "13:00", 1.0),
        ("13:45", "16:45", 1.0),
        ("17:30", "20:30", 1.2),  # Evening Prime surge
        ("21:15", "00:15", 1.25), # Night Prime surge
    ]

    for screen in screen_objs:
        for show_date in dates:
            for idx, (stime, etime, surge) in enumerate(showtimes):
                movie = movie_objs[(screen.id + idx) % len(movie_objs)]
                show = Show(
                    screen_id=screen.id,
                    movie_id=movie.id,
                    show_date=show_date,
                    start_time=stime,
                    end_time=etime,
                    language=movie.languages.split(",")[0].strip(),
                    format=screen.format,
                    surge_multiplier=surge
                )
                db.add(show)
    await db.flush()

    # 6. Default Admin & Demo Users
    demo_user = User(
        email="alex@ticketlocal.io",
        hashed_password="demo_password_hash",
        full_name="Alex Mercer",
        phone="+91 98765 43210",
        role="customer"
    )
    admin_user = User(
        email="admin@nexora.io",
        hashed_password="admin_password_hash",
        full_name="NEXORA Operator",
        phone="+91 90000 00000",
        role="admin"
    )
    db.add_all([demo_user, admin_user])
    await db.commit()
    logger.info("Database seeding completed successfully.")
