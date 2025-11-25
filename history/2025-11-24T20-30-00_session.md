# TDDセッション記録: 2025-11-24

## セッション概要

- **日時**: 2025-11-24 20:00頃～
- **対象Issue**: Issue #9 RegistrationService
- **ブランチ**: feature/user-repository

---

## 実施内容

### 1. RegistrationService の TDD 実装

#### Red-Green-Refactor サイクル

| サイクル | テスト | 結果 |
|---------|--------|------|
| 1 | 有効なデータでユーザーを登録できる | ✅ |
| 2 | 登録したユーザーがリポジトリに保存される | ✅ |
| 3 | 登録時にパスワードがハッシュ化される | ✅ |
| 4 | 既存のメールアドレスで登録するとエラーになる | ✅ |

#### 実装した機能

- `RegistrationService` クラス
  - `register(email, password)` メソッド
  - 重複メールチェック
  - パスワードハッシュ化
  - リポジトリへの保存

---

### 2. プロパティベースドテストの追加と問題解決

#### 発生した問題

1. **bcryptが遅い問題**
   - hypothesisが100件のテストケースを生成
   - bcryptは意図的に遅いアルゴリズム
   - テスト実行に数分かかる

2. **テストデータの問題**
   - NULLバイト: bcryptが`\x00`を許可しない
   - IDN正規化: Punycodeがデコードされる（`XN--11B4C3D` → `कॉम`）
   - メール正規化: 大文字が小文字に変換される

#### 解決策: 依存性注入

**実装変更**:
```python
class RegistrationService:
    def __init__(self, repository, hasher: Callable[[str], str] = hash_password):
        self._repository = repository
        self._hasher = hasher
```

**テストでの使用**:
```python
def fast_hash(password: str) -> str:
    return f"hashed_{password}"

service = RegistrationService(repository, hasher=fast_hash)
```

**効果**:
- テスト実行時間: 数分 → 6秒
- 「テストしやすい設計 = 良い設計」（Kent Beck）

---

### 3. 学習ポイント

#### AAA パターン（Arrange-Act-Assert）

```python
def test_registered_user_is_saved_to_repository():
    # Arrange（準備）
    repository = InMemoryUserRepository()
    service = RegistrationService(repository)

    # Act（実行）
    service.register("test@example.com", "password123")

    # Assert（検証）
    saved_user = repository.find_by_email("test@example.com")
    assert saved_user is not None
```

- **リポジトリ層のトレンドではない** - テスト全般のベストプラクティス
- 複数オブジェクトが連携するテストで特に有効
- テストコードは「実行可能なドキュメント」

#### 依存性注入の利点

- テストが高速化
- コンポーネントの交換が容易
- 単一責任の原則に沿った設計

---

## 成果物

### コミット

```
661ff6e feat: Issue #9 RegistrationService実装 + 依存性注入によるテスト改善
```

### ファイル変更

| ファイル | 変更内容 |
|----------|----------|
| `backend/app/domain/registration_service.py` | 新規作成 |
| `backend/tests/domain/test_user_registration.py` | テスト追加（+109行） |

### テスト結果

- 全16テストがパス
- 実行時間: 5.90秒

---

## 次のステップ

- [ ] PRの作成（中断）
- [ ] Issue #10: SQLAlchemy UserRepository実装

---

## 参考

- t_wada式TDD: 「動作するきれいなコード」
- Kent Beck: テストファースト、小さなステップ
- hypothesis: プロパティベースドテスト
