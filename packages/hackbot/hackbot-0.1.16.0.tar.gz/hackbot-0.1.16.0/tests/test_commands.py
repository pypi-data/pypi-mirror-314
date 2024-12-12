import pytest
import argparse
import tempfile
import os
from unittest.mock import patch, MagicMock
from hackbot.commands import (
    hackbot_run,
    show_selectable_models,
    check_common_args,
    check_run_args,
    check_scope_args,
    setup_parser,
)


@pytest.fixture
def mock_args():
    args = MagicMock()
    args.address = "https://app.hackbot.co"
    args.port = None
    args.api_key = "test_api_key"
    args.source = "test_source"
    args.output = None
    args.auth_only = False
    args.issues_repo = None
    args.github_api_key = None
    args.command = "run"
    return args


@patch("hackbot.commands.authenticate")
@patch("hackbot.commands.cli_run")
def test_hackbot_run_success(mock_cli_run, mock_auth, mock_args):
    """Test successful hackbot run command execution"""

    mock_auth.return_value = True
    mock_cli_run.return_value = [{"bug_id": "TEST-1"}]

    result = hackbot_run(mock_args)
    assert result == 0

    mock_auth.assert_called_once()
    mock_cli_run.assert_called_once()


@patch("os.path.exists")
def test_hackbot_run_invalid_source(mock_exists, mock_args):
    """Test hackbot run with invalid source directory"""
    mock_exists.return_value = False

    result = hackbot_run(mock_args)
    assert result == 1


@patch("os.path.exists")
@patch("hackbot.commands.authenticate")
def test_hackbot_run_auth_failure(mock_auth, mock_exists, mock_args):
    """Test hackbot run with authentication failure"""
    mock_exists.return_value = True
    mock_auth.return_value = False

    result = hackbot_run(mock_args)
    assert result == 1


@patch("os.path.exists")
@patch("hackbot.commands.authenticate")
@patch("hackbot.commands.cli_run")
def test_hackbot_run_auth_only(mock_cli_run, mock_auth, mock_exists, mock_args):
    """Test hackbot run with auth_only flag"""
    mock_exists.return_value = True
    mock_auth.return_value = True
    mock_args.auth_only = True

    result = hackbot_run(mock_args)
    assert result == 0

    mock_cli_run.assert_not_called()


@patch("os.path.exists")
@patch("hackbot.commands.authenticate")
@patch("hackbot.commands.cli_run")
@patch("hackbot.commands.generate_issues")
def test_hackbot_run_with_github(
    mock_generate_issues, mock_cli_run, mock_auth, mock_exists, mock_args
):
    """Test hackbot run with GitHub integration"""
    mock_exists.return_value = True
    mock_auth.return_value = True
    mock_cli_run.return_value = [{"bug_id": "TEST-1"}]
    mock_args.issues_repo = "test/repo"
    mock_args.github_api_key = "github_token"

    result = hackbot_run(mock_args)
    assert result == 0

    mock_generate_issues.assert_called_once_with(
        "test/repo", "github_token", [{"bug_id": "TEST-1"}]
    )


@patch("hackbot.commands.os.path.exists")
def test_check_github_args(mock_exists):
    """Test GitHub argument validation using argparse"""
    # Create parser with the required arguments
    parser = setup_parser()

    mock_exists.return_value = True

    # Test case 1: Issues repo without GitHub API key
    args = parser.parse_args(["--api-key", "test-key", "run", "--issues_repo", "test/repo"])
    result = check_run_args(args)
    assert isinstance(result, int)
    assert result == 1

    # Test case 2: No issues repo and no GitHub API key (should pass this check)
    args = parser.parse_args(["--api-key", "test-key", "run"])
    result = check_run_args(args)
    assert isinstance(result, argparse.Namespace)
    assert result.api_key == "test-key"
    assert result.command == "run"

    # Test case 3: Issues repo with GitHub API key
    args = parser.parse_args(
        [
            "--api-key",
            "test-key",
            "run",
            "--issues_repo",
            "test/repo",
            "--github_api_key",
            "github_token",
        ]
    )
    result = check_run_args(args)
    assert isinstance(result, argparse.Namespace)
    assert result.api_key == "test-key"
    assert result.command == "run"
    assert result.issues_repo == "test/repo"
    assert result.github_api_key == "github_token"

    # Test case 4: GitHub API key only
    args = parser.parse_args(["--api-key", "test-key", "run", "--github_api_key", "github_token"])
    result = check_run_args(args)
    assert isinstance(result, int)
    assert result == 1

    with pytest.raises(SystemExit) as excinfo:
        args = parser.parse_args(
            [
                "--api-key",
                "test-key",
                "scope",
                "--issues_repo",
                "test/repo",
            ]
        )
    assert excinfo.value.code == 2

    with pytest.raises(SystemExit) as excinfo:
        args = parser.parse_args(
            [
                "--api-key",
                "test-key",
                "models",
                "--issues_repo",
                "test/repo",
            ]
        )
    assert excinfo.value.code == 2


@patch("hackbot.commands.os.path.exists")
def test_check_api_args(mock_exists):
    """Test API argument validation"""
    mock_exists.return_value = True
    parser = setup_parser()
    args = parser.parse_args(["run"])

    result = check_common_args(args)
    assert isinstance(result, int)
    assert result == 1

    args = parser.parse_args(
        [
            "--api-key",
            "test-key",
            "run",
        ]
    )
    result = check_common_args(args)
    assert isinstance(result, argparse.Namespace)
    assert result.api_key == "test-key"
    assert result.command == "run"

    args = parser.parse_args(
        [
            "--api-key",
            "test-key",
            "--address",
            "test://test.com",
            "--port",
            "90",
            "run",
        ]
    )
    result = check_common_args(args)
    assert isinstance(result, argparse.Namespace)
    assert result.api_key == "test-key"
    assert result.command == "run"
    assert result.address == "test://test.com"
    assert result.port == 90

    args = parser.parse_args(
        [
            "--api-key",
            "test-key",
            "--address",
            "test://test.com",
            "run",
        ]
    )
    result = check_common_args(args)
    assert isinstance(result, argparse.Namespace)
    assert result.api_key == "test-key"
    assert result.command == "run"
    assert result.address == "test://test.com"

    args = parser.parse_args(
        [
            "--api-key",
            "test-key",
            "--port",
            "90",
            "run",
        ]
    )
    result = check_common_args(args)
    assert isinstance(result, argparse.Namespace)
    assert result.api_key == "test-key"
    assert result.command == "run"
    assert result.port == 90


@patch("hackbot.commands.os.path.exists")
def test_check_scope_args(mock_exists):
    """Test scope argument validation"""
    mock_exists.return_value = True
    parser = setup_parser()
    args = parser.parse_args(
        [
            "--api-key",
            "test-key",
            "scope",
        ]
    )

    result = check_scope_args(args)
    assert isinstance(result, argparse.Namespace)
    assert result.api_key == "test-key"
    assert result.command == "scope"

    args = parser.parse_args(
        [
            "scope",
        ]
    )

    result = check_scope_args(args)
    assert isinstance(result, int)
    assert result == 1


@patch("hackbot.commands.os.path.exists")
def test_check_run_args(mock_exists):
    """Test run command argument validation"""
    mock_exists.return_value = True
    parser = setup_parser()

    with pytest.raises(SystemExit) as excinfo:
        args = parser.parse_args(
            [
                "--api-key",
                "test-key",
                "--address",
                "test://test.com",
                "--port",
                "90",
                "--debug",
                "true",
                "--profile",
                "starter",
                "--model",
                "gpt-4o",
                "--source",
                "test_source",
                "run",
            ]
        )
    assert excinfo.value.code == 2

    args = parser.parse_args(
        [
            "--api-key",
            "test-key",
            "--address",
            "test://test.com",
            "--port",
            "90",
            "run",
            "--debug",
            "true",
            "--profile",
            "starter",
            "--model",
            "gpt-4o",
            "--source",
            "test_source",
        ]
    )
    result = check_run_args(args)
    assert isinstance(result, int)
    assert result == 1

    args = parser.parse_args(
        [
            "--api-key",
            "test-key",
            "--address",
            "test://test.com",
            "--port",
            "90",
            "run",
            "--debug",
            "true",
            "--profile",
            "starter",
            "--source",
            "test_source",
        ]
    )
    result = check_run_args(args)
    assert isinstance(result, argparse.Namespace)
    assert result.api_key == "test-key"
    assert result.command == "run"
    assert result.address == "test://test.com"
    assert result.port == 90
    assert result.debug is True
    assert result.profile == "starter"
    assert result.model is None
    assert result.source == os.path.join(os.getcwd(), "test_source")

    args = parser.parse_args(
        [
            "--api-key",
            "test-key",
            "--address",
            "test://test.com",
            "--port",
            "90",
            "run",
            "--debug",
            "true",
            "--model",
            "gpt-4o",
            "--source",
            "test_source",
        ]
    )
    result = check_run_args(args)
    assert isinstance(result, argparse.Namespace)
    assert result.api_key == "test-key"
    assert result.command == "run"
    assert result.address == "test://test.com"
    assert result.port == 90
    assert result.debug is True
    assert result.profile == "pro"
    assert result.model == "gpt-4o"
    assert result.source == os.path.join(os.getcwd(), "test_source")

    # Test without foundry.toml
    mock_exists.return_value = False
    args = parser.parse_args(
        [
            "--api-key",
            "test-key",
            "run",
        ]
    )
    result = check_run_args(args)
    assert isinstance(result, int)
    assert result == 1


def test_check_run_args_foundry():
    """Test run command argument validation"""
    parser = setup_parser()

    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "foundry.toml"), "w") as f:
            f.write("# Temporary foundry.toml")
            f.flush()

        args = parser.parse_args(
            [
                "--api-key",
                "test-key",
                "run",
                "--source",
                tmpdir,
            ]
        )

        result = check_run_args(args)
        assert isinstance(result, argparse.Namespace)
        assert result.command == "run"
        assert result.source == tmpdir

    # Test with foundry.toml in parent directory

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create parent dir with foundry.toml
        parent_dir = os.path.join(tmpdir, "parent")
        os.makedirs(parent_dir)
        with open(os.path.join(parent_dir, "foundry.toml"), "w") as f:
            f.write("# Parent foundry.toml")

        # Create child dir structure
        child_dir = os.path.join(parent_dir, "test_source", "child", "dir")
        os.makedirs(child_dir)

        args = parser.parse_args(
            [
                "--api-key",
                "test-key",
                "run",
                "--source",
                child_dir,
            ]
        )
        result = check_run_args(args)

        assert isinstance(result, argparse.Namespace)
        assert result.command == "run"
        assert result.source == parent_dir


@patch("hackbot.commands.get_selectable_models")
@patch("hackbot.commands.log.info")
def test_show_selectable_models(mock_logger, mock_get_selectable_models):
    """Test model listing functionality"""
    mock_get_selectable_models.return_value = ["model1", "model2", "model3"]

    args = MagicMock()
    args.address = "test://test.com"
    args.port = 90
    show_selectable_models(address=args.address, port=args.port, api_key=args.api_key)

    # Verify models were logged
    assert mock_logger.call_count > 0
    mock_logger.assert_any_call("Selectable models:")
    mock_logger.assert_any_call("  - model1")
    mock_logger.assert_any_call("  - model2")
    mock_logger.assert_any_call("  - model3")
