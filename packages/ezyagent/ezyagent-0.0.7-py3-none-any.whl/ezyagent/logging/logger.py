import json
import logging
import sys
import time
import uuid
from contextlib import contextmanager
from copy import deepcopy
from typing import Any, Dict, Generator, Optional, Union

import structlog
from rich.console import Console
from rich.logging import RichHandler
from tabulate import tabulate


class LogContext:
    """Context for storing log-related data."""

    def __init__(self) -> None:
        self.context: Dict[str, Any] = {}
        self.correlation_id: Optional[str] = None

    def set(self, key: str, value: Any) -> None:
        """Set a context value."""
        self.context[key] = value

    def get(self, key: str) -> Any:
        """Get a context value."""
        return self.context.get(key)

    def clear(self) -> None:
        """Clear all context data."""
        self.context.clear()
        self.correlation_id = None


class Span:
    """Represents a logging span for tracking operations."""

    def __init__(self, logger: 'AgentLogger', name: str):
        self.logger = logger
        self.name = name
        self.start_time = time.time()
        self.tags: Dict[str, Any] = {}

    def set_tag(self, key: str, value: Any) -> None:
        """Set a tag for this span."""
        self.tags[key] = value

    def finish(self) -> None:
        """Complete the span and log its duration."""
        duration = time.time() - self.start_time
        message = self.tags.get("message", "")
        log_tags = deepcopy(self.tags)
        if 'message' in log_tags:
            log_tags.pop("message")
        self.logger.info(
            message=message,
            duration=f"{duration:.2f}s",
            **log_tags
        )


class AgentLogger:
    """Main logging class with tabulated formatting and structured logging."""

    def __init__(
        self,
        level: str = "INFO",
        format: str = "rich",
        outputs: Optional[list[str]] = None,
        correlation_id: Optional[str] = None
    ):
        self.context = LogContext()
        self.context.correlation_id = correlation_id or str(uuid.uuid4())
        self.console = Console(force_terminal=True)

        # Configure logging based on format
        if format == "json":
            self._setup_json_logging()
        else:
            self._setup_rich_logging()

        # Set log level
        logging.getLogger().setLevel(getattr(logging, level.upper()))
        self.logger = structlog.get_logger()

        # Setup additional outputs
        if outputs:
            self._setup_outputs(outputs)

    def _setup_rich_logging(self) -> None:
        """Setup rich logging with tabulated formatting."""
        logging.basicConfig(
            level="INFO",
            format="%(message)s",
            datefmt="%H:%M:%S",
            handlers=[RichHandler(
                rich_tracebacks=True,
                markup=True,
                show_path=False,
                show_time=False,  # We'll handle time in our table
                omit_repeated_times=True
            )]
        )

        structlog.configure(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt="%H:%M:%S"),
                self._format_message_processor,
                structlog.dev.ConsoleRenderer(
                    colors=True,
                    exception_formatter=structlog.dev.plain_traceback,
                    pad_event=0
                )
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    def _format_message_processor(
        self,
        logger: Any,
        name: str,
        event_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Format log events into tabulated output."""
        time_str = event_dict.get("timestamp", "")
        message = event_dict.get("event", "")
        duration = event_dict.get("duration", "")
        conv_id = self.context.correlation_id[:8]

        # Build table data
        headers = ["Time", "ID", "Message", "Duration"]
        table_data = [[time_str, conv_id, message, duration]]

        # Create table with clean formatting
        table = tabulate(
            table_data,
            headers=headers,
            tablefmt="simple",
            numalign="left",
            maxcolwidths=[10, 8, None, 10]
        )

        event_dict["event"] = "\n" + table
        return event_dict

    def _setup_json_logging(self) -> None:
        """Setup JSON structured logging."""
        structlog.configure(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    def _setup_outputs(self, outputs: list[str]) -> None:
        """Setup additional logging outputs."""
        for output in outputs:
            if output == "file":
                handler = logging.FileHandler("agent.log")
                handler.setFormatter(logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                ))
                logging.getLogger().addHandler(handler)

    @contextmanager
    def span(self, name: str) -> Generator[Span, None, None]:
        """Create a logging span for tracking operations."""
        span = Span(self, name)
        try:
            yield span
        finally:
            span.finish()

    def bind(self, **kwargs: Any) -> None:
        """Bind context values to all future log entries."""
        for key, value in kwargs.items():
            self.context.set(key, value)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        self.logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        self.logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        self.logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        self.logger.error(message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message."""
        self.logger.critical(message, **kwargs)