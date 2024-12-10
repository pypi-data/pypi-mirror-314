import pytest


def test_get_user_nousername(gitlab):
    with pytest.raises(ValueError, match="cannot be called without username;"):
        gitlab.get_user()
