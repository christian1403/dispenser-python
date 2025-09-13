"""
Calibration Service for handling sensor calibration operations
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)


class CalibrationService:
    """Service class for handling sensor calibration operations"""
    
    def __init__(self):
        """Initialize the calibration service with default calibration parameters"""
        # ESP32 specifications
        self.ESP32_MAX_VOLTAGE = 3.3  # ESP32 reference voltage
        self.ESP32_ADC_RESOLUTION = 4095  # ESP32 12-bit ADC (2^12 - 1)
        
        # Default calibration parameters - these would typically be stored in database
        # and retrieved/updated through configuration management
        self._calibration_params = {
            'ph': {
                'slope': 3.5,  # pH per volt
                'intercept': 7.0,  # pH at neutral voltage (1.65V for 3.3V system)
                'min_value': 0.0,
                'max_value': 14.0,
                'neutral_adc': 2048  # ADC value at pH 7 (approximately 1.65V)
            },
            'tds': {
                'slope': 500.0,  # PPM per volt
                'intercept': 0.0,  # PPM at 0V
                'min_value': 0.0,
                'max_value': 2000.0,  # Adjusted for 3.3V system
                'compensation_temp': 25.0  # Temperature compensation reference
            },
            'turbidity': {
                'slope': -1000.0,  # NTU per volt (negative because higher voltage = lower turbidity)
                'intercept': 3000.0,  # NTU at 0V
                'min_value': 0.0,
                'max_value': 3000.0,
                'clear_water_adc': 3000  # ADC value for clear water
            }
        }
    
    def adc_to_voltage(self, adc_value: int) -> float:
        """
        Convert ESP32 ADC value to voltage
        
        Args:
            adc_value: ADC reading from ESP32 (0-4095)
            
        Returns:
            Voltage value (0-3.3V)
        """
        if adc_value < 0 or adc_value > self.ESP32_ADC_RESOLUTION:
            raise ValueError(f"ADC value must be between 0 and {self.ESP32_ADC_RESOLUTION}")
        
        voltage = (adc_value / self.ESP32_ADC_RESOLUTION) * self.ESP32_MAX_VOLTAGE
        return round(voltage, 4)
    
    def calibrate_ph(self, raw_value: float) -> Dict[str, Any]:
        """
        Calibrate pH sensor raw value to actual pH value
        
        Args:
            raw_value: Raw ADC value from ESP32 pH sensor (0-4095) or voltage (0-3.3V)
            
        Returns:
            Dictionary containing calibrated pH value and metadata
            
        Raises:
            ValueError: If raw_value is invalid
        """
        try:
            if not isinstance(raw_value, (int, float)):
                raise ValueError("Raw value must be a number")
            
            # Determine if input is ADC value or voltage
            if raw_value > self.ESP32_MAX_VOLTAGE:
                # Input is ADC value
                if raw_value < 0 or raw_value > self.ESP32_ADC_RESOLUTION:
                    raise ValueError(f"ADC value must be between 0 and {self.ESP32_ADC_RESOLUTION}")
                voltage = self.adc_to_voltage(int(raw_value))
                adc_value = int(raw_value)
            else:
                # Input is voltage
                if raw_value < 0 or raw_value > self.ESP32_MAX_VOLTAGE:
                    raise ValueError(f"Voltage must be between 0 and {self.ESP32_MAX_VOLTAGE}V")
                voltage = raw_value
                adc_value = int((voltage / self.ESP32_MAX_VOLTAGE) * self.ESP32_ADC_RESOLUTION)
            
            params = self._calibration_params['ph']
            
            # pH calibration formula adjusted for ESP32
            # pH = slope * (voltage - neutral_voltage) + neutral_pH
            neutral_voltage = (params['neutral_adc'] / self.ESP32_ADC_RESOLUTION) * self.ESP32_MAX_VOLTAGE
            ph_value = params['slope'] * (voltage - neutral_voltage) + 7.0
            
            # Clamp to valid pH range
            ph_value = max(params['min_value'], min(params['max_value'], ph_value))
            
            return {
                'value': round(ph_value, 2),
                'unit': 'pH',
                'raw_value': raw_value,
                'adc_value': adc_value,
                'voltage': voltage,
                'calibration_timestamp': datetime.utcnow().isoformat(),
                'sensor_type': 'ph',
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error calibrating pH value {raw_value}: {str(e)}")
            return {
                'value': None,
                'unit': 'pH',
                'raw_value': raw_value,
                'error': str(e),
                'sensor_type': 'ph',
                'status': 'error'
            }
    
    def calibrate_tds(self, raw_value: float) -> Dict[str, Any]:
        """
        Calibrate TDS sensor raw value to actual PPM value
        
        Args:
            raw_value: Raw ADC value from ESP32 TDS sensor (0-4095) or voltage (0-3.3V)
            
        Returns:
            Dictionary containing calibrated TDS value in PPM and metadata
            
        Raises:
            ValueError: If raw_value is invalid
        """
        try:
            if not isinstance(raw_value, (int, float)):
                raise ValueError("Raw value must be a number")
            
            # Determine if input is ADC value or voltage
            if raw_value > self.ESP32_MAX_VOLTAGE:
                # Input is ADC value
                if raw_value < 0 or raw_value > self.ESP32_ADC_RESOLUTION:
                    raise ValueError(f"ADC value must be between 0 and {self.ESP32_ADC_RESOLUTION}")
                voltage = self.adc_to_voltage(int(raw_value))
                adc_value = int(raw_value)
            else:
                # Input is voltage
                if raw_value < 0 or raw_value > self.ESP32_MAX_VOLTAGE:
                    raise ValueError(f"Voltage must be between 0 and {self.ESP32_MAX_VOLTAGE}V")
                voltage = raw_value
                adc_value = int((voltage / self.ESP32_MAX_VOLTAGE) * self.ESP32_ADC_RESOLUTION)
            
            params = self._calibration_params['tds']
            
            # TDS calibration formula for ESP32
            # TDS (PPM) = slope * voltage + intercept
            # Temperature compensation can be added here if needed
            tds_ppm = params['slope'] * voltage + params['intercept']
            
            # Clamp to valid TDS range
            tds_ppm = max(params['min_value'], min(params['max_value'], tds_ppm))
            
            return {
                'value': round(tds_ppm, 1),
                'unit': 'ppm',
                'raw_value': raw_value,
                'adc_value': adc_value,
                'voltage': voltage,
                'calibration_timestamp': datetime.utcnow().isoformat(),
                'sensor_type': 'tds',
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error calibrating TDS value {raw_value}: {str(e)}")
            return {
                'value': None,
                'unit': 'ppm',
                'raw_value': raw_value,
                'error': str(e),
                'sensor_type': 'tds',
                'status': 'error'
            }
    
    def calibrate_turbidity(self, raw_value: float) -> Dict[str, Any]:
        """
        Calibrate turbidity sensor raw value to actual NTU value
        
        Args:
            raw_value: Raw ADC value from ESP32 turbidity sensor (0-4095) or voltage (0-3.3V)
            
        Returns:
            Dictionary containing calibrated turbidity value in NTU and metadata
            
        Raises:
            ValueError: If raw_value is invalid
        """
        try:
            if not isinstance(raw_value, (int, float)):
                raise ValueError("Raw value must be a number")
            
            # Determine if input is ADC value or voltage
            if raw_value > self.ESP32_MAX_VOLTAGE:
                # Input is ADC value
                if raw_value < 0 or raw_value > self.ESP32_ADC_RESOLUTION:
                    raise ValueError(f"ADC value must be between 0 and {self.ESP32_ADC_RESOLUTION}")
                voltage = self.adc_to_voltage(int(raw_value))
                adc_value = int(raw_value)
            else:
                # Input is voltage
                if raw_value < 0 or raw_value > self.ESP32_MAX_VOLTAGE:
                    raise ValueError(f"Voltage must be between 0 and {self.ESP32_MAX_VOLTAGE}V")
                voltage = raw_value
                adc_value = int((voltage / self.ESP32_MAX_VOLTAGE) * self.ESP32_ADC_RESOLUTION)
            
            params = self._calibration_params['turbidity']
            
            # Turbidity calibration formula for ESP32
            # For most turbidity sensors, higher voltage = clearer water (lower NTU)
            # NTU = slope * voltage + intercept
            turbidity_ntu = params['slope'] * voltage + params['intercept']
            
            # Clamp to valid turbidity range
            turbidity_ntu = max(params['min_value'], min(params['max_value'], turbidity_ntu))
            
            return {
                'value': round(turbidity_ntu, 1),
                'unit': 'NTU',
                'raw_value': raw_value,
                'adc_value': adc_value,
                'voltage': voltage,
                'calibration_timestamp': datetime.utcnow().isoformat(),
                'sensor_type': 'turbidity',
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Error calibrating turbidity value {raw_value}: {str(e)}")
            return {
                'value': None,
                'unit': 'NTU',
                'raw_value': raw_value,
                'error': str(e),
                'sensor_type': 'turbidity',
                'status': 'error'
            }
    
    def calibrate_sensor_value(self, sensor_type: str, raw_value: float) -> Dict[str, Any]:
        """
        Generic method to calibrate any supported sensor type
        
        Args:
            sensor_type: Type of sensor ('ph', 'tds', 'turbidity')
            raw_value: Raw voltage value from sensor
            
        Returns:
            Dictionary containing calibrated value and metadata
            
        Raises:
            ValueError: If sensor_type is not supported
        """
        sensor_type = sensor_type.lower()
        
        if sensor_type == 'ph':
            return self.calibrate_ph(raw_value)
        elif sensor_type == 'tds':
            return self.calibrate_tds(raw_value)
        elif sensor_type == 'turbidity':
            return self.calibrate_turbidity(raw_value)
        else:
            raise ValueError(f"Unsupported sensor type: {sensor_type}")
    
    def update_calibration_params(self, sensor_type: str, params: Dict[str, float]) -> bool:
        """
        Update calibration parameters for a sensor type
        
        Args:
            sensor_type: Type of sensor ('ph', 'tds', 'turbidity')
            params: Dictionary containing calibration parameters
            
        Returns:
            True if update successful, False otherwise
        """
        try:
            sensor_type = sensor_type.lower()
            
            if sensor_type not in self._calibration_params:
                raise ValueError(f"Unsupported sensor type: {sensor_type}")
            
            # Validate required parameters
            required_params = ['slope', 'intercept', 'min_value', 'max_value']
            for param in required_params:
                if param not in params:
                    raise ValueError(f"Missing required parameter: {param}")
                if not isinstance(params[param], (int, float)):
                    raise ValueError(f"Parameter {param} must be a number")
            
            # Update parameters
            self._calibration_params[sensor_type].update(params)
            logger.info(f"Updated calibration parameters for {sensor_type}: {params}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating calibration parameters for {sensor_type}: {str(e)}")
            return False
    
    def get_calibration_params(self, sensor_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get calibration parameters for a sensor type or all sensors
        
        Args:
            sensor_type: Type of sensor ('ph', 'tds', 'turbidity'), or None for all
            
        Returns:
            Dictionary containing calibration parameters
        """
        if sensor_type is None:
            return self._calibration_params.copy()
        
        sensor_type = sensor_type.lower()
        if sensor_type in self._calibration_params:
            return {sensor_type: self._calibration_params[sensor_type].copy()}
        else:
            raise ValueError(f"Unsupported sensor type: {sensor_type}")