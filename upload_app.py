import os
import time

import redis

from slack_progress_bar import SlackProgressBar

USER_0 = os.getenv("USER_0")
USER_1 = os.getenv("USER_1")
BOT_TOKEN = os.getenv("BOT_TOKEN")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


class SlackManager:

    def __init__(self, token: str, user_id: str) -> None:
        """A manager that manages messages to Slack instance.

        Parameters
        ----------
        token
            The Slack bot token.
        user_id
            The user id of the slack member to send messages to.
        """
        self.token = token
        self.user_id = user_id
        self.redis = redis.Redis(
            host=REDIS_HOST, password=REDIS_PASSWORD, decode_responses=True
        )

        self._curr_bar = None
        self._curr_total = 0

    @property
    def is_subscribed(self) -> bool:
        """Check if user is subscribed to messages.

        Returns
        -------
        bool
            If the user is subscribed or not.
        """
        key = f"{self.user_id}:subscribed"

        # Assume user is
        if (val := self.redis.get(key)) is None:
            print("Subscription not found. Default to subscribed.")
            self.redis.set(key, 1)
            return True

        return bool(int(val))

    def new_bar(self, total: int) -> None:
        """Create a new progress bar on Slack.

        Parameters
        ----------
        total
            The total size of the progress bar.
        """
        if self.is_subscribed:
            self._curr_bar = SlackProgressBar(self.token, self.user_id, total)
        else:
            self._curr_bar = None
        self._curr_total = total

    def update_bar(self, value: int) -> None:
        """Update the current progress bar on Slack.

        Parameters
        ----------
        value
            The value to set the progress bar.
        """
        if self.is_subscribed:
            if not self._curr_bar:
                self._curr_bar = SlackProgressBar(
                    self.token, self.user_id, self._curr_total
                )
            self._curr_bar.update(value)


class UploadApp:

    def __init__(self, slack_manager: SlackManager) -> None:
        """A dummy app that fakes data upload and sends progress to Slack.

        Parameters
        ----------
        slack_manager
            The manager used to interface with Slack.
        """
        self.slack_manager = slack_manager

    def run(self) -> None:
        """Run the upload app."""
        while p := input("Enter how many files to upload (q to quit): "):
            if p == "q" or p == "0":
                break
            elif not p.isnumeric():
                print("Enter valid number!")
            else:
                self.upload(int(p))

    def upload(self, n_files: int) -> None:
        """Upload the number of files.

        Parameters
        ----------
        n_files
            The number of files to upload.
        """
        data_uploaded = 0
        self.slack_manager.new_bar(total=n_files)
        while data_uploaded != n_files:
            time.sleep(0.5)  # Upload time
            data_uploaded += 1
            self.slack_manager.update_bar(value=data_uploaded)


if __name__ == "__main__":

    while True:
        user = input(
            "Which user is this (q to quit)?"
            "\n  0: USER_0"
            "\n  1: USER_1"
            "\n"
        )
        if user == "0":
            user_id = USER_0
        elif user == "1":
            user_id = USER_1
        elif user == "q":
            break
        else:
            print("Invalid selection!")
            continue

        if user_id is not None and BOT_TOKEN is not None:
            slack_manager = SlackManager(token=BOT_TOKEN, user_id=user_id)
            app = UploadApp(slack_manager)
            app.run()
        else:
            raise ValueError(
                "Must set USER_0, USER_1, and BOT_TOKEN env variables!"
            )
