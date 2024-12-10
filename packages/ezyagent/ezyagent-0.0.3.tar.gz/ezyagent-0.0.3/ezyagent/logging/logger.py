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


class LogContext:
    """Context for storing log-related data."""

    def __init__(self) -> None:
        self.context: Dict[str, Any] = {}
        self.correlation_id: Optional[str] = None

    def set(self, key: str, value: Any) -> None:
        self.context[key] = value

    def get(self, key: str) -> Any:
        return self.context.get(key)

    def clear(self) -> None:
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
        self.tags[key] = value

    def finish(self) -> None:
        duration = time.time() - self.start_time
        message = self.tags.get("message", "")
        log_tags = deepcopy(self.tags)
        if 'message' in log_tags:
            log_tags.pop("message")
        self.logger.info(message, duration=f"{duration:.3f}s", **log_tags)


class AgentLogger:
    """Main logging class with clean formatting and structured logging."""

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

        if format == "json":
            self._setup_json_logging()
        else:
            self._setup_rich_logging()

        logging.getLogger().setLevel(getattr(logging, level.upper()))
        self.logger = structlog.get_logger()

        if outputs:
            self._setup_outputs(outputs)

    def _setup_rich_logging(self) -> None:
        logging.basicConfig(
            level="INFO",
            format="%(message)s",
            handlers=[RichHandler(
                rich_tracebacks=True,
                markup=True,
                show_path=False,
                show_time=True,
                omit_repeated_times=True,
                log_time_format="%H:%M:%S"
            )]
        )

        structlog.configure(
            processors=[
                self._clean_event_processor,
                structlog.processors.TimeStamper(fmt="%H:%M:%S"),
                self._add_context_processor,
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

    def _clean_event_processor(
        self,
        logger: Any,
        name: str,
        event_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Clean up message content
        if 'event' in event_dict:
            msg = str(event_dict['event'])
            if isinstance(msg, str):
                msg = ' '.join(msg.split())
                if len(msg) > 100:  # Truncate very long messages
                    msg = msg[:97] + "..."
                event_dict['event'] = msg

        # Remove verbose fields
        for field in ['logger', 'level', 'logger_name']:
            event_dict.pop(field, None)

        return event_dict

    def _add_context_processor(
        self,
        logger: Any,
        name: str,
        event_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        if self.context.correlation_id:
            event_dict["id"] = self.context.correlation_id[:8]

        # Only add essential context
        essential_fields = {'user_id', 'session_id', 'request_id'}
        context = {
            k: v for k, v in self.context.context.items()
            if k in essential_fields
        }
        event_dict.update(context)
        return event_dict

    def _setup_json_logging(self) -> None:
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                self._clean_event_processor,
                self._add_context_processor,
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    def _setup_outputs(self, outputs: list[str]) -> None:
        for output in outputs:
            if output == "file":
                handler = logging.FileHandler("agent.log")
                handler.setFormatter(logging.Formatter(
                    '%(asctime)s [%(levelname)s] %(message)s'
                ))
                logging.getLogger().addHandler(handler)

    @contextmanager
    def span(self, name: str) -> Generator[Span, None, None]:
        span = Span(self, name)
        try:
            yield span
        finally:
            span.finish()

    def bind(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            self.context.set(key, value)

    def debug(self, message: str, **kwargs: Any) -> None:
        self.logger.debug(message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        self.logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        self.logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        self.logger.error(message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        self.logger.critical(message, **kwargs)