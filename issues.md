# TDD JWT 認証プロジェクト - イシューリスト

## Week 1: 基盤構築 + 純粋関数の TDD

| #   | イシュー                        | TDD テスト対象     | 優先度 | 状態 |
| --- | ------------------------------- | ------------------ | ------ | ---- |
| 1   | Docker Compose 環境セットアップ | -                  | High   | [x]  |
| 2   | FastAPI スケルトン作成          | -                  | High   | [x]  |
| 3   | Next.js スケルトン作成          | -                  | High   | [x]  |
| 4   | pytest 環境構築                 | -                  | High   | [x]  |
| 5   | パスワードハッシュ化機能        | `test_password.py` | High   | [x]  |
| 6   | JWT 生成・検証機能              | `test_jwt.py`      | High   | [x]  |

---

## Week 2: ユーザー登録の TDD + UI

| #   | イシュー                        | TDD テスト対象                  | 優先度 | 状態 |
| --- | ------------------------------- | ------------------------------- | ------ | ---- |
| 7   | User ドメインエンティティ       | `test_user_registration.py`     | High   | [ｘ] |
| 8   | UserRepository インターフェース | `test_user_registration.py`     | High   | [x]  |
| 9   | RegistrationService             | `test_user_registration.py`     | High   | [x]  |
| 10  | SQLAlchemy UserRepository 実装  | `test_user_repository.py`       | High   | [x]  |
| 11  | 登録 API エンドポイント         | `test_registration_endpoint.py` | High   | [x]  |
| 12  | 登録フォーム UI（Next.js）      | E2E テスト（任意）              | Medium | [x]  |
| 12a | 品質保証観点でのテスト          | 全テスト（任意）                | Medium | [ ]  |

---

## Week 3: ログイン + セッション管理の TDD

| #   | イシュー                      | TDD テスト対象            | 優先度 | 状態 |
| --- | ----------------------------- | ------------------------- | ------ | ---- |
| 13  | LoginService 実装             | `test_login.py`           | High   | [ ]  |
| 14  | 認証エラーハンドリング        | `test_login.py`           | High   | [ ]  |
| 15  | Redis セッションストア        | `test_session.py`         | High   | [ ]  |
| 16  | ログイン API エンドポイント   | `test_login_endpoint.py`  | High   | [ ]  |
| 17  | ログインフォーム UI           | E2E テスト（任意）        | Medium | [ ]  |
| 18  | 保護されたルート（/users/me） | `test_protected_route.py` | High   | [ ]  |
| 19  | ダッシュボード UI             | E2E テスト（任意）        | Medium | [ ]  |

---

## Week 4: トークンリフレッシュ + OAuth

| #   | イシュー                  | TDD テスト対象             | 優先度 | 状態 |
| --- | ------------------------- | -------------------------- | ------ | ---- |
| 20  | リフレッシュトークン生成  | `test_refresh_token.py`    | High   | [ ]  |
| 21  | アクセストークン更新 API  | `test_refresh_endpoint.py` | High   | [ ]  |
| 22  | Google OAuth 設定         | -                          | Medium | [ ]  |
| 23  | GoogleOAuthService        | `test_oauth.py`            | High   | [ ]  |
| 24  | OAuth コールバック API    | `test_oauth_callback.py`   | High   | [ ]  |
| 25  | Google ログインボタン追加 | E2E テスト（任意）         | Medium | [ ]  |

---

## 横断的イシュー

| #   | イシュー                     | 備考                        | 状態 |
| --- | ---------------------------- | --------------------------- | ---- |
| 26  | .gitignore 作成              | Python + Node.js 用         | [x]  |
| 27  | CI/CD 設定（GitHub Actions） | テスト自動実行              | [x]  |
| 28  | エラーハンドリング共通化     | カスタム例外クラス          | [ ]  |
| 29  | API 仕様書（OpenAPI）        | FastAPI 自動生成            | [ ]  |
| 30  | SECRET_KEY 等を環境変数化    | JWT 設定を.env から読み込み | [ ]  |

---

## TDD サイクルの進め方

各イシューは以下のサイクルで進める：

1. **Red**: 失敗するテストを書く（10 分）
2. **Green**: 最小限の実装でテストを通す（20 分）
3. **Refactor**: コードをきれいにする（10 分）
4. **UI 確認**: Docker 起動してブラウザで動作確認（10 分）
5. **Git commit**: 1 サイクルごとにコミット（5 分）

---

## 参考資料

- t_wada 式 TDD: 「動作するきれいなコード」を目指す
- Kent Beck: テストファースト、小さなステップ
- Tidy First?: リファクタリングを先に行う判断
