"""Userドメインエンティティ

【なぜこのファイルが必要？】
会員登録サイトを作るとき、「ユーザー」という概念をプログラムで表現する必要があります。
このファイルは「ユーザーとは何か？」を定義しています。

例えるなら、学校の名簿カードの「フォーマット」を決めているようなものです。
- 名前欄
- 住所欄
- 電話番号欄
などが書かれた「空白のカード」を定義しています。
"""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """ユーザーエンティティ

    【このクラスは何？】
    1人のユーザーの情報を入れる「箱」です。

    【なぜPydanticのBaseModelを使う？】
    普通のclassでも作れますが、Pydanticを使うと：
    - メールアドレスが正しい形式かチェックしてくれる
    - パスワードが空じゃないかチェックしてくれる
    自分でチェック機能を書かなくていいので楽です。
    """

    # 【idとは？】
    # ユーザーを識別するための「背番号」のようなもの。
    # 同じ名前の人がいても、この番号で区別できます。
    # uuid4は「世界で絶対に被らない番号を自動生成する」仕組みです。
    id: UUID = Field(default_factory=uuid4)

    # 【emailとは？】
    # ユーザーのメールアドレス。
    # EmailStrを使うと「abc」のような不正な値を自動で弾いてくれます。
    email: EmailStr

    # 【hashed_passwordとは？】
    # パスワードを暗号化したもの。
    # 「password123」→「$2b$12$xxx...」のように変換されます。
    # なぜ暗号化？→ データベースが盗まれても、元のパスワードがバレないため。
    # min_length=1は「空っぽは禁止」という意味。
    hashed_password: str = Field(min_length=1)

    # 【created_atとは？】
    # ユーザーが登録した日時。
    # 「いつ登録したか」を記録しておくと、後で分析に使えます。
    # lambda: は「呼ばれた瞬間の時刻を取得する」という意味。
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # 【is_activeとは？】
    # このユーザーが「有効」かどうか。
    # 退会したユーザーをFalseにすれば、データは残しつつログインを止められます。
    # なぜ削除しない？→ 過去の注文履歴などを残すため。
    is_active: bool = True
