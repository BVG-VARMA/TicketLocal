from datetime import datetime, date, time
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, and_, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import City, Theater, Screen, Show, Content, ContentType
from app.schemas import CityOut, ContentOut, ShowOut, TheaterShowsOut, ScreenSimpleOut, TheaterSimpleOut

router = APIRouter(tags=["Catalog & Shows"])

@router.get("/cities", response_model=List[CityOut])
async def get_cities(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(City).order_by(City.name))
    return res.scalars().all()

@router.get("/content", response_model=List[ContentOut])
async def get_content(
    type: Optional[ContentType] = Query(None, description="Filter by MOVIE or EVENT"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    language: Optional[str] = Query(None, description="Filter by language"),
    search: Optional[str] = Query(None, description="Search by title"),
    db: AsyncSession = Depends(get_db),
):
    query = select(Content)
    conditions = []
    if type:
        conditions.append(Content.type == type)
    if genre:
        conditions.append(Content.genre.ilike(f"%{genre}%"))
    if language:
        conditions.append(Content.language.ilike(f"%{language}%"))
    if search:
        conditions.append(Content.title.ilike(f"%{search}%"))

    if conditions:
        query = query.where(and_(*conditions))

    query = query.order_by(Content.rating.desc(), Content.id.desc())
    res = await db.execute(query)
    return res.scalars().all()

@router.get("/content/{content_id}", response_model=ContentOut)
async def get_content_by_id(content_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Content).where(Content.id == content_id))
    content = res.scalar_one_or_none()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.get("/shows", response_model=List[TheaterShowsOut])
async def get_shows(
    city: Optional[str] = Query(None, description="City name (e.g. Hyderabad, Bangalore, Mumbai)"),
    date_str: Optional[str] = Query(None, alias="date", description="Date in YYYY-MM-DD format"),
    content_id: Optional[int] = Query(None, description="Content ID"),
    type: Optional[ContentType] = Query(None, description="Content type MOVIE or EVENT"),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns active shows matching filters, grouped by Theater.
    """
    query = (
        select(Show)
        .join(Show.screen)
        .join(Screen.theater)
        .join(Theater.city)
        .join(Show.content)
        .where(Show.is_active == True)
        .options(
            joinedload(Show.screen).joinedload(Screen.theater).joinedload(Theater.city),
            joinedload(Show.content),
        )
    )

    conditions = []
    if city:
        conditions.append(City.name.ilike(city))
    if content_id:
        conditions.append(Show.content_id == content_id)
    if type:
        conditions.append(Content.type == type)
    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            start_dt = datetime.combine(target_date, time.min)
            end_dt = datetime.combine(target_date, time.max)
            conditions.append(Show.start_time.between(start_dt, end_dt))
        except ValueError:
            pass

    if conditions:
        query = query.where(and_(*conditions))

    query = query.order_by(Theater.name, Show.start_time)
    res = await db.execute(query)
    shows = res.unique().scalars().all()

    # Group by Theater
    theater_map = {}
    for s in shows:
        t = s.screen.theater
        if t.id not in theater_map:
            theater_map[t.id] = {
                "theater_id": t.id,
                "theater_name": t.name,
                "theater_address": t.address,
                "shows": [],
            }
        theater_map[t.id]["shows"].append(
            ShowOut(
                id=s.id,
                screen_id=s.screen_id,
                content_id=s.content_id,
                start_time=s.start_time,
                end_time=s.end_time,
                base_price=s.base_price,
                is_active=s.is_active,
                screen=ScreenSimpleOut(id=s.screen.id, name=s.screen.name, rows=s.screen.rows, cols=s.screen.cols),
                theater=TheaterSimpleOut(id=t.id, name=t.name, address=t.address, city_id=t.city_id),
                content=ContentOut.model_validate(s.content) if s.content else None,
            )
        )

    return list(theater_map.values())
