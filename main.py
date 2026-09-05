import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import create_client, Client


# =========================================================
# SUPABASE CONFIGURATION
# =========================================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Auth Login & Protect API",
    description="Secure API using Supabase Authentication and JWT",
    version="1.0.0"
)


# Swagger Bearer Authentication
security = HTTPBearer()


# =========================================================
# DATA MODEL
# =========================================================

class AuthData(BaseModel):
    email: str
    password: str


# =========================================================
# STAGE 0 - HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "Server running and connected to Supabase"
    }


# =========================================================
# STAGE 1 - SIGNUP
# =========================================================

@app.post("/auth/signup", status_code=201)
def signup(data: AuthData):

    if not data.email or not data.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })

        return {
            "message": "User created successfully",
            "user": response.user
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================================================
# STAGE 1 - LOGIN
# =========================================================

@app.post("/auth/login")
def login(data: AuthData):

    if not data.email or not data.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })

        if not response.session:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        return {
            "message": "Login successful",
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


# =========================================================
# STAGE 2 - PUBLIC ROUTE
# =========================================================

@app.get("/public/info")
def public_info():
    return {
        "message": "This is a public route",
        "access": "No authentication required"
    }


# =========================================================
# STAGE 3 - VERIFY JWT TOKEN
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication token is required"
        )

    try:
        response = supabase.auth.get_user(token)

        if not response or not response.user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        return response.user

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# =========================================================
# STAGE 3 - PROTECTED PROFILE
# =========================================================

@app.get("/protected/profile")
def protected_profile(
    user=Depends(get_current_user)
):

    return {
        "message": "Protected profile",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "created_at": str(user.created_at)
        }
    }


# =========================================================
# STAGE 4 - PROTECTED DASHBOARD
# =========================================================

@app.get("/protected/dashboard")
def protected_dashboard(
    user=Depends(get_current_user)
):

    return {
        "message": "Welcome to the protected dashboard",
        "user_id": user.id,
        "email": user.email
    }


# =========================================================
# STAGE 4 - LOGOUT
# =========================================================

@app.post("/auth/logout", status_code=204)
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication token is required"
        )

    try:
        supabase.auth.set_session(
            token,
            ""
        )

        supabase.auth.sign_out()

        return None

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )