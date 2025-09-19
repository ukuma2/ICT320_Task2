import pytest
from app import app, R
from auth import hash_text, verify_text
from db import user_key


@pytest.fixture
def client():
    # Flask test client for simulating HTTP requests
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_password_hash_and_verify():
    pw = "mypassword"
    hashed = hash_text(pw)
    assert hashed.startswith("$2b$")
    assert verify_text(pw, hashed) is True
    assert verify_text("wrongpw", hashed) is False


def test_register_and_login_flow(client):
    email = "autotest@example.com"
    firstname = "Auto"

    # Clean up if user already exists
    R.delete(user_key(email))

    # Register new user
    resp = client.post("/register", data={
        "login": email,
        "firstname": firstname,
        "password": "secret123",
        "security_a": "blue"
    }, follow_redirects=True)
    assert b"Account created successfully" in resp.data

    # Login with correct password
    resp = client.post("/login", data={
        "login": email,
        "password": "secret123"
    }, follow_redirects=True)
    assert f"Welcome, {firstname}".encode() in resp.data

    # Login with wrong password
    resp = client.post("/login", data={
        "login": email,
        "password": "wrongpass"
    }, follow_redirects=True)
    assert b"Incorrect password" in resp.data


def test_forgot_password_flow(client):
    email = "autotest_reset@example.com"
    firstname = "ResetUser"

    # Clean up
    R.delete(user_key(email))

    # Register new user
    client.post("/register", data={
        "login": email,
        "firstname": firstname,
        "password": "oldpw",
        "security_a": "milo"
    }, follow_redirects=True)

    # Trigger forgot password
    resp = client.post("/forgot", data={"login": email}, follow_redirects=True)
    assert b"Answer" in resp.data  # should show security question form

    # Submit wrong answer
    resp = client.post("/forgot_verify", data={
        "login": email,
        "answer": "wrong",
        "newpw": "newpw123"
    }, follow_redirects=True)
    assert b"Incorrect answer" in resp.data

    # Submit correct answer
    resp = client.post("/forgot_verify", data={
        "login": email,
        "answer": "milo",
        "newpw": "newpw123"
    }, follow_redirects=True)
    assert b"Password reset successful" in resp.data

    # Verify new password works
    resp = client.post("/login", data={
        "login": email,
        "password": "newpw123"
    }, follow_redirects=True)
    assert f"Welcome, {firstname}".encode() in resp.data
