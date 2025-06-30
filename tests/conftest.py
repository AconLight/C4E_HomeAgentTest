"""Shared pytest fixtures for all test modules."""

import pytest
from datetime import datetime
from typing import Dict, List
from core.interfaces.base import Device, DeviceData, SensorValue

class MockDevice(Device):
    """Mock device for testing."""
    
    def __init__(self, values: Dict[str, float], units: Dict[str, str]):
        self.values = values
        self.units = units
        self._metadata = {"type": "mock", "location": "test"}
    
    def read(self) -> Dict[str, float]:
        return self.values
    
    def get_metadata(self) -> Dict[str, Dict]:
        return self._metadata
    
    def get_value_types(self) -> List[str]:
        return list(self.values.keys())
    
    def get_units(self) -> Dict[str, str]:
        return self.units

@pytest.fixture
def mock_temp_device():
    """Temperature device fixture."""
    return MockDevice(
        values={"temperature": 22.5},
        units={"temperature": "celsius"}
    )

@pytest.fixture
def mock_power_device():
    """Power consumption device fixture."""
    return MockDevice(
        values={"power": 1.5, "voltage": 230.0, "current": 6.5},
        units={"power": "kW", "voltage": "V", "current": "A"}
    )

@pytest.fixture
def sample_device_data():
    """Sample device data fixture."""
    return {
        "temp_device": DeviceData(
            timestamp=datetime.now(),
            device_id="temp_device",
            values={
                "temperature": SensorValue(
                    value=22.5,
                    unit="celsius",
                    value_type="temperature",
                    metadata={"precision": 0.1}
                )
            },
            metadata={"location": "living_room"}
        ),
        "power_device": DeviceData(
            timestamp=datetime.now(),
            device_id="power_device",
            values={
                "power": SensorValue(
                    value=1.5,
                    unit="kW",
                    value_type="power",
                    metadata={"phase": "total"}
                ),
                "voltage": SensorValue(
                    value=230.0,
                    unit="V",
                    value_type="voltage",
                    metadata={}
                )
            },
            metadata={"device": "main_meter"}
        )
    }
