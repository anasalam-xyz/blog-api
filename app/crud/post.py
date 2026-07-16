from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post


async def create_post(
    db: AsyncSession, title: str, content: str, author_id: int
) -> Post:
    post = Post(title=title, content=content, author_id=author_id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


async def get_post(db: AsyncSession, post_id: int) -> Post | None:
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()


async def get_posts(db: AsyncSession) -> list[Post] | None:
    result = await db.execute(select(Post))
    return list(result.scalars().all())


async def update_post(db: AsyncSession, post: Post, title: str, content: str) -> Post:
    post.title = title
    post.content = content
    await db.commit()
    await db.refresh(post)
    return post


async def delete_post(db: AsyncSession, post: Post) -> None:
    await db.delete(post)
    await db.commit()
