# TDD JWT認証システム開発 - 会話履歴サマリー - 2025-11-26

## プロジェクト概要
TDDアプローチによるJWT認証システムの開発プロジェクト。Issue #10のSQLAlchemy UserRepository実装を中心とした開発セッション。

## 開発フロー

### 1. 初期段階 - Issue #10対応開始
- **目標**: SQLAlchemy UserRepositoryの実装
- **アプローチ**: Test-Driven Development (Red-Green-Refactor)
- **環境**: Docker Compose (PostgreSQL, Redis, FastAPI, Next.js)

### 2. TDD実装プロセス

#### Red Phase（テスト作成）
- `backend/tests/domain/test_user_repository.py` 作成
- 5つのテストケースを段階的に実装
- SQLite :memory: を使用したテスト環境構築

#### Green Phase（実装）
- `backend/app/infrastructure/database.py`: SQLAlchemy基盤とUserModel定義
- `backend/app/infrastructure/user_repository.py`: SqlAlchemyUserRepository実装
- ドメインモデル ↔ データベースモデル変換ロジック

#### 技術的な課題と解決
1. **SQLAlchemy UUID型エラー**
   - 問題: SQLiteがUUID型をサポートしない
   - 解決: String型を使用し、リポジトリ層でUUID変換

2. **Python 3.9互換性問題**
   - 問題: `User | None` 構文がPython 3.9で未対応
   - 解決: `Union[User, None]` 構文に変更
   - 影響ファイル: 複数のドメインファイル

### 3. Git Flow問題と解決

#### 問題: 直接mainブランチへのコミット
- ユーザーの意図: プルリクエストワークフローの使用
- 対応: feature branchの作成とPR作成プロセスの確立

#### リポジトリフォーク
- 元リポジトリ: `o-shige/tdd-training`
- フォーク先: `shkonno/tdd-training`
- 理由: Push権限の問題

### 4. CI/CD環境構築

#### GitHub Actions設定
- **初期問題**: フォーク環境でActionsが実行されない
- **修正内容**:
  - `feature/*` ブランチをトリガーに追加
  - `workflow_dispatch` による手動実行を有効化
  - デバッグ情報の追加

#### Python依存関係の修正
- **Hypothesis バージョンエラー**: 6.148.2 → 6.90.0
- **requirements.txt** の整合性確保

### 5. 最終段階 - Pipキャッシュ警告修正

#### 問題
```
Error: Cache folder path is retrieved for pip but doesn't exist on disk: /home/runner/.cache/pip
```

#### 解決策
- setup-python actionの内蔵キャッシュを無効化
- actions/cache@v4による手動キャッシュ設定
- pip install時のキャッシュ使用を有効化

## 実装された主要コンポーネント

### 1. データベース層
```python
# backend/app/infrastructure/database.py
class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
```

### 2. リポジトリ実装
```python
# backend/app/infrastructure/user_repository.py
class SqlAlchemyUserRepository(UserRepository):
    def save(self, user: User) -> User:
        user_model = UserModel(
            id=str(user.id),
            email=user.email,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
            is_active=user.is_active
        )
        self._session.add(user_model)
        self._session.commit()
        return self._to_domain_user(user_model)
```

### 3. テスト構成
```python
# backend/tests/domain/test_user_repository.py
@pytest.fixture
def repository(self):
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    repository = SqlAlchemyUserRepository(session)
    return repository
```

## アーキテクチャ決定

### データベース戦略
- **テスト環境**: SQLite :memory: (高速)
- **本番環境**: PostgreSQL (Docker Compose)
- **理由**: テスト実行速度と本番環境の堅牢性のバランス

### 型システム
- **Python 3.9互換性**: Union型の使用
- **型安全性**: 厳密な型ヒントの適用
- **ドメイン境界**: エンティティとモデルの明確な分離

### 依存性注入
- **データベースセッション**: リポジトリコンストラクタでの注入
- **テスト容易性**: モックやインメモリ実装の差し替え可能

## 技術スタック確認

### バックエンド
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PostgreSQL (psycopg2-binary 2.9.9)
- Redis 5.0.1
- JWT認証 (PyJWT 2.8.0)
- パスワードハッシュ (bcrypt 4.1.1, passlib 1.7.4)

### テスト
- pytest 7.4.3
- hypothesis 6.90.0 (プロパティベースドテスト)
- httpx 0.25.2 (HTTP テストクライアント)

### CI/CD
- GitHub Actions
- Python 3.9環境
- 自動テスト実行
- 依存関係キャッシュ

## 成果物

### 実装完了
- ✅ SQLAlchemy UserRepository (5つのテストすべて通過)
- ✅ データベースモデルとドメインモデルの変換
- ✅ Python 3.9互換性
- ✅ GitHub Actions CI環境
- ✅ プルリクエストワークフロー

### テストカバレッジ
- ユーザー保存機能
- ID/Email による検索機能
- 存在しないユーザーの処理
- データベース変換の整合性
- 重複メールアドレスの処理

## 学習ポイント

### TDD実践
- Red-Green-Refactor サイクルの確実な実行
- テストファーストによる設計の改善
- リファクタリングの安全性確保

### アーキテクチャ
- Repository パターンの実装
- ドメインロジックとインフラの分離
- 依存性逆転の原則の適用

### インフラ
- GitHub Actions でのフォーク環境対応
- Python バージョン互換性の管理
- Docker Compose による開発環境統一

## 次のステップ候補
1. Issue #11以降の機能実装
2. Redis セッション管理の実装
3. JWT トークン生成・検証機能
4. フロントエンド連携
5. エンドツーエンドテストの追加

## 参考情報
- プロジェクトリポジトリ: shkonno/tdd-training (フォーク)
- 開発ブランチ: feature/issue-10-sqlalchemy-repository
- TDD メンター: t_wada, Kent Beck, Tidy First 思想に基づく