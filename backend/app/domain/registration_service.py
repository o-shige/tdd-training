"""ユーザー登録サービス

【なぜこのファイルが必要？】
「ユーザー登録」という作業の「手順書」です。

例えるなら、飲食店の「注文受付マニュアル」のようなもの：
1. お客さんが来たら → メールアドレスをもらう
2. すでに登録済み？ → エラーを返す
3. 新規なら → パスワードを暗号化して保存

【なぜServiceという名前？】
プログラミングでは「何かの処理をまとめたもの」をServiceと呼びます。
- 登録Service
- 注文Service
- 支払いService
など、機能ごとに分けると管理しやすくなります。
"""

from typing import Callable

from app.domain.password import hash_password
from app.domain.user import User


class RegistrationService:
    """ユーザー登録のビジネスロジックを担当

    【ビジネスロジックとは？】
    「このアプリ独自のルール」のこと。
    - 同じメールは登録できない
    - パスワードは暗号化する
    これらは「会員登録サービス」なら必須のルール。

    【なぜUserやRepositoryと分ける？】
    役割を分けると変更しやすくなるから：
    - User: データの形を変えたい → user.pyだけ変更
    - Repository: 保存先を変えたい → repositoryだけ変更
    - Service: ルールを変えたい → serviceだけ変更

    これを「関心の分離」と言います。
    """

    def __init__(self, repository, hasher: Callable[[str], str] = hash_password):
        """サービスを初期化する

        【なぜ__init__で受け取る？】
        これを「依存性注入（DI）」と言います。

        【依存性注入のメリット】
        テストのとき、本物のデータベースの代わりに
        「テスト用の偽物」を渡せます。
        本番→PostgreSQL、テスト→メモリ
        同じコードで両方動きます。

        【なぜhasherも受け取る？】
        本物のbcryptは遅い（1回0.1秒くらい）。
        テストで100回呼ぶと10秒かかってしまう。
        テスト用の高速な偽物を渡せるようにしています。
        """
        # 【_（アンダースコア）の意味】
        # 「このクラスの中だけで使う」という目印。
        # 外から直接触らないでね、という合図です。
        self._repository = repository
        self._hasher = hasher

    def register(self, email: str, password: str) -> User:
        """新しいユーザーを登録する

        【処理の流れ】
        1. 同じメールがすでに登録されていないかチェック
        2. パスワードを暗号化
        3. Userを作成
        4. リポジトリに保存
        5. 作成したUserを返す

        【なぜUserを返す？】
        呼び出し側が「登録できたユーザー」を使えるように。
        例：登録完了メールを送る、ログに記録する等。
        """
        # ステップ1: 重複チェック
        # 【なぜ先にチェック？】
        # 無駄な処理（パスワード暗号化等）を避けるため。
        # 「早く失敗する」のがプログラミングの原則。
        existing = self._repository.find_by_email(email)
        if existing:
            # 【なぜValueError？】
            # 「入力値が不正」というエラー。
            # ユーザーが悪いので、修正を促せます。
            raise ValueError(f"Email {email} is already registered")

        # ステップ2: パスワード暗号化
        # 【なぜここで暗号化？】
        # Userは「暗号化済み」のパスワードしか受け付けない。
        # 平文パスワードを持ち歩くのは危険だから。
        hashed = self._hasher(password)

        # ステップ3: Userオブジェクト作成
        # 【なぜemailとhashed_passwordだけ？】
        # id, created_at, is_activeは自動設定される。
        # 必要なものだけ渡せばOK。
        user = User(email=email, hashed_password=hashed)

        # ステップ4: 保存
        # 【なぜsaveの戻り値を使わない？】
        # 今は使わないが、将来DBがIDを振る場合に備えて。
        self._repository.save(user)

        # ステップ5: 作成したUserを返す
        return user
