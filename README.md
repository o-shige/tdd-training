# tdd-training

パターン2をTDD × Docker × UI確認で進める4週間プランを立てますね。

## 技術スタック（完全無料構成）

```
バックエンド: Python 3.11 + FastAPI
フロントエンド: Next.js 14 + TypeScript
DB: PostgreSQL 15 (Docker)
Cache: Redis 7 (Docker)
テスト: pytest + testcontainers
認証UI: Headless UI (無料)
開発環境: Docker Compose
```

---

## Week 1: 基盤構築 + 純粋関数のTDD

**ゴール**: パスワードハッシュ化とJWT生成・検証が動く状態

### Day 1-2: 環境セットアップ
```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: auth_db
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpass
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    depends_on:
      - postgres
      - redis
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
```

**タスク**:
- リポジトリ初期化（`auth-tdd-learning/`）
- Docker Compose起動確認
- FastAPIとNext.jsのスケルトン作成
- pytest環境構築

### Day 3-5: TDDサイクル1（純粋関数）

**Red → Green → Refactor**

```python
# backend/tests/test_password.py
import pytest
from auth.security import hash_password, verify_password

def test_hash_password_returns_different_hash_each_time():
    """同じパスワードでも毎回異なるハッシュを生成"""
    password = "mypassword123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    assert hash1 != hash2

def test_verify_password_succeeds_with_correct_password():
    """正しいパスワードで検証成功"""
    password = "mypassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) == True

def test_verify_password_fails_with_wrong_password():
    """間違ったパスワードで検証失敗"""
    password = "mypassword123"
    hashed = hash_password(password)
    assert verify_password("wrongpassword", hashed) == False
```

```python
# backend/tests/test_jwt.py
import pytest
from auth.jwt import create_access_token, verify_token
from datetime import timedelta

def test_create_and_verify_token():
    """トークン生成と検証の基本フロー"""
    payload = {"user_id": "123", "email": "test@example.com"}
    token = create_access_token(payload, expires_delta=timedelta(hours=1))
    
    decoded = verify_token(token)
    assert decoded["user_id"] == "123"
    assert decoded["email"] == "test@example.com"

def test_verify_expired_token_raises_error():
    """期限切れトークンはエラー"""
    payload = {"user_id": "123"}
    token = create_access_token(payload, expires_delta=timedelta(seconds=-1))
    
    with pytest.raises(TokenExpiredError):
        verify_token(token)
```

**実装**:
- `backend/auth/security.py` (bcrypt使用)
- `backend/auth/jwt.py` (PyJWT使用)

**UI確認**: まだなし（Week 2から）

---

## Week 2: ユーザー登録のTDD + UI実装

**ゴール**: ユーザー登録フォームからDBに保存できる状態

### Day 1-2: ドメイン層のTDD

```python
# backend/tests/test_user_registration.py
import pytest
from auth.domain.user import User, UserRepository
from auth.services.registration import RegistrationService
from unittest.mock import Mock

def test_register_new_user_successfully():
    """新規ユーザー登録成功"""
    # Arrange
    user_repo = Mock(spec=UserRepository)
    user_repo.find_by_email.return_value = None  # メール重複なし
    service = RegistrationService(user_repo)
    
    # Act
    user = service.register(
        email="test@example.com",
        password="password123"
    )
    
    # Assert
    assert user.email == "test@example.com"
    assert user.password_hash != "password123"  # ハッシュ化されてる
    user_repo.save.assert_called_once()

def test_register_with_duplicate_email_raises_error():
    """重複メールでエラー"""
    user_repo = Mock(spec=UserRepository)
    user_repo.find_by_email.return_value = User(email="test@example.com")
    service = RegistrationService(user_repo)
    
    with pytest.raises(DuplicateEmailError):
        service.register("test@example.com", "password123")
```

**実装**:
- `backend/auth/domain/user.py` (Userエンティティ)
- `backend/auth/domain/repository.py` (リポジトリインターフェース)
- `backend/auth/services/registration.py` (登録サービス)

### Day 3-4: インフラ層 + API実装

```python
# backend/tests/integration/test_user_repository.py
import pytest
from sqlalchemy import create_engine
from auth.infrastructure.user_repository import SQLAlchemyUserRepository

@pytest.fixture
def test_db():
    """テスト用DB"""
    engine = create_engine("postgresql://dev:devpass@localhost:5432/auth_test")
    # マイグレーション実行
    yield engine
    # クリーンアップ

def test_save_and_find_user(test_db):
    """ユーザー保存と取得"""
    repo = SQLAlchemyUserRepository(test_db)
    
    user = User(email="test@example.com", password_hash="hashed")
    repo.save(user)
    
    found = repo.find_by_email("test@example.com")
    assert found.email == "test@example.com"
```

```python
# backend/tests/api/test_registration_endpoint.py
from fastapi.testclient import TestClient

def test_register_endpoint(test_client, test_db):
    """登録APIエンドポイント"""
    response = test_client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert "id" in response.json()
```

### Day 5: フロントエンド実装

```typescript
// frontend/app/register/page.tsx
export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    const res = await fetch('http://localhost:8000/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    
    if (res.ok) {
      alert('登録成功！')
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button type="submit">登録</button>
    </form>
  )
}
```

**UI確認**: `http://localhost:3000/register` で登録フォーム動作確認

---

## Week 3: ログイン + セッション管理のTDD

**ゴール**: ログインしてトークン取得、保護されたページにアクセスできる

### Day 1-2: ログインサービスのTDD

```python
# backend/tests/test_login.py
def test_login_with_correct_credentials():
    """正しい認証情報でログイン成功"""
    user_repo = Mock()
    user_repo.find_by_email.return_value = User(
        email="test@example.com",
        password_hash=hash_password("password123")
    )
    service = LoginService(user_repo)
    
    tokens = service.login("test@example.com", "password123")
    
    assert "access_token" in tokens
    assert "refresh_token" in tokens

def test_login_with_wrong_password_raises_error():
    """間違ったパスワードでエラー"""
    user_repo = Mock()
    user_repo.find_by_email.return_value = User(
        email="test@example.com",
        password_hash=hash_password("password123")
    )
    service = LoginService(user_repo)
    
    with pytest.raises(InvalidCredentialsError):
        service.login("test@example.com", "wrongpassword")
```

### Day 3-4: セッション管理（Redis）

```python
# backend/tests/test_session.py
def test_store_and_retrieve_session(redis_client):
    """セッション保存と取得"""
    session_store = RedisSessionStore(redis_client)
    
    session_store.save("user123", {"email": "test@example.com"})
    session = session_store.get("user123")
    
    assert session["email"] == "test@example.com"

def test_session_expires_after_ttl(redis_client):
    """TTL後にセッション期限切れ"""
    session_store = RedisSessionStore(redis_client, ttl=1)
    session_store.save("user123", {"email": "test@example.com"})
    
    time.sleep(2)
    
    assert session_store.get("user123") is None
```

### Day 5: ログインUI + 保護ルート

```typescript
// frontend/app/login/page.tsx
export default function LoginPage() {
  const handleLogin = async (email: string, password: string) => {
    const res = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    
    const { access_token } = await res.json()
    localStorage.setItem('token', access_token)
    router.push('/dashboard')
  }
  
  return <LoginForm onSubmit={handleLogin} />
}
```

```typescript
// frontend/app/dashboard/page.tsx
export default function Dashboard() {
  useEffect(() => {
    const token = localStorage.getItem('token')
    fetch('http://localhost:8000/users/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
  }, [])
  
  return <div>保護されたダッシュボード</div>
}
```

**UI確認**: ログイン → ダッシュボードへリダイレクト

---

## Week 4: トークンリフレッシュ + Googleログイン

**ゴール**: リフレッシュトークン + ソーシャルログイン1つ追加

### Day 1-2: リフレッシュトークンのTDD

```python
def test_refresh_access_token_with_valid_refresh_token():
    """有効なリフレッシュトークンで新しいアクセストークン取得"""
    service = TokenService()
    refresh_token = service.create_refresh_token(user_id="123")
    
    new_access_token = service.refresh_access_token(refresh_token)
    
    decoded = verify_token(new_access_token)
    assert decoded["user_id"] == "123"
```

### Day 3-5: Googleログイン（無料で実装）

Google OAuth 2.0を使用（無料）

```python
# backend/tests/test_oauth.py
def test_google_oauth_callback_creates_or_updates_user():
    """Google認証コールバックでユーザー作成/更新"""
    google_service = GoogleOAuthService()
    user_repo = Mock()
    
    # Googleから返ってくる情報をシミュレート
    google_user_info = {
        "email": "test@gmail.com",
        "name": "Test User",
        "sub": "google-user-id-123"
    }
    
    user = google_service.authenticate(google_user_info, user_repo)
    
    assert user.email == "test@gmail.com"
    assert user.oauth_provider == "google"
```

**実装**:
- Google Cloud Consoleで無料のOAuthクライアント作成
- `authlib`ライブラリでOAuth実装
- フロントエンドに「Googleでログイン」ボタン追加

**UI確認**: Googleでログインボタン → 認証フロー → ダッシュボード

---

## プロジェクト構成

```
auth-tdd-learning/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── auth/
│   │   ├── domain/
│   │   │   ├── user.py
│   │   │   └── repository.py
│   │   ├── services/
│   │   │   ├── registration.py
│   │   │   ├── login.py
│   │   │   └── oauth.py
│   │   ├── infrastructure/
│   │   │   ├── user_repository.py
│   │   │   └── session_store.py
│   │   ├── api/
│   │   │   └── endpoints.py
│   │   ├── security.py
│   │   └── jwt.py
│   └── tests/
│       ├── test_password.py
│       ├── test_jwt.py
│       ├── test_user_registration.py
│       └── integration/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── app/
│       ├── register/
│       ├── login/
│       └── dashboard/
└── README.md
```

---

## 日次の進め方（TDDサイクル）

**毎日のルーチン**:
1. **Red**: 失敗するテストを書く（10分）
2. **Green**: 最小限の実装でテストを通す（20分）
3. **Refactor**: コードをきれいにする（10分）
4. **UI確認**: Docker起動してブラウザで動作確認（10分）
5. **Git commit**: 1サイクルごとにコミット（5分）

**1日3-4サイクル** × **週5日** = 15-20サイクル/週

---

しげさんのCCSSД手法と相性良いと思います。各週末にフラクタルレビューして次週の調整もできます。

まずWeek 1のDocker環境セットアップから始めますか？