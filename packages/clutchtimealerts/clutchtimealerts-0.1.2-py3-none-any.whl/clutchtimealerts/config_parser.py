from clutchtimealerts.db_utils import TABLE_NAME
import yaml
import logging

logger = logging.getLogger("clutchtimealerts")


class ConfigParser:
    def __init__(
        self,
        config_path: str = "config.yaml",
        classname_dict: dict = {},
        common_name_dict: dict = {},
    ) -> None:
        self.config_path = config_path
        self.classname_dict = classname_dict
        self.common_name_dict = common_name_dict

    def parse_config(self) -> None:
        # Parse YAML Config
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)

        # Parse database file path
        self.db_file_path = config.get("db_file_path", "clutchtime.db")
        self.db_table_name = config.get("db_table_name", TABLE_NAME)

        notification_configs = config.get("notifications", [])
        self.notifications = []
        for notify_config in notification_configs:
            if "type" not in notify_config:
                raise ValueError("Notification type must be specified in config file")

            # Get YAML Config
            notifiction_type = notify_config["type"]
            class_config = notify_config["config"]

            # Check that notification type exists
            if notifiction_type in self.classname_dict:
                notification_class = self.classname_dict[notifiction_type]
            elif notifiction_type in self.common_name_dict:
                notification_class = self.common_name_dict[notifiction_type]
            else:
                logger.warning(
                    f"Unknown notification type: {notifiction_type} ... skipping"
                )
                continue

            # Instatiate Notification
            try:
                notification_instance = notification_class(**class_config)
            except Exception as e:
                logger.warning(
                    f"Failed to create notification of type {notifiction_type}: {e} ... skipping"
                )
                continue

            self.notifications.append(notification_instance)

        if len(self.notifications) == 0:
            raise ValueError("No notifications found in config file")
