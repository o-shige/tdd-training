# GitHub Actions CI/CD設定セッション

日時: 2025-11-23

## 概要

Issue #27「CI/CD設定（GitHub Actions）」の実装とGitHub Actionsの概念学習

---

## 実施内容

### 1. CI/CD設定の方針決定

- **ワークフロー分離**: Backend/Frontendを別ファイルに分離（ベストプラクティス）
  - 並列実行で高速化
  - 失敗の特定が容易
  - 独立したキャッシュ最適化

- **対象ブランチ**: mainへのpush/PRのみ
  - feature branchへの直接pushでは実行されない
  - PRを作成した時点で実行される

### 2. 作成したファイル

- `.github/workflows/backend.yml` - Pythonテスト用
- `.github/workflows/frontend.yml` - Next.jsビルド/lint用
- `frontend/package-lock.json` - 依存関係のバージョン固定

### 3. コミット・PR

- コミット: `ci: GitHub Actions CI/CD設定を追加`
- ブランチ: `feature/password-hashing`
- PR作成: mainブランチへ

---

## 学習内容

### package-lock.jsonの役割

- **目的**: 依存関係のバージョンを完全固定
- **メリット**: 「誰が・いつ・どこで実行しても同じバージョンがインストールされる」
- **重要**: .gitignoreに入れてはいけない（コミットしてpushすることで意味がある）

| コマンド | 動作 |
|----------|------|
| `npm install` | lock fileを作成/更新 |
| `npm ci` | lock fileを厳密に使用（CIで推奨） |

### GitHub Actionsのトリガー（`on:`）

```yaml
on:
  push:
    branches: [main]      # mainに直接pushしたとき
  pull_request:
    branches: [main]      # mainへのPRを作成/更新したとき
```

- `pull_request`はマージ前に実行される（事前確認）
- `push`はマージ後に実行される（最終確認）
- **PRを作成したタイミングで実行**（マージ時ではない）

### キャッシュの意味

- 依存関係（pip/npm）をキャッシュして次回以降高速化
- GitHub Actionsの無料枠を節約

### 実行環境

- **仮想マシン（VM）** で実行（コンテナではない）
- `runs-on: ubuntu-latest` - GitHubが管理するUbuntu VM
- 各実行で新しいVMが作られ、終了後に破棄される
- パブリックリポジトリは無料、プライベートは月2000分

### ワークフロー構造

```yaml
jobs:
  test:                           # ジョブID
    runs-on: ubuntu-latest        # 実行環境
    defaults:
      run:
        working-directory: backend  # 全コマンドの実行ディレクトリ
    steps:
      - uses: actions/checkout@v4   # Action（再利用可能な処理）
      - run: pytest tests/ -v       # コマンド（シェル実行）
```

| ステップ種類 | 書き方 | 説明 |
|-------------|--------|------|
| Action | `uses:` | 他の人が作った再利用可能な処理 |
| コマンド | `run:` | シェルコマンドを直接実行 |

---

## 作成したワークフロー詳細

### backend.yml

- Python 3.11
- pipキャッシュ有効
- `pytest tests/ -v` でテスト実行

### frontend.yml

- Node.js 20
- npmキャッシュ有効
- `npm ci` → `npm run lint` → `npm run build`

---

## 次のステップ

- PRをマージしてCIが正常に動作することを確認
- 将来DB必要なテストを追加する場合、GitHub ActionsでもPostgreSQLサービス追加が必要
- critical脆弱性（`npm audit`で検出）の対応
