import logging
from typing import Any, Callable, Dict, Optional, cast


class Logger:
    """
    A wrapper for logging with dynamic method handling for different log levels.
    """

    def __init__(self, logger: Optional[logging.Logger] = None) -> None:
        """
        Initialize the Logger instance.

        :param logger: An optional `logging.Logger` instance. If not provided, a default logger is created.
        """
        self.logger: logging.Logger = logger if logger else self._create_default_logger()

    def log(self, level: str, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a message with the specified level.

        :param level: Log level as a string (e.g., 'debug', 'info', etc.).
        :param message: The message to log.
        :param context: Additional context to include in the log.
        """
        log_func = self._get_log_func(level)
        cleaned_context = self._clean_context(context)
        log_func(f"(P2P Checkout) {message} - Context: {cleaned_context}")

    def _get_log_func(self, level: str) -> Callable[[str], None]:
        """
        Retrieve the logging function for the specified level.

        :param level: Log level as a string.
        :return: The logging function corresponding to the level, or `info` as fallback.
        """
        return getattr(self.logger, level.lower(), self.logger.info)

    def __getattr__(self, name: str) -> Callable[[str, Optional[Dict[str, Any]]], None]:
        """
        Dynamically handle logging methods like `debug`, `info`, etc.

        :param name: The name of the method being called.
        :return: A callable function that logs with the specified level.
        """
        if name in {"debug", "info", "warning", "error", "critical"}:
            return cast(
                Callable[[str, Optional[Dict[str, Any]]], None],
                lambda message, context=None: self.log(name, message, context),
            )
        raise AttributeError(f"'Logger' object has no attribute '{name}'")

    @staticmethod
    def _clean_context(context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Clean up the context by ensuring it's a dictionary.

        :param context: The context to clean up.
        :return: A cleaned dictionary (empty if input is None or invalid).
        """
        return context if isinstance(context, dict) else {}

    @staticmethod
    def _create_default_logger() -> logging.Logger:
        """
        Create and configure a default logger.

        :return: A `logging.Logger` instance.
        """
        logger = logging.getLogger("P2PLogger")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
