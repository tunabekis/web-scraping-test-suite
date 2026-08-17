# src/factories/login_test_data.py

from typing import List, Dict


def login_scenarios() -> List[Dict]:
    """
    Returns a list of login test scenarios.

    Each scenario is a dict with:
        - id: used as the pytest test id
        - username
        - password
        - should_succeed (bool)
    """
    return [
        {
            "id": "valid_credentials",
            "username": "testuser",
            "password": "password123",
            "should_succeed": True,
        },
        {
            "id": "wrong_username",
            "username": "wronguser",
            "password": "password123",
            "should_succeed": False,
        },
        {
            "id": "wrong_password",
            "username": "testuser",
            "password": "wrongpass",
            "should_succeed": False,
        },
        {
            "id": "empty_username",
            "username": "",
            "password": "password123",
            "should_succeed": False,
        },
        {
            "id": "empty_password",
            "username": "testuser",
            "password": "",
            "should_succeed": False,
        },
    ]
