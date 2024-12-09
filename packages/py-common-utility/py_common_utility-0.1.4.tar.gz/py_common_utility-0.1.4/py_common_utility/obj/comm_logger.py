import logging
import inspect


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Get caller's filename and line number
        caller_frame = inspect.stack()[8]
        caller_filename = caller_frame.filename
        caller_line_number = caller_frame.lineno

        # Add caller information to the log record
        record.caller_filename = caller_filename
        record.caller_line_number = caller_line_number

        # Create the custom log message
        log_message = f"[{caller_filename}:{caller_line_number}] {record.getMessage()}"
        return log_message


def get_comm_logger(name: str) -> logging.Logger:
    """
    logger = get_comm_logger(__name__)
    """
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create a custom formatter
    formatter = CustomFormatter()

    # Add the formatter to the handler
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)
    return logger
