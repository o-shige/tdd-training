from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from app.domain.registration_service import RegistrationService
from app.infrastructure.user_repository import SqlAlchemyUserRepository
from app.infrastructure.database import SessionLocal

app = FastAPI(
    title="Auth TDD Learning",
    description="JWT認証をTDDで学ぶプロジェクト",
    version="0.1.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserRegistrationRequest(BaseModel):
    email: EmailStr
    password: str


class UserRegistrationResponse(BaseModel):
    id: str
    email: str


@app.get("/")
def root():
    return {"message": "Auth API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/api/register", status_code=201, response_model=UserRegistrationResponse)
def register_user(request: UserRegistrationRequest):
    # パスワードの長さをチェック
    if len(request.password) < 8:
        raise HTTPException(status_code=400, detail={"error": "Password must be at least 8 characters long"})

    try:
        # データベースセッション作成
        db = SessionLocal()
        try:
            repository = SqlAlchemyUserRepository(db)
            service = RegistrationService(repository)

            # ユーザー登録
            user = service.register(request.email, request.password)

            return UserRegistrationResponse(
                id=str(user.id),
                email=user.email
            )
        finally:
            db.close()

    except ValueError as e:
        # 重複メールアドレスエラー
        raise HTTPException(status_code=409, detail={"error": str(e)})
    except Exception as e:
        # その他のエラー
        raise HTTPException(status_code=400, detail={"error": str(e)})
