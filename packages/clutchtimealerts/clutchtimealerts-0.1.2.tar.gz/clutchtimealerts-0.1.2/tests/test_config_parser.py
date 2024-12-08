import pytest
from unittest.mock import patch, mock_open, MagicMock
from clutchtimealerts.config_parser import ConfigParser
from clutchtimealerts.notifications.base import Notification


class MockNotification(Notification):
    COMMON_NAME = "mock_notification"

    def __init__(self, *args, **kwargs):
        super().__init__()
        raise ImportError("Mocked import error")

    def send(self, message):
        pass


@pytest.fixture
def sample_config():
    """Fixture for a sample configuration YAML."""
    return """
    db_file_path: "test.db"
    db_table_name: "test_table"
    notifications:
      - type: email
        config:
          recipient: "test@example.com"
      - type: sms
        config:
          phone_number: "+123456789"
    """


@pytest.fixture
def classname_dict():
    """Fixture for mock classname dictionary."""
    return {
        "email": MagicMock(return_value="EmailNotificationInstance"),
        "sms": MagicMock(return_value="SMSNotificationInstance"),
        "mock_notification": MockNotification,
    }


@pytest.fixture
def common_name_dict():
    """Fixture for mock common name dictionary."""
    return {
        "text": MagicMock(return_value="TextNotificationInstance"),
    }


@patch("builtins.open", new_callable=mock_open)
@patch("yaml.safe_load")
def test_parse_config_valid_config(
    mock_yaml_load, mock_open_file, sample_config, classname_dict, common_name_dict
):
    """Test parsing a valid configuration file."""
    mock_yaml_load.return_value = {
        "db_file_path": "test.db",
        "db_table_name": "test_table",
        "notifications": [
            {"type": "email", "config": {"recipient": "test@example.com"}},
            {"type": "sms", "config": {"phone_number": "+123456789"}},
        ],
    }

    parser = ConfigParser(
        config_path="test_config.yaml",
        classname_dict=classname_dict,
        common_name_dict=common_name_dict,
    )
    parser.parse_config()

    # Check database path and table name
    assert parser.db_file_path == "test.db"
    assert parser.db_table_name == "test_table"

    # Check notifications
    assert len(parser.notifications) == 2
    assert classname_dict["email"].call_count == 1
    assert classname_dict["sms"].call_count == 1


@patch("builtins.open", new_callable=mock_open)
@patch("yaml.safe_load")
@patch("clutchtimealerts.config_parser.logger.warning")
def test_parse_config_invalid_notification_type(
    mock_warning,
    mock_yaml_load,
    mock_open_file,
    sample_config,
    classname_dict,
    common_name_dict,
):
    """Test config with invalid notification type."""
    mock_yaml_load.return_value = {
        "notifications": [
            {"type": "unknown_type", "config": {}},
        ],
    }

    parser = ConfigParser(
        config_path="test_config.yaml",
        classname_dict=classname_dict,
        common_name_dict=common_name_dict,
    )

    try:
        parser.parse_config()
    except ValueError:
        assert True
    except Exception:
        assert False

    # Check that no notifications are created
    assert len(parser.notifications) == 0

    # Check that the logger was called with a warning
    mock_warning.assert_called_with(
        "Unknown notification type: unknown_type ... skipping"
    )


@patch("builtins.open", new_callable=mock_open)
@patch("yaml.safe_load")
def test_parse_config_missing_notification_type(
    mock_yaml_load, mock_open_file, sample_config
):
    """Test config missing notification type."""
    mock_yaml_load.return_value = {
        "notifications": [
            {"config": {"recipient": "test@example.com"}},
        ],
    }

    parser = ConfigParser(config_path="test_config.yaml")

    with pytest.raises(
        ValueError, match="Notification type must be specified in config file"
    ):
        parser.parse_config()


@patch("builtins.open", new_callable=mock_open)
@patch("yaml.safe_load")
def test_parse_config_no_notifications(mock_yaml_load, mock_open_file):
    """Test config with no notifications."""
    mock_yaml_load.return_value = {}

    parser = ConfigParser(config_path="test_config.yaml")

    with pytest.raises(ValueError, match="No notifications found in config file"):
        parser.parse_config()


@patch("builtins.open", new_callable=mock_open)
@patch("yaml.safe_load")
@patch("clutchtimealerts.config_parser.logger.warning")
def test_parse_config_invalid_notification_config(
    mock_warning, mock_yaml_load, mock_open_file, classname_dict
):
    """Test config with invalid notification configuration."""
    # Simulate invalid configuration for notifications
    mock_yaml_load.return_value = {
        "notifications": [
            {
                "type": "mock_notification",
                "config": {"invalid_param": "value"},
            },  # Invalid config
        ],
    }

    parser = ConfigParser(config_path="test_config.yaml", classname_dict=classname_dict)

    # Call the method to parse the config
    try:
        parser.parse_config()
    except ValueError:
        assert True
    except Exception:
        assert False

    # Check that no notifications are created
    print(parser.notifications)
    assert len(parser.notifications) == 0

    # Check that the logger was called with the correct warning
    mock_warning.assert_any_call(
        "Failed to create notification of type mock_notification: Mocked import error ... skipping"
    )
