# TDD対話ルール追加 + CodeRabbit設定

**日時**: 2025-11-22 20:45
**前回からの継続**: 20251122_2030.md

---

## 概要

1. TDD実施時の対話ルールをCLAUDE.mdに追記
2. CodeRabbit設定ファイル（.coderabbit.yaml）を新規作成

---

## 1. TDD対話ルールの改善

### 問題点

前回のTDD実装では、エージェントが自律的にテストと実装を書いてしまった。ユーザーがリードする形で対話的に進めたい。

### 改善内容（CLAUDE.mdに追記）

**各フェーズでの振る舞い**:

| Phase | 改善前 | 改善後 |
|-------|--------|--------|
| Red | 自律的にテスト作成 | テストケース提案→承認→実装 |
| Green | 自律的に実装 | 方針提示→承認→実装 |
| Refactor | 自律的に判断 | 案を提示→ユーザーが判断 |

**対話の原則**:
- 各ステップで一旦停止し、ユーザーの指示を待つ
- 「〜しますか？」「〜でよいですか？」と確認する
- ユーザーが明示的に指示するまでコードを書かない
- 選択肢がある場合は提示してユーザーに選ばせる

---

## 2. CodeRabbit設定

### 確認事項

**Q**: .coderabbit.yamlを更新する感じ？
**A**: まだ存在しないので新規作成

**Q**: 新規作成してプッシュするだけで設定が変わるの？
**A**: はい。Code Rabbit GitHub AppがPR作成時に自動で読み込む

### 設定内容

```yaml
language: "ja"                    # 日本語レビュー

reviews:
  profile: chill                  # 穏やかなフィードバック
  high_level_summary: true        # PR要約を自動生成
  sequence_diagrams: true         # シーケンス図生成
  auto_review:
    enabled: true
    drafts: false
  path_filters:                   # 除外パス
    - "!node_modules/**"
    - "!**/__pycache__/**"
    - "!dist/**"
    - "!.next/**"

tools:
  ruff:
    enabled: true                 # Python linter
  eslint:
    enabled: true                 # JS/TS linter
  gitleaks:
    enabled: true                 # シークレット検出

knowledge_base:
  code_guidelines:
    enabled: true
    filePatterns:
      - "**/CLAUDE.md"            # プロジェクトルール参照
```

### Git操作

| 操作 | 詳細 |
|------|------|
| ブランチ | `feature/password-hashing`（既存） |
| コミット | `chore: CodeRabbit設定ファイルを追加` |
| プッシュ | ✅ 完了 |

---

## 作成・更新されたファイル

| ファイル | 操作 |
|----------|------|
| `CLAUDE.md` | 「TDD対話ルール」セクション追記 |
| `.coderabbit.yaml` | 新規作成 |

---

## 次のアクション

1. [ ] PRを作成（https://github.com/o-shige/tdd-training/pull/new/feature/password-hashing）
2. [ ] Code Rabbitの日本語レビューを確認
3. [ ] レビュー内容を確認してマージ

---

## 参考リンク

- [CodeRabbit Configuration Reference](https://docs.coderabbit.ai/reference/configuration)
- [Configure CodeRabbit](https://docs.coderabbit.ai/configure-coderabbit/)
