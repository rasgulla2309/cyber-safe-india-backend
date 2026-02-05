from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import (
    number_checker,
    chat,
    admin,
    auth,
    auth_user,
    profile,
    ws_chat,
    news,
    phishing
)

# =========================
# FASTAPI APP
# =========================
app = FastAPI(title="Cyber Safe India")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DATABASE
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# ROUTERS
# =========================
app.include_router(number_checker.router)
app.include_router(chat.router)
app.include_router(admin.router)
app.include_router(auth.router)        # admin / community login
app.include_router(auth_user.router)   # user OTP login
app.include_router(profile.router)     # profile system
app.include_router(news.router)
app.include_router(ws_chat.router)
app.include_router(phishing.router)

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"message": "Backend running successfully"}
