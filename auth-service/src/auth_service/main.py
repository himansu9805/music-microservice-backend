"""This is the main module of the auth service."""

import uvicorn
from auth_service import const
from auth_service.routes.users import user_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

api = FastAPI(
    title="Auth Service API",
    description="This is the API for the Auth Service.",
    version=const.API_VERSION,
)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(user_router, prefix=f"/api/{const.API_VERSION}")


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
