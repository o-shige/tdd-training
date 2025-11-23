"""パスワードハッシュ化機能のテスト

TDDサイクル: Red -> Green -> Refactor
要件: ユーザーのパスワードを安全にハッシュ化・検証する
"""

from app.domain.password import hash_password, verify_password


class TestHashPassword:
    """hash_password関数のテスト"""

    def test_ハッシュ化された値は元のパスワードと異なる(self):
        password = "mysecretpassword"
        hashed = hash_password(password)
        assert hashed != password

    def test_ハッシュ値はstr型で返される(self):
        password = "mysecretpassword"
        hashed = hash_password(password)
        assert isinstance(hashed, str)

    def test_同じパスワードでも毎回異なるハッシュが生成される(self):
        password = "mysecretpassword"
        hashed1 = hash_password(password)
        hashed2 = hash_password(password)
        assert hashed1 != hashed2


class TestVerifyPassword:
    """verify_password関数のテスト"""

    def test_正しいパスワードで検証が成功する(self):
        password = "mysecretpassword"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_間違ったパスワードで検証が失敗する(self):
        password = "mysecretpassword"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)
        assert verify_password(wrong_password, hashed) is False

    def test_空文字列のパスワードでも動作する(self):
        password = ""
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
        assert verify_password("notempty", hashed) is False
