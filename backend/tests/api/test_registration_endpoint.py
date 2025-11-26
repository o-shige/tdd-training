"""登録APIエンドポイントのテスト"""

import pytest
from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)


def test_register_user_with_valid_data():
    """有効なデータでユーザー登録すると201 Createdが返される"""
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    response = client.post(
        "/api/register",
        json={
            "email": unique_email,
            "password": "password123"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == unique_email
    assert "id" in response.json()
    assert "hashed_password" not in response.json()  # パスワードは返さない


def test_register_user_with_invalid_email():
    """無効なメールアドレスだと422 Unprocessable Entityが返される"""
    response = client.post(
        "/api/register",
        json={
            "email": "invalid-email",
            "password": "password123"
        }
    )

    assert response.status_code == 422
    assert "detail" in response.json()


def test_register_user_with_short_password():
    """短いパスワードだと400 Bad Requestが返される"""
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    response = client.post(
        "/api/register",
        json={
            "email": unique_email,
            "password": "123"
        }
    )

    assert response.status_code == 400
    assert "detail" in response.json()
    assert "error" in response.json()["detail"]


def test_register_user_with_duplicate_email():
    """既存のメールアドレスだと409 Conflictが返される"""
    duplicate_email = f"duplicate_{uuid.uuid4().hex[:8]}@example.com"

    # まず1つ目を登録
    client.post(
        "/api/register",
        json={
            "email": duplicate_email,
            "password": "password123"
        }
    )

    # 同じメールアドレスで再度登録
    response = client.post(
        "/api/register",
        json={
            "email": duplicate_email,
            "password": "different_password"
        }
    )

    assert response.status_code == 409
    assert "detail" in response.json()
    assert "error" in response.json()["detail"]


def test_register_user_with_invalid_json():
    """不正なJSONだと422 Unprocessable Entityが返される"""
    response = client.post(
        "/api/register",
        content="invalid json",  # contentに変更
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422


def test_register_user_with_missing_fields():
    """必須フィールドが不足していると422 Unprocessable Entityが返される"""
    unique_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    response = client.post(
        "/api/register",
        json={
            "email": unique_email
            # passwordが不足
        }
    )

    assert response.status_code == 422
    assert "detail" in response.json()