from typing import Dict, Any, List
import numpy as np

from ..interfaces.base import Strategy
from ..utils.config import config

class EnergyOptimizationStrategy(Strategy):
    """Strategy for optimizing energy consumption while maintaining comfort."""
    
    def __init__(self):
        """Initialize the energy optimization strategy."""
        self.optimization_target = config.get(
            "strategy.optimization_target",
            "energy_efficiency"
        )
        self.constraints = config.get("strategy.constraints", [])
        
        # Define comfort ranges
        self.comfort_temp_range = (20, 24)  # °C
        self.comfort_humidity_range = (30, 60)  # %
        
    def evaluate(self, state: Dict[str, Any]) -> float:
        """
        Evaluate current state based on energy efficiency and comfort constraints.
        Returns a score between 0 and 1, where 1 is optimal.
        """
        scores = []
        
        # Energy efficiency score
        if "energy_consumption" in state["devices"]:
            energy_score = self._evaluate_energy(state["devices"]["energy_consumption"])
            scores.append(energy_score)
        
        # Temperature comfort score
        if "temperature" in state["devices"]:
            temp_score = self._evaluate_temperature(state["devices"]["temperature"])
            scores.append(temp_score)
        
        # Humidity comfort score
        if "humidity" in state["devices"]:
            humidity_score = self._evaluate_humidity(state["devices"]["humidity"])
            scores.append(humidity_score)
        
        return np.mean(scores) if scores else 0.0
    
    def suggest(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest optimal action based on current state."""
        current_score = self.evaluate(state)
        
        if current_score >= 0.9:
            return {"action": "maintain"}
        
        # Example decision logic
        if "temperature" in state["devices"]:
            temp = state["devices"]["temperature"]
            if temp < self.comfort_temp_range[0]:
                return {"action": "heat", "target_temp": self.comfort_temp_range[0]}
            elif temp > self.comfort_temp_range[1]:
                return {"action": "cool", "target_temp": self.comfort_temp_range[1]}
        
        return {"action": "monitor"}
    
    def _evaluate_energy(self, consumption: float) -> float:
        """Evaluate energy consumption."""
        # Example: Higher score for lower consumption
        # Assuming consumption is in kWh and typical range is 0-5 kWh
        return max(0, 1 - (consumption / 5))
    
    def _evaluate_temperature(self, temperature: float) -> float:
        """Evaluate temperature comfort."""
        if self.comfort_temp_range[0] <= temperature <= self.comfort_temp_range[1]:
            return 1.0
        # Score decreases linearly outside comfort range
        if temperature < self.comfort_temp_range[0]:
            return max(0, 1 - (self.comfort_temp_range[0] - temperature) / 5)
        return max(0, 1 - (temperature - self.comfort_temp_range[1]) / 5)
    
    def _evaluate_humidity(self, humidity: float) -> float:
        """Evaluate humidity comfort."""
        if self.comfort_humidity_range[0] <= humidity <= self.comfort_humidity_range[1]:
            return 1.0
        # Score decreases linearly outside comfort range
        if humidity < self.comfort_humidity_range[0]:
            return max(0, 1 - (self.comfort_humidity_range[0] - humidity) / 15)
        return max(0, 1 - (humidity - self.comfort_humidity_range[1]) / 15)
