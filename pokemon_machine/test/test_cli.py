"""Tests for game_feature.cli"""

import pytest
from unittest.mock import patch, MagicMock
from game_feature.cli import (
    do_register,
    do_login,
    do_logout,
    do_get_pokemon,
    _entry_menu,
    _main_menu,
    main,
)


def _mock_response(status_code: int = 200, json_data: dict | None = None):
    """Build a fake ``requests.Response``."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.ok = 200 <= status_code < 300
    resp.json.return_value = json_data or {}
    resp.text = str(json_data or "")
    return resp


# =========================================================================
# do_register
# =========================================================================

class TestDoRegister:
    @patch("game_feature.cli.requests.post")
    @patch("game_feature.cli._input", side_effect=["Ash", "10", "brave", "secret"])
    def test_success(self, _mock_input, mock_post):
        mock_post.return_value = _mock_response(200, {"owner": {"id": 1}})
        result = do_register()
        assert result is None
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["json"]["name"] == "Ash"

    @patch("game_feature.cli.requests.post")
    @patch("game_feature.cli._input", side_effect=["Ash", "10", "brave", "secret"])
    def test_server_error(self, _mock_input, mock_post):
        mock_post.return_value = _mock_response(409, {"message": "Data already exists"})
        result = do_register()
        assert result is None

    @patch("game_feature.cli.requests.post", side_effect=Exception("Connection refused"))
    @patch("game_feature.cli._input", side_effect=["Ash", "10", "brave", "secret"])
    def test_connection_error(self, _mock_input, mock_post):
        """Non-ConnectionError exceptions are not caught — verifies the
        except clause targets ConnectionError specifically."""
        with pytest.raises(Exception, match="Connection refused"):
            do_register()


# =========================================================================
# do_login
# =========================================================================

class TestDoLogin:
    @patch("game_feature.cli.requests.post")
    @patch("game_feature.cli._input", side_effect=["Ash", "secret"])
    def test_success_returns_session(self, _mock_input, mock_post):
        fake_data = {"owner": {"id": 1, "name": "Ash"}, "access_token": "tok"}
        mock_post.return_value = _mock_response(200, fake_data)
        result = do_login()
        assert result is not None
        assert result["owner"]["name"] == "Ash"
        assert result["access_token"] == "tok"

    @patch("game_feature.cli.requests.post")
    @patch("game_feature.cli._input", side_effect=["Ash", "wrong"])
    def test_bad_credentials(self, _mock_input, mock_post):
        mock_post.return_value = _mock_response(401, {"message": "Verification failed"})
        result = do_login()
        assert result is None


# =========================================================================
# do_logout
# =========================================================================

class TestDoLogout:
    @patch("game_feature.cli.requests.post")
    def test_success(self, mock_post, fake_session):
        mock_post.return_value = _mock_response(200, {"status": "success"})
        do_logout(fake_session)
        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["json"]["user_id"] == "1"

    @patch("game_feature.cli.requests.post")
    def test_server_error(self, mock_post, fake_session):
        mock_post.return_value = _mock_response(500, {"message": "Server error"})
        # should not raise — just prints the error
        do_logout(fake_session)


# =========================================================================
# do_get_pokemon
# =========================================================================

class TestDoGetPokemon:
    def test_rejects_when_limit_reached(self, full_session, capsys):
        do_get_pokemon(full_session)
        output = capsys.readouterr().out
        assert "storage is full" in output.lower()

    @patch("game_feature.cli.run_quiz", return_value=25)
    @patch("game_feature.cli.requests")  # unused but imported
    def test_calls_quiz_when_under_limit(self, _mock_req, mock_quiz, fake_session, capsys):
        # We need to also mock the dynamic import of pokemon_hunter
        with patch.dict("sys.modules", {"pokemon_hunter": MagicMock(), "pokemon_hunter.pokemon_hunter": MagicMock()}):
            import pokemon_hunter.calling as ph
            ph.get_pokemon = MagicMock(return_value={"name": "pikachu"})

            do_get_pokemon(fake_session)
            mock_quiz.assert_called_once()


# =========================================================================
# Menu helpers
# =========================================================================

class TestEntryMenu:
    @patch("game_feature.cli._input", return_value="1")
    def test_returns_choice(self, _mock_input):
        assert _entry_menu() == "1"


class TestMainMenu:
    @patch("game_feature.cli._input", return_value="2")
    def test_returns_choice(self, _mock_input):
        assert _main_menu("Ash") == "2"


# =========================================================================
# main()  — full flow
# =========================================================================

class TestMain:
    @patch("game_feature.cli._entry_menu", side_effect=["0"])
    def test_exit_immediately(self, _mock_menu):
        main()  # should not raise

    @patch("game_feature.cli.do_login")
    @patch("game_feature.cli.do_logout")
    @patch("game_feature.cli._main_menu", side_effect=["2"])
    @patch("game_feature.cli._entry_menu", side_effect=["1", "0"])
    def test_login_then_logout(self, _menu, _main, mock_logout, mock_login):
        mock_login.return_value = {
            "owner": {"id": 1, "name": "Ash", "pokemon_limit": 3, "pokemon_count": 0},
            "access_token": "tok",
        }
        main()
        mock_login.assert_called_once()
        mock_logout.assert_called_once()

    @patch("game_feature.cli.do_register", return_value=None)
    @patch("game_feature.cli._entry_menu", side_effect=["2", "0"])
    def test_register_then_exit(self, _menu, mock_register):
        main()
        mock_register.assert_called_once()

    @patch("game_feature.cli._entry_menu", side_effect=["9", "0"])
    def test_invalid_choice_then_exit(self, _menu, capsys):
        main()
        output = capsys.readouterr().out
        assert "Invalid choice" in output
