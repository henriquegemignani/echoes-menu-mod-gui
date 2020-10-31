from unittest.mock import MagicMock, patch

from echoes_menu_mod_gui.interface_common import update_checker


@patch("echoes_menu_mod_gui.interface_common.update_checker._read_from_persisted", autospec=True)
def test_get_latest_version(mock_read_from_persisted: MagicMock,
                                 ):
    on_result = MagicMock()

    update_checker.get_latest_version(on_result)

    on_result.assert_called_once_with(
        mock_read_from_persisted.return_value.tag_name,
        mock_read_from_persisted.return_value.html_url
    )
