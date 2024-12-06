from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import notifications_router


app = FastAPI(redirect_slashes=False)
app.include_router(notifications_router)

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)