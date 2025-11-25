# TDDセッション記録: Issue #7 Userドメインエンティティ

**日時**: 2025-11-24T10:25:37
**ブランチ**: feature/user-entity
**コミット**: 2e08895

---

## 概要

Issue #7 (Userドメインエンティティ) のバリデーション強化をTDDで実装

---

## 実施内容

### 1. 無効なメールアドレスの拒否テスト

**Phase**: Red → Green (既存の振る舞い確認)

```python
def test_create_user_with_invalid_email_raises_error():
    """無効なメールアドレスでUserを作成するとエラーになる"""
    with pytest.raises(ValidationError):
        User(
            email="invalid-email",
            hashed_password="hashed_password_here"
        )
```

- `EmailStr`型により既にバリデーション済み
- テストは成功（既存の振る舞いを文書化）

---

### 2. 空のパスワードの拒否テスト

**Phase**: Red → Green → Refactor

#### Red Phase
```python
def test_create_user_with_empty_password_raises_error():
    """空のパスワードでUserを作成するとエラーになる"""
    with pytest.raises(ValidationError):
        User(
            email="test@example.com",
            hashed_password=""
        )
```

- テスト失敗: `DID NOT RAISE ValidationError`

#### Green Phase
```python
# user.py
hashed_password: str = Field(min_length=1)
```

- 最小限の実装でテストをパス

#### Refactor Phase
- リファクタリング不要と判断

---

### 3. 空のメールアドレスの拒否テスト

**Phase**: Red → Green (既存の振る舞い確認)

```python
def test_create_user_with_empty_email_raises_error():
    """空のメールアドレスでUserを作成するとエラーになる"""
    with pytest.raises(ValidationError):
        User(
            email="",
            hashed_password="hashed_password_here"
        )
```

- `EmailStr`型により空文字列も拒否
- テストは成功

---

## 最終テスト結果

```
tests/domain/test_user_registration.py::test_create_user_with_valid_attributes PASSED
tests/domain/test_user_registration.py::test_create_user_with_invalid_email_raises_error PASSED
tests/domain/test_user_registration.py::test_create_user_with_empty_password_raises_error PASSED
tests/domain/test_user_registration.py::test_create_user_with_empty_email_raises_error PASSED

4 passed in 0.32s
```

---

## 変更ファイル

1. **backend/app/domain/user.py**
   - `hashed_password`に`min_length=1`バリデーション追加

2. **backend/tests/domain/test_user_registration.py**
   - 3つのテストケース追加
   - pytest, ValidationErrorのimport追加

3. **.gitignore**
   - memo.md追加

---

## 判断事項

### Docstring/リファクタリングの必要性

**結論**: 不要

理由:
- Pydanticの型アノテーションが自己説明的
- フィールド名が明確
- 16行のシンプルな実装
- Kent Beckの原則に従い、動作するきれいなコードを維持

---

## 環境問題

### Docker再ビルド
- `email-validator`パッケージが未インストール状態だった
- `docker compose up -d --build backend`で解決

### GitHub MCP
- 認証エラー発生
- 今後はgit CLIで対応

---

## 次のステップ

- Issue #8: UserRepositoryインターフェース
- PR作成: https://github.com/o-shige/tdd-training/compare/main...feature/user-entity

---

## 学び

1. **既存の振る舞いを文書化するテスト**も価値がある
2. **Pydanticの型システム**を活用してバリデーションを簡潔に
3. **最小限の実装**でテストをパスさせる (YAGNI)
