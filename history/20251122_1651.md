# 会話履歴: GitHub MCP設定

**日時**: 2025-11-22 16:51
**プロジェクト**: tdd-training

---

## 概要

GitHub MCPサーバーの設定と、セキュリティ対策（環境変数の保護、.gitignoreの設定）を実施。

---

## 実施内容

### 1. MCP接続状況の確認

- **状態**: MCPサーバー未設定
- **結果**: `No MCP servers configured.`

### 2. GitHub MCPサーバーの追加

**実行コマンド**:
```bash
claude mcp add github -- npx -y @modelcontextprotocol/server-github
```

**設定ファイル**:
- `C:\Users\creat\OneDrive\ドキュメント\programing\tdd-training\.claude\mcp.json`

### 3. Personal Access Tokenの設定

**設定内容**:
- トークンを環境変数参照に変更（ハードコードを回避）
- `${GITHUB_PERSONAL_ACCESS_TOKEN}` を使用

**最終的な`.claude/mcp.json`**:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

### 4. 冗長設定の削除

**削除対象**:
- `~/.claude.json` 内の重複したGitHub MCPサーバー設定

**理由**:
- プロジェクトレベル (`.claude/mcp.json`) の設定のみを使用

### 5. .gitignoreの更新

**追加項目**:
- `history/` - 会話履歴ディレクトリ

**既存項目**:
- `.claude/` - MCPサーバー設定（トークン含む）
- `.kiro/`
- `CLAUDE.md`

---

## 必要なアクション

### 環境変数の設定（Windows PowerShell）

```powershell
[System.Environment]::SetEnvironmentVariable("GITHUB_PERSONAL_ACCESS_TOKEN", "<your-token>", "User")
```

### セキュリティ推奨事項

1. トークンがチャット履歴に公開されたため、新しいトークンを作成
2. 古いトークンを無効化
3. トークン作成: https://github.com/settings/tokens

---

## ファイル変更一覧

| ファイル | 操作 |
|---------|------|
| `.claude/mcp.json` | 環境変数参照に変更 |
| `~/.claude.json` | 冗長なMCP設定を削除 |
| `.gitignore` | `history/` を追加 |

---

## 次のステップ

1. 環境変数 `GITHUB_PERSONAL_ACCESS_TOKEN` を設定
2. Claude Codeを再起動
3. `/mcp` でGitHub MCPサーバーの接続を確認
