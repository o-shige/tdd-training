# TDD Session: Issue #8 UserRepositoryインターフェース

**日時**: 2025-11-24T11:01:01
**ブランチ**: feature/user-repository

---

## 概要

Issue #8「UserRepositoryインターフェース」をTDDで実装し、プロパティベースドテストを追加した。

---

## 実施内容

### 1. UserRepositoryインターフェースの実装（TDD）

#### テストケース1: saveメソッド
- **Red**: `test_user_repository_interface_has_save_method` を追加 → ImportError
- **Green**: `UserRepository`抽象クラスを作成、`save`メソッドを定義
- **Refactor**: 不要

#### テストケース2: find_by_emailメソッド
- **Red**: `test_user_repository_interface_has_find_by_email_method` を追加 → AssertionError
- **Green**: `find_by_email`メソッドを追加
- **Refactor**: 不要

#### テストケース3: find_by_idメソッド
- **Red**: `test_user_repository_interface_has_find_by_id_method` を追加 → AssertionError
- **Green**: `find_by_id`メソッドを追加
- **Refactor**: 不要

### 2. プロパティベースドテストの追加

`hypothesis`ライブラリを使用して品質保証観点のテストを追加。

#### 追加したテスト
1. `test_user_with_any_valid_email_is_created` - ランダムなメールアドレスでUser作成
2. `test_user_with_any_non_empty_password_is_created` - ランダムなパスワードでUser作成
3. `test_user_always_has_valid_uuid` - 生成されたUserが常にUUID v4を持つ

#### 発見した事実
- PydanticのEmailStrはドメインを小文字に正規化する
- Punycode形式の国際化ドメイン名をUnicode形式に変換する

### 3. ルールの追加

CLAUDE.mdに「テストの粒度」ルールを追加：
- **単純なテスト**: まとめて3つ程度を一括で実施してOK
- **複雑なテスト**: 1つずつ対話しながら実施

---

## 作成・更新ファイル

| ファイル | 変更内容 |
|---------|---------|
| `backend/app/domain/user_repository.py` | 新規作成 - UserRepository抽象クラス |
| `backend/tests/domain/test_user_registration.py` | テストケース追加（7件） |
| `backend/requirements.txt` | hypothesis追加 |
| `CLAUDE.md` | テストの粒度ルール追加 |
| `.gitignore` | .hypothesis/追加 |

---

## UserRepositoryインターフェース

```python
from abc import ABC, abstractmethod
from uuid import UUID
from app.domain.user import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def find_by_id(self, id: UUID) -> User | None:
        pass
```

---

## 学習ポイント

### abstractmethodとは
- 実装を持たない抽象メソッドを定義するデコレータ
- 継承したクラスで必ず実装が必要
- 依存性逆転の原則（DIP）を実現

### プロパティベースドテスト
- 具体的な値ではなくランダムな値を大量生成してテスト
- 「常に成り立つ性質」を検証
- エッジケースを自動的に発見できる

---

## コミット履歴

1. `feat: Issue #8 UserRepositoryインターフェースのsaveメソッド追加`
2. `feat: Issue #8 UserRepositoryインターフェース完成 + プロパティベースドテスト`

---

## PR情報

**URL**: https://github.com/o-shige/tdd-training/pull/new/feature/user-repository

**タイトル**: feat: Issue #8 UserRepositoryインターフェース

---

## 次のステップ

- Issue #9: RegistrationService
