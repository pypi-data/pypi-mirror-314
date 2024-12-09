"""Data model to represent state of a CCM21 device."""
from dataclasses import dataclass
from . import CCM21SlaveDevice

@dataclass
class CCM21DeviceState:
    """Data retrieved from a CCM21 device."""

    devices: dict[int, CCM21SlaveDevice]
