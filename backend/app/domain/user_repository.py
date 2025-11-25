"""UserRepositoryインターフェース

【なぜこのファイルが必要？】
ユーザー情報を「どこかに保存する」ためのルールブックです。

例えるなら、図書館の「本の貸し出しルール」のようなものです：
- 「保存する」→ 本を棚に戻す
- 「メールで探す」→ 本のタイトルで探す
- 「IDで探す」→ 本のバーコードで探す

【なぜ「抽象クラス」にする？】
実際の保存先はいろいろありえます：
- PostgreSQLデータベース
- Redisキャッシュ
- テスト用のメモリ

でも、使う側は「保存先がどこか」を気にしなくていい。
「saveを呼べば保存される」ことだけ知っていればOK。
これを「抽象化」と言います。
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.user import User


class UserRepository(ABC):
    """ユーザーデータの保存・検索を行うインターフェース

    【ABCとは？】
    Abstract Base Class（抽象基底クラス）の略。
    「このクラスは直接使えません。継承して使ってね」という意味。

    【@abstractmethodとは？】
    「このメソッドは必ず実装してね」という約束。
    実装しないとエラーになるので、実装忘れを防げます。

    【なぜインターフェースを使う？】
    RegistrationServiceは「保存する機能」が欲しいだけ。
    保存先がPostgreSQLかRedisかは関係ない。
    インターフェースを使うと、保存先を後から自由に変えられます。
    """

    @abstractmethod
    def save(self, user: User) -> User:
        """ユーザーを保存する

        【なぜUserを返す？】
        保存後のユーザー（IDが付与されたもの等）を返すため。
        データベースがIDを自動生成する場合に便利。
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        """メールアドレスでユーザーを探す

        【なぜNoneを返す可能性がある？】
        見つからない場合があるから。
        「| None」は「Userか、見つからなかったらNone」という意味。
        """
        pass

    @abstractmethod
    def find_by_id(self, id: UUID) -> User | None:
        """IDでユーザーを探す

        【emailとidの違いは？】
        - email: ユーザーが自分で決める。変更される可能性あり
        - id: システムが自動生成。絶対に変わらない

        注文履歴などは「id」で紐付けます。
        メールアドレスが変わっても履歴が消えないように。
        """
        pass
