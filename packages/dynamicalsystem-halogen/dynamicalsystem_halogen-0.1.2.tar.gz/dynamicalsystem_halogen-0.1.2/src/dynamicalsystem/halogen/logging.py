from dynamicalsystem.halogen.config import config_instance
from datetime import datetime
from logging import getLogger, Handler, Formatter, StreamHandler, INFO, WARNING
from requests import post, ConnectionError
from sys import stdout

config = config_instance(__name__)


class SignalHandler(Handler):
    def emit(self, record):
        headers = {"Content-Type": "application/json"}
        message = self.format(record)
        data = {
            "message": message,
            "number": config.log_signal_identity,
            "recipients": [config.log_signal_target],
        }

        try:
            response = post(config.log_signal_url, json=data, headers=headers)
        except ConnectionError as e:
            print(f"Failed to connect to Signal Messenger: {e}")
            return

        # TODO: give this access to the console logger
        if not response.ok:
            error = response.json().get("error")
            print("Failed to log to Signal Messenger: %", error.split("\n")[0])

        return response


class SignalFormatter(Formatter):
    def format(self, record):
        return (
            f"{record.levelname} "
            f"{record.name}\n"
            f'{datetime.fromtimestamp(record.created).strftime("%d %b %Y, %H:%M:%S")}\n'
            f"{record.msg}"
        )


# TODO: work out why this doesn't show in docker log (although root does)
def create_logger():
    logger = getLogger()

    logger.addHandler(_console_handler())
    logger.addHandler(_signal_handler())
    logger.setLevel(getattr(config, "log_level", INFO))

    logger.debug("Logger created")

    return logger


def _console_handler() -> StreamHandler:
    handler = StreamHandler(stdout)
    handler.setLevel(getattr(config, "log_level", INFO))
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    return handler


# TODO: Work out how to trigger this with context
def _signal_handler() -> SignalHandler:
    handler = SignalHandler()
    handler.setLevel(WARNING)
    handler.setFormatter(SignalFormatter())

    return handler
