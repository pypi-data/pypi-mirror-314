"""Represents the 'capabilities' DAP event."""

from __future__ import annotations

from typing import Any

from .dap_event import DAPEvent


class CapabilitiesDAPEvent(DAPEvent):
    """Represents the 'capabilities' DAP event."""

    event_name = "capabilities"

    changes: dict[str, Any]

    def __init__(self, changes: dict[str, Any]) -> None:
        """Create a new 'capabilities' DAP event message.

        Args:
            changes (dict[str, Any]): The changes in the capabilities.
        """
        super().__init__()
        self.changes = changes

    def validate(self) -> None:
        """Validate the 'capabilities' DAP event message after creation."""

    def encode(self) -> dict[str, int]:
        """Encode the 'capabilities' DAP event message as a dictionary.

        Returns:
            dict[str, int]: The encoded 'capabilities' DAP event message.
        """
        d = super().encode()
        d["body"] = {
            "capabilities": self.changes,
        }
        return d
