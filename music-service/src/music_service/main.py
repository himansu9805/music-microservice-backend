"""This is the main module of the music service."""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from music_service import const
from music_service.routes.music import music_router

api = FastAPI(
    title="Music Service API",
    description="This is the API for the Music Service.",
    version=const.API_VERSION,
)

api.include_router(music_router, prefix=f"/api/{const.API_VERSION}")


@api.get("/", include_in_schema=False)
async def read_root():
    """This is the root endpoint."""
    return RedirectResponse(url="/docs")


@api.get("/health", include_in_schema=False)
async def health():
    """This is the health check endpoint."""
    return {"status": "ok"}


def main():
    """This is the main function of the auth service."""
    uvicorn.run(api, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
