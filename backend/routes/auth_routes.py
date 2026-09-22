# ============================================================
# EduMind AI - Authentication Routes
# ============================================================

from datetime import datetime, timedelta
import json
import os

import jwt
from dotenv import load_dotenv

from fastapi import APIRouter, HTTPException, Depends

from pydantic import BaseModel, EmailStr, Field

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

from database import get_connection
from auth_utils import get_current_user_id


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# ============================================================
# PASSWORD HASHING
# ============================================================

password_hash = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher()
    )
)


# ============================================================
# JWT CONFIGURATION
# ============================================================

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "edumind-secret-key"
)

JWT_ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ============================================================
# ALLOWED JOB ROLES
# ============================================================

ALLOWED_JOB_ROLES = [
    "Data Analyst",
    "Data Scientist",
    "IT / Technical Officer",
    "Manager / Team Lead",
    "Statistical Officer",
]


# ============================================================
# REQUEST MODELS
# ============================================================

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    designation: str = ""
    department: str = ""
    job_role: str = ""
    current_assignment: str = ""
    education: str = ""
    experience: str = ""

    previous_training: list[str] = Field(
        default_factory=list
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProfileUpdateRequest(BaseModel):
    designation: str = ""
    department: str = ""
    job_role: str = ""
    current_assignment: str = ""
    education: str = ""
    experience: str = ""
    previous_training: str = "[]"


# ============================================================
# CREATE JWT TOKEN
# ============================================================

def create_access_token(
    user_id: int,
    email: str,
    role: str = "learner"
):
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return token


# ============================================================
# REGISTER
# ============================================================

@router.post("/register")
async def register_user(
    data: RegisterRequest
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # ----------------------------------------------------
        # Clean input
        # ----------------------------------------------------

        name = data.name.strip()
        email = str(data.email).strip().lower()

        designation = data.designation.strip()
        department = data.department.strip()
        job_role = data.job_role.strip()
        current_assignment = data.current_assignment.strip()
        education = data.education.strip()
        experience = data.experience.strip()

        # ----------------------------------------------------
        # Validate required fields
        # ----------------------------------------------------

        if not name:
            raise HTTPException(
                status_code=400,
                detail="Name is required."
            )

        if not email:
            raise HTTPException(
                status_code=400,
                detail="Email is required."
            )

        if not data.password:
            raise HTTPException(
                status_code=400,
                detail="Password is required."
            )

        if len(data.password) < 6:
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 6 characters."
            )

        # ----------------------------------------------------
        # Validate job role
        # ----------------------------------------------------

        if job_role and job_role not in ALLOWED_JOB_ROLES:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid job role. Choose one of: "
                    + ", ".join(ALLOWED_JOB_ROLES)
                )
            )

        # ----------------------------------------------------
        # Check existing email
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE LOWER(email) = ?
            """,
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered."
            )

        # ----------------------------------------------------
        # Hash password
        # ----------------------------------------------------

        hashed_password = password_hash.hash(
            data.password
        )

        # ----------------------------------------------------
        # Convert previous training list to JSON
        #
        # Example:
        # ["Python", "SQL"]
        #
        # becomes:
        # '["Python", "SQL"]'
        # ----------------------------------------------------

        previous_training = data.previous_training or []

        previous_training_json = json.dumps(
            previous_training
        )

        # ----------------------------------------------------
        # Register user as LEARNER
        #
        # IMPORTANT:
        # Role is NOT accepted from frontend.
        # Every newly registered user is learner.
        # ----------------------------------------------------

        cursor.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password_hash,
                designation,
                department,
                job_role,
                current_assignment,
                education,
                experience,
                previous_training,
                role
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                email,
                hashed_password,
                designation,
                department,
                job_role,
                current_assignment,
                education,
                experience,
                previous_training_json,
                "learner"
            )
        )

        # ----------------------------------------------------
        # Save database changes
        # ----------------------------------------------------

        connection.commit()

        user_id = cursor.lastrowid

        print()
        print("=" * 60)
        print("✅ USER REGISTERED SUCCESSFULLY")
        print("=" * 60)
        print("User ID :", user_id)
        print("Name    :", name)
        print("Email   :", email)
        print("Role    : learner")
        print("=" * 60)

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return {
            "success": True,
            "message": "Registration successful.",
            "user": {
                "id": user_id,
                "name": name,
                "email": email,
                "designation": designation,
                "department": department,
                "job_role": job_role,
                "current_assignment": current_assignment,
                "education": education,
                "experience": experience,
                "previous_training": previous_training,
                "role": "learner"
            }
        }

    except HTTPException:
        raise

    except Exception as error:

        connection.rollback()

        print()
        print("=" * 60)
        print("❌ REGISTRATION ERROR")
        print("=" * 60)
        print(type(error).__name__)
        print(str(error))
        print("=" * 60)

        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(error)}"
        )

    finally:
        connection.close()


# ============================================================
# LOGIN
# ============================================================

@router.post("/login")
async def login_user(
    data: LoginRequest
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        email = str(data.email).strip().lower()

        # ----------------------------------------------------
        # Find user
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                password_hash,
                designation,
                department,
                job_role,
                current_assignment,
                education,
                experience,
                previous_training,
                role
            FROM users
            WHERE LOWER(email) = ?
            """,
            (email,)
        )

        user = cursor.fetchone()

        # ----------------------------------------------------
        # User not found
        # ----------------------------------------------------

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password."
            )

        # ----------------------------------------------------
        # Verify password
        # ----------------------------------------------------

        try:
            password_valid = password_hash.verify(
                data.password,
                user["password_hash"]
            )
        except Exception:
            password_valid = False

        if not password_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password."
            )

        # ----------------------------------------------------
        # Get role
        # ----------------------------------------------------

        role = str(
            user["role"] or "learner"
        ).strip().lower()

        # ----------------------------------------------------
        # Create JWT
        # ----------------------------------------------------

        access_token = create_access_token(
            user_id=int(user["id"]),
            email=user["email"],
            role=role
        )

        # ----------------------------------------------------
        # Previous training
        # ----------------------------------------------------

        previous_training = user["previous_training"] or "[]"

        try:
            previous_training_list = json.loads(
                previous_training
            )

            if not isinstance(
                previous_training_list,
                list
            ):
                previous_training_list = []

        except Exception:
            previous_training_list = []

        # ----------------------------------------------------
        # USER RESPONSE
        # ----------------------------------------------------

        user_data = {
            "id": int(user["id"]),
            "name": user["name"],
            "email": user["email"],
            "designation": user["designation"] or "",
            "department": user["department"] or "",
            "job_role": user["job_role"] or "",
            "current_assignment": user["current_assignment"] or "",
            "education": user["education"] or "",
            "experience": user["experience"] or "",
            "previous_training": previous_training_list,
            "role": role,
        }

        return {
            "success": True,
            "message": "Login successful.",
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_data
        }

    except HTTPException:
        raise

    except Exception as error:

        print()
        print("=" * 60)
        print("❌ LOGIN ERROR")
        print("=" * 60)
        print(type(error).__name__)
        print(str(error))
        print("=" * 60)

        raise HTTPException(
            status_code=500,
            detail="Login failed."
        )

    finally:
        connection.close()


# ============================================================
# GET CURRENT USER
# ============================================================

@router.get("/me")
async def get_current_user(
    user_id: int = Depends(get_current_user_id)
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # ----------------------------------------------------
        # Get current user
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                designation,
                department,
                job_role,
                current_assignment,
                education,
                experience,
                previous_training,
                role
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        # ----------------------------------------------------
        # Role
        # ----------------------------------------------------

        role = str(
            user["role"] or "learner"
        ).strip().lower()

        # ----------------------------------------------------
        # Previous training
        # ----------------------------------------------------

        previous_training = user["previous_training"] or "[]"

        try:
            previous_training_list = json.loads(
                previous_training
            )

            if not isinstance(
                previous_training_list,
                list
            ):
                previous_training_list = []

        except Exception:
            previous_training_list = []

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return {
            "success": True,
            "user": {
                "id": int(user["id"]),
                "name": user["name"],
                "email": user["email"],
                "designation": user["designation"] or "",
                "department": user["department"] or "",
                "job_role": user["job_role"] or "",
                "current_assignment": user["current_assignment"] or "",
                "education": user["education"] or "",
                "experience": user["experience"] or "",
                "previous_training": previous_training_list,
                "role": role,
            }
        }

    except HTTPException:
        raise

    except Exception as error:

        print()
        print("=" * 60)
        print("❌ GET CURRENT USER ERROR")
        print("=" * 60)
        print(type(error).__name__)
        print(str(error))
        print("=" * 60)

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve user."
        )

    finally:
        connection.close()


# ============================================================
# UPDATE CURRENT USER PROFILE
# ============================================================

@router.put("/profile")
async def update_profile(
    data: ProfileUpdateRequest,
    user_id: int = Depends(get_current_user_id)
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # ----------------------------------------------------
        # Validate job role
        # ----------------------------------------------------

        job_role = data.job_role.strip()

        if job_role and job_role not in ALLOWED_JOB_ROLES:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid job role. Choose one of: "
                    + ", ".join(ALLOWED_JOB_ROLES)
                )
            )

        # ----------------------------------------------------
        # Prepare previous training
        #
        # ProfileUpdateRequest currently receives this as
        # a JSON string from the frontend.
        # ----------------------------------------------------

        previous_training = (
            data.previous_training or "[]"
        ).strip()

        try:
            parsed_training = json.loads(
                previous_training
            )

            if not isinstance(
                parsed_training,
                list
            ):
                parsed_training = []

        except Exception:

            # If frontend sends a normal comma-separated
            # string, convert it into a list.

            parsed_training = [
                item.strip()
                for item in previous_training.split(",")
                if item.strip()
            ]

        previous_training_json = json.dumps(
            parsed_training
        )

        # ----------------------------------------------------
        # Update profile
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE users
            SET
                designation = ?,
                department = ?,
                job_role = ?,
                current_assignment = ?,
                education = ?,
                experience = ?,
                previous_training = ?
            WHERE id = ?
            """,
            (
                data.designation.strip(),
                data.department.strip(),
                job_role,
                data.current_assignment.strip(),
                data.education.strip(),
                data.experience.strip(),
                previous_training_json,
                user_id,
            )
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        connection.commit()

        # ----------------------------------------------------
        # Get updated user
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT
                id,
                name,
                email,
                designation,
                department,
                job_role,
                current_assignment,
                education,
                experience,
                previous_training,
                role
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        # ----------------------------------------------------
        # Parse previous training
        # ----------------------------------------------------

        saved_training = user["previous_training"] or "[]"

        try:
            saved_training = json.loads(
                saved_training
            )

            if not isinstance(
                saved_training,
                list
            ):
                saved_training = []

        except Exception:
            saved_training = []

        # ----------------------------------------------------
        # Return updated user
        # ----------------------------------------------------

        return {
            "success": True,
            "message": "Profile updated successfully.",
            "user": {
                "id": int(user["id"]),
                "name": user["name"],
                "email": user["email"],
                "designation": user["designation"] or "",
                "department": user["department"] or "",
                "job_role": user["job_role"] or "",
                "current_assignment": (
                    user["current_assignment"] or ""
                ),
                "education": user["education"] or "",
                "experience": user["experience"] or "",
                "previous_training": saved_training,
                "role": (
                    str(
                        user["role"] or "learner"
                    ).strip().lower()
                ),
            }
        }

    except HTTPException:
        raise

    except Exception as error:

        connection.rollback()

        print()
        print("=" * 60)
        print("❌ PROFILE UPDATE ERROR")
        print("=" * 60)
        print(type(error).__name__)
        print(str(error))
        print("=" * 60)

        raise HTTPException(
            status_code=500,
            detail="Failed to update profile."
        )

    finally:
        connection.close()