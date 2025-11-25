"""パスワードハッシュ化モジュール

【なぜこのファイルが必要？】
パスワードを「暗号化」するための専用ツールです。

【なぜ暗号化が必要？】
データベースが盗まれたとき、パスワードがそのまま保存されていたら大問題。
暗号化しておけば、盗まれても元のパスワードがわかりません。

【ハッシュ化とは？】
「password123」→「$2b$12$abcdef...」のように変換すること。
特徴：
- 元に戻せない（一方通行）
- 同じ入力 → 同じ出力
- 少しでも違う入力 → 全然違う出力

例えるなら「肉をミンチにする」ようなもの。
ミンチから元の肉の形はわからないけど、
同じ肉なら同じミンチになる。
"""

from passlib.context import CryptContext

# 【CryptContextとは？】
# パスワードの暗号化方法を設定する「設定書」。
# bcryptは現在最も安全とされている暗号化方式。
# deprecated="auto"は「古い方式は自動で更新する」という意味。
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """パスワードをハッシュ化する

    【どういうときに使う？】
    ユーザーが新規登録するとき。
    入力されたパスワードを暗号化してから保存します。

    【なぜbcryptが良い？】
    - わざと遅い（攻撃者が総当たりしにくい）
    - 自動で「ソルト」を追加（同じパスワードでも違う結果になる）

    Args:
        password: 平文パスワード（ユーザーが入力したもの）

    Returns:
        ハッシュ化されたパスワード（データベースに保存するもの）

    例:
        hash_password("password123")
        → "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN..."
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """パスワードを検証する

    【どういうときに使う？】
    ユーザーがログインするとき。
    入力されたパスワードと、保存されているハッシュを比較します。

    【仕組み】
    1. 入力されたパスワードをハッシュ化
    2. 保存されているハッシュと比較
    3. 一致したらTrue

    Args:
        password: 平文パスワード（ユーザーが入力したもの）
        hashed: ハッシュ化されたパスワード（データベースから取得したもの）

    Returns:
        検証結果（Trueならログイン成功）

    例:
        verify_password("password123", "$2b$12$LQv3c1y...")
        → True（正しいパスワード）

        verify_password("wrong", "$2b$12$LQv3c1y...")
        → False（間違ったパスワード）
    """
    return pwd_context.verify(password, hashed)
