from unittest.mock import MagicMock, patch

import pytest

from echoes_menu_mod_gui import cli


@patch("echoes_menu_mod_gui.cli.qt.create_subparsers", autospec=True)
def test_create_subparsers(mock_qt_create_subparsers: MagicMock,
                           ):
    # Setup
    root_parser = MagicMock()

    # Run
    cli.create_subparsers(root_parser)

    # Asser
    mock_qt_create_subparsers.assert_called_once_with(root_parser)


@pytest.mark.parametrize("args", [
    [],
    ["--version"],
])
@patch("sys.exit", autospec=True)
def test_parse_args_valid(mock_exit: MagicMock,
                          args):
    # Run
    cli._create_parser().parse_args(args)

    # Assert
    mock_exit.assert_not_called()


@pytest.mark.parametrize("args", [
    ["-h"],
])
@patch("sys.exit", autospec=True)
def test_parse_args_invalid(mock_exit: MagicMock,
                            args):
    # Run
    parser = cli._create_parser()
    parser.parse_args(args)

    # Assert
    mock_exit.assert_called_once_with(0)


@patch("echoes_menu_mod_gui.cli.qt.run", autospec=True)
def test_run_args_no_option(mock_qt_run: MagicMock,
                            ):
    # Setup
    args = MagicMock()
    args.func = None

    # Run
    cli._run_args(args)

    # Assert
    mock_qt_run.assert_called_once_with(args)


def test_run_args_with_func():
    # Setup
    args = MagicMock()

    # Run
    cli._run_args(args)

    # Assert
    args.func.assert_called_once_with(args)


@patch("echoes_menu_mod_gui.cli._run_args", autospec=True)
@patch("echoes_menu_mod_gui.cli._create_parser", autospec=True)
def test_run_cli(mock_create_parser: MagicMock,
                 mock_run_args: MagicMock,
                 ):
    # Setup
    argv = [MagicMock(), MagicMock(), MagicMock()]

    # Run
    cli.run_cli(argv)

    # Assert
    mock_create_parser.return_value.parse_args.assert_called_once_with(argv[1:])
    mock_run_args.assert_called_once_with(mock_create_parser.return_value.parse_args.return_value)
