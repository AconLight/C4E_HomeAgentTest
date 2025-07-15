from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SensorValue:
    """Single value reading from a device with its metadata."""
    value: float
    unit: str
    value_type: str  # e.g., "temperature", "humidity", "power"
    metadata: Dict[str, Any]

@dataclass
class DeviceData:
    """Data structure for device readings and metadata."""
    timestamp: datetime
    device_id: str
    values: Dict[str, SensorValue]  # key is value_type
    metadata: Dict[str, Any]

class Device(ABC):
    """Base interface for all devices in the system."""
    
    @abstractmethod
    def read(self) -> Dict[str, float]:
        """Read current sensor values.
        
        Returns:
            Dict mapping value_type to its current reading
        """
        pass
    
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Get sensor metadata."""
        pass
    
    @abstractmethod
    def get_value_types(self) -> List[str]:
        """Get list of value types this sensor provides."""
        pass
    
    @abstractmethod
    def get_units(self) -> Dict[str, str]:
        """Get mapping of value_type to its unit."""
        pass

class Agent(ABC):
    """Base interface for all agents in the system."""
    
    @abstractmethod
    def ask(self, prompt: str) -> str:
        """Ask agent."""
        pass

class Strategy(ABC):
    """Base interface for optimization strategies."""
    
    @abstractmethod
    def evaluate(self, state: Dict[str, DeviceData]) -> float:
        """Evaluate current state."""
        pass
    
    @abstractmethod
    def suggest(self, state: Dict[str, DeviceData]) -> Dict[str, Any]:
        """Suggest optimal action."""
        pass
