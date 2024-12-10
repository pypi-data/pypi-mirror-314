import logging
import sys
from typing import Any, Optional


class ConsoleHandler(logging.StreamHandler):
    """Handler for console output with color support."""

    def __init__(self, stream: Optional[Any] = None):
        super().__init__(stream or sys.stdout)
        self.colors = {
            'DEBUG': '\033[36m',  # Cyan
            'INFO': '\033[32m',  # Green
            'WARNING': '\033[33m',  # Yellow
            'ERROR': '\033[31m',  # Red
            'CRITICAL': '\033[41m',  # Red background
            'RESET': '\033[0m'  # Reset
        }

    def format(self, record: logging.LogRecord) -> str:
        """Format the record with colors."""
        if hasattr(record, 'color') and not record.color:
            return super().format(record)

        color = self.colors.get(record.levelname, '')
        reset = self.colors['RESET']

        formatted = super().format(record)
        return f"{color}{formatted}{reset}"


class FileHandler(logging.FileHandler):
    """Handler for file output with rotation support."""

    def __init__(
        self,
        filename: str,
        mode: str = 'a',
        encoding: Optional[str] = None,
        delay: bool = False,
        max_bytes: int = 1024 * 1024 * 10,  # 10MB
        backup_count: int = 5
    ):
        super().__init__(filename, mode, encoding, delay)
        self.max_bytes = max_bytes
        self.backup_count = backup_count

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a record with rotation support."""
        try:
            if self.should_rotate():
                self.do_rotation()
            super().emit(record)
        except Exception:
            self.handleError(record)

    def should_rotate(self) -> bool:
        """Check if log file should be rotated."""
        if not self.stream:
            return False

        try:
            self.stream.seek(0, 2)  # Seek to end of file
            size = self.stream.tell()
            return size >= self.max_bytes
        except (AttributeError, OSError):
            return False

    def do_rotation(self) -> None:
        """Perform log rotation."""
        if self.stream:
            self.stream.close()
            self.stream = None

        for i in range(self.backup_count - 1, 0, -1):
            sfn = f"{self.baseFilename}.{i}"
            dfn = f"{self.baseFilename}.{i + 1}"
            try:
                import os
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            except Exception:
                pass