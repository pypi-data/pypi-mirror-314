import unittest

from checkout.mixins.logger import Logger


class LoggerTest(unittest.TestCase):

    def setUp(self):
        """
        Create a new Logger instance for testing.
        """
        self.logger = Logger()

    def test_log_debug(self):
        """
        Test logging a debug-level message.
        """
        with self.assertLogs("P2PLogger", level="DEBUG") as log:
            self.logger.debug("Debug message", {"key": "value"})
        self.assertIn("(P2P Checkout) Debug message - Context: {'key': 'value'}", log.output[0])

    def test_log_info(self):
        """
        Test logging an info-level message.
        """
        with self.assertLogs("P2PLogger", level="INFO") as log:
            self.logger.info("Info message", {"key": "value"})
        self.assertIn("(P2P Checkout) Info message - Context: {'key': 'value'}", log.output[0])

    def test_log_warning(self):
        """
        Test logging a warning-level message.
        """
        with self.assertLogs("P2PLogger", level="WARNING") as log:
            self.logger.warning("Warning message", {"key": "value"})
        self.assertIn("(P2P Checkout) Warning message - Context: {'key': 'value'}", log.output[0])

    def test_log_error(self):
        """
        Test logging an error-level message.
        """
        with self.assertLogs("P2PLogger", level="ERROR") as log:
            self.logger.error("Error message", {"key": "value"})
        self.assertIn("(P2P Checkout) Error message - Context: {'key': 'value'}", log.output[0])

    def test_log_critical(self):
        """
        Test logging a critical-level message.
        """
        with self.assertLogs("P2PLogger", level="CRITICAL") as log:
            self.logger.critical("Critical message", {"key": "value"})
        self.assertIn("(P2P Checkout) Critical message - Context: {'key': 'value'}", log.output[0])

    def test_log_invalid_level(self):
        """
        Test logging with an invalid level (defaults to `info`).
        """
        with self.assertLogs("P2PLogger", level="INFO") as log:
            self.logger.log("invalid", "Invalid level message", {"key": "value"})
        self.assertIn("(P2P Checkout) Invalid level message - Context: {'key': 'value'}", log.output[0])

    def test_clean_context_with_valid_dict(self):
        """
        Test clean_up method with a valid dictionary.
        """
        context = {"key": "value"}
        cleaned_context = self.logger._clean_context(context)
        self.assertEqual(cleaned_context, context)

    def test_clean_context_with_none(self):
        """
        Test clean_up method with None as input.
        """
        cleaned_context = self.logger._clean_context(None)
        self.assertEqual(cleaned_context, {})

    def test_clean_context_with_invalid_type(self):
        """
        Test clean_up method with an invalid type (not a dict).
        """
        cleaned_context = self.logger._clean_context("invalid")
        self.assertEqual(cleaned_context, {})

    def test_dynamic_methods(self):
        """
        Test dynamically created logging methods (e.g., debug, info, etc.).
        """
        with self.assertLogs("P2PLogger", level="DEBUG") as log:
            self.logger.debug("Dynamically created debug method", {"key": "value"})
        self.assertIn("(P2P Checkout) Dynamically created debug method - Context: {'key': 'value'}", log.output[0])

    def test_invalid_dynamic_method(self):
        """
        Test accessing an invalid dynamic method raises an AttributeError.
        """
        with self.assertRaises(AttributeError):
            self.logger.invalid_method("This should fail")
