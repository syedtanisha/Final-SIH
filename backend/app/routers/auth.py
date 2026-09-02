from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..schemas.user import UserCreate, UserLogin, UserOut, Token, UserUpdate
from ..core.security import get_current_user, hash_password, verify_password, create_access_token
from ..models.models import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    email_clean = user_in.email.lower().strip()
    existing = db.query(User).filter(User.email == email_clean).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user account with this email already exists."
        )

    hashed_pwd = hash_password(user_in.password)
    user_obj = User(
        email=email_clean,
        hashed_password=hashed_pwd,
        full_name=user_in.full_name,
        designation=user_in.designation or "Statistical Professional",
        department=user_in.department or "MoSPI",
        organization=user_in.organization or "Government of India"
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    # Automatically initialize baseline competencies if needed
    return user_obj

def _authenticate_user(username_raw: str, password_raw: str, db: Session) -> Token:
    username = username_raw.lower().strip()
    user = db.query(User).filter(User.email == username).first()
    if not user or not verify_password(password_raw, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email credentials or password."
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token, token_type="Bearer", user=UserOut.model_validate(user))

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return _authenticate_user(form_data.username, form_data.password, db)

@router.post("/login/json", response_model=Token)
def login_json(login_data: UserLogin, db: Session = Depends(get_db)):
    return _authenticate_user(login_data.username, login_data.password, db)

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserOut)
def update_profile(
    profile_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if profile_data.full_name is not None:
        current_user.full_name = profile_data.full_name
    if profile_data.designation is not None:
        current_user.designation = profile_data.designation
    if profile_data.department is not None:
        current_user.department = profile_data.department
    if profile_data.organization is not None:
        current_user.organization = profile_data.organization
    db.commit()
    db.refresh(current_user)
    return current_user
