from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.post import PostCreate, PostRead
from app.crud.post import create_post, get_post, get_posts
from app.api.deps import CurrentUser

router = APIRouter()


@router.post("/", response_model=PostRead)
async def create_new_post(
    post_in: PostCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: CurrentUser,
):
    post = await create_post(
        db, title=post_in.title, content=post_in.content, author_id=current_user.id
    )
    return post


@router.get("/", response_model=list[PostRead])
async def read_all_posts(db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_posts(db)


@router.get("/{post_id}", response_model=PostRead)
async def read_single_post(post_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return post
