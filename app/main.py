from fastapi import FastAPI
from app.api import auth, post

app = FastAPI(title="Blog API")


@app.get("/health")
def test():
    return {"message": "Blog Platform API"}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(post.router, prefix="/post", tags=["post"])
