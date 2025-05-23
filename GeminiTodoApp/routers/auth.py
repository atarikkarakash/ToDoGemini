from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Annotated
from jose.constants import ALGORITHMS
from starlette import status
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy.orm import Session
from starlette.datastructures import Secret
from datetime import timedelta, datetime, timezone
from ..database import SessionLocal
from pydantic import BaseModel
from ..models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates

#Bu Jinja HTMLlerin içerisindeki söz dizimleri hep jinjadır.




router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

templates = Jinja2Templates(directory="app/templates")

SECRET_KEY = "3a2fck87fddnvr4i0y3xs9pbultzqdst6l0jivcm19w7l8l3nzlnho5syfs5119x"
ALGORITHM = "HS256"



def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

db_dependency = Annotated[Session, Depends(get_db)]


bcrypt_context = CryptContext(schemes = ["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Terim olarak parola ve şifre farkını bilmemiz gerekiyor. Kullanıcıların parolalarını açık metin olarak veritabanında tutmayız.
# Hem biz hem başkaları görmesin diye user = User(**create_user_request.dict()) bu şekilde yapıyor olsak. Kimse bilemeden parolaları görebiliriz.
# Bu yüzden farklı algoritmalarla şifreliyoruz. Biz veri tabanında parolayı değil şifreyi tutuyoruz. Yani kullanıcının parolasının şifrelenmiş halini tutuyoruz.
# Örnek olarak SHA256


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub' : username, 'id': user_id, 'role':role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        user_role = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or ID invalid")
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Token is invalid")




@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    user = User(
        username = create_user_request.username,
        email = create_user_request.email,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        is_active=True,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        phone_number=create_user_request.phone_number
    )
    db.add(user)
    db.commit()

# Token mantığı: Kullanıcıya verdiğimiz şifrelenmiş bir string değeri.
# Kullanıcının sadece kendi todosunu görmesi gibi. Authanticated isteklere çevireceğiz yani.


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
                                 db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Username or Password")
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=60))
    return {"access_token":token, "token_type": "bearer"}
















