import datetime
import json
from typing import Any, Dict


class BaseFormatter:
    """Base class for log formatters."""

    def format(self, record: Dict[str, Any]) -> str:
        """Format the log record."""
        raise NotImplementedError


class JSONFormatter(BaseFormatter):
    """Format logs as JSON."""

    def format(self, record: Dict[str, Any]) -> str:
        """Format the log record as JSON."""
        output = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "level": record.get("level", "NOTSET"),
            "message": record.get("event"),
            "correlation_id": record.get("correlation_id"),
        }

        # Add any additional context
        context = {
            k: v for k, v in record.items()
            if k not in ["level", "event", "correlation_id"]
        }
        if context:
            output["context"] = context

        return json.dumps(output)


class PrettyFormatter(BaseFormatter):
    """Format logs in a human-readable format."""

    def format(self, record: Dict[str, Any]) -> str:
        """Format the log record in a pretty format."""
        timestamp = datetime.datetime.utcnow().isoformat()
        level = record.get("level", "NOTSET")
        message = record.get("event", "")
        correlation_id = record.get("correlation_id", "")

        # Format the base message
        output = f"[{timestamp}] {level:8} {message}"

        # Add correlation ID if present
        if correlation_id:
            output = f"{output} (correlation_id: {correlation_id})"

        # Add any additional context
        context = {
            k: v for k, v in record.items()
            if k not in ["level", "event", "correlation_id"]
        }
        if context:
            output = f"{output}\nContext: {json.dumps(context, indent=2)}"

        return output