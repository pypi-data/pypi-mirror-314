import time
import requests
import logging

from clutchtimealerts.scraper.live_scores import NBAScoreScraper
from clutchtimealerts.notifications.base import Notification
from clutchtimealerts.db_utils import (
    TABLE_NAME,
    EXPECTED_COLUMNS,
    check_and_recreate_table,
    clear_table,
    insert_game,
    check_alert_sent,
    update_alert_sent,
    check_overtime_alert_sent,
    update_overtime_number,
)

logger = logging.getLogger("clutchtimealerts")


class ClutchAlertsService:
    def __init__(
        self,
        notifications: list[Notification],
        db_path: str = "clutchtime.db",
        db_table_name: str = TABLE_NAME,
    ) -> None:
        self.scraper = NBAScoreScraper()
        self.notifications = notifications
        self.db_path = db_path
        self.db_table_name = db_table_name

    def send_clutch_alert(self, message) -> None:
        """
        Send the given message as notification.

        Parameters
        ----------
        message : str
            The message to send to notification.

        Returns
        -------
        None
        """
        logger.debug(f"Sending message: {message}")
        for notification in self.notifications:
            try:
                notification.send(message)
            except Exception as e:
                logger.error(
                    f"Error sending notification to {notification.__class__.__name__}: {e}"
                )

    def _get_minutes_from_clock(self, clock) -> int:
        """
        Extract the minutes from the given clock string.

        The clock string is expected to be in the format "PT{minutes}M{seconds}S"
        If the string is empty or not in this format, -1 is returned.

        Parameters
        ----------
        clock : str
            The clock string to extract the minutes from.

        Returns
        -------
        int
            The minutes if the string is in the correct format, otherwise -1.
        """
        try:
            return int(clock.split("PT")[1].split("M")[0])
        except Exception:
            return -1

    def isCluthTime(self, game: dict) -> bool:
        """
        Checks if the given game is in "clutch time" - the last five minutes of the fourth quarter
        or overtime with the point difference being five points or fewer.

        Parameters
        ----------
        game : dict
            The game data to check.

        Returns
        -------
        bool
            True if the game is in clutch time, otherwise False.
        """
        period = game["period"]
        homeTeamScore = game["homeTeam"]["score"]
        awayTeamScore = game["awayTeam"]["score"]
        clock = game["gameClock"]
        minutes = self._get_minutes_from_clock(clock)

        if period < 4:
            return False
        elif minutes == -1 or minutes >= 5:
            return False
        elif abs(homeTeamScore - awayTeamScore) > 5:
            return False

        return True

    def isOvertime(self, game: dict) -> bool:
        """
        Checks if the given game is in overtime.

        Parameters
        ----------
        game : dict
            The game data to check.

        Returns
        -------
        bool
            True if the game is in overtime, otherwise False.
        """
        return game["period"] > 4

    def run(self) -> None:
        """
        Run the ClutchAlertsService to continuously monitor NBA games and send alerts.

        This method initializes the database and enters an infinite loop to fetch
        live NBA games. It checks each game's status to determine if it is in "clutch time,"
        and sends alerts for such games. If there are no live games, it sleeps for 2 hours.

        Returns
        -------
        None
        """
        # Create the database
        check_and_recreate_table(self.db_path, self.db_table_name, EXPECTED_COLUMNS)
        while True:
            # Fetch live games
            try:
                games = self.scraper.live_games()
                logger.info(f"Fetched {len(games)} live games")
            except requests.exceptions.ConnectionError:
                logger.error("Failed to fetch live games. Retrying...")
                time.sleep(60)
                continue

            # Iterate through each live game and send alert
            for game in games:
                gameId = game["gameId"]
                homeTeam = game["homeTeam"]["teamTricode"]
                awayTeam = game["awayTeam"]["teamTricode"]
                homeTeamScore = game["homeTeam"]["score"]
                awayTeamScore = game["awayTeam"]["score"]
                if self.isOvertime(game):
                    watch_link = f"https://www.nba.com/game/{awayTeam}-vs-{homeTeam}-{gameId}?watchLive=true"
                    overtime_number = game["period"] - 4
                    logger.info(
                        f"Overtime Game detected: OT{overtime_number} {awayTeam} v {homeTeam} - checking db"
                    )
                    if not check_overtime_alert_sent(
                        self.db_path,
                        self.db_table_name,
                        game["gameId"],
                        overtime_number,
                    ):
                        logger.info(
                            f"Alerting for Overtime Game: OT{overtime_number} {awayTeam} v {homeTeam}"
                        )
                        self.send_clutch_alert(
                            f"""OT{overtime_number} Alert\n{homeTeam} {homeTeamScore} - {awayTeamScore} {awayTeam}\n{watch_link}"""
                        )
                        # Update both tables
                        update_overtime_number(
                            self.db_path, self.db_table_name, game["gameId"]
                        )
                        update_alert_sent(
                            self.db_path, self.db_table_name, game["gameId"]
                        )
                elif self.isCluthTime(game):
                    watch_link = f"https://www.nba.com/game/{awayTeam}-vs-{homeTeam}-{gameId}?watchLive=true"
                    logger.info(
                        f"Clutch Game detected: {awayTeam} v {homeTeam} - checking db"
                    )
                    if not check_alert_sent(
                        self.db_path, self.db_table_name, game["gameId"]
                    ):
                        insert_game(self.db_path, self.db_table_name, game["gameId"])
                        logger.info(
                            f"Alerting for Clutch Game: {awayTeam} v {homeTeam}"
                        )
                        self.send_clutch_alert(
                            f"""Clutch Game\n{homeTeam} {homeTeamScore} - {awayTeamScore} {awayTeam}\n{watch_link}"""
                        )
                        update_alert_sent(
                            self.db_path, self.db_table_name, game["gameId"]
                        )

            # Sleep for 2 hours if there are no live games
            if len(games) == 0:
                logger.info("No live games. Sleeping for 2 hours...")
                clear_table(self.db_path, self.db_table_name)
                time.sleep(7200)
            # Otherwise sleep for 30 seconds
            else:
                time.sleep(15)
