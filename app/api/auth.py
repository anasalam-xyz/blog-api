from fastapi import Depends, status, HTTPException, APIRouter
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.crud.user import get_user_by_email, create_user
from app.core.security import create_access_token, verify_hash, hash_password

router = APIRouter()


@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    existing_user = await get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Email already registered"
        )

    hashed = hash_password(user_in.password)
    user = create_user(db, user_in.email, hashed)

    return user


@router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_hash(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
