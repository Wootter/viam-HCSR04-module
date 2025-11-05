from typing import ClassVar, Mapping, Any, Optional
from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.components.sensor import Sensor
from viam.logging import getLogger

import RPi.GPIO as GPIO
import time

LOGGER = getLogger(__name__)

class hcsr04(Sensor, Reconfigurable):
    """
    HC-SR04 represents an ultrasonic distance sensor that measures distance in centimeters.
    """
    MODEL: ClassVar[Model] = Model(ModelFamily("wootter", "sensor"), "hcsr04")

    def __init__(self, name: str):
        super().__init__(name)
        self.trig_pin = None
        self.echo_pin = None
        LOGGER.info(f"{self.__class__.__name__} initialized.")

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        instance = cls(config.name)
        instance.reconfigure(config, dependencies)
        return instance

    @classmethod
    def validate(cls, config: ComponentConfig):
        # Ensure 'trig_pin' and 'echo_pin' are in the configuration
        if "trig_pin" not in config.attributes.fields:
            raise Exception("'trig_pin' must be defined in the configuration.")
        if "echo_pin" not in config.attributes.fields:
            raise Exception("'echo_pin' must be defined in the configuration.")
        return ([], [])

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        # Get the pins from the configuration
        self.trig_pin = int(config.attributes.fields["trig_pin"].number_value)
        self.echo_pin = int(config.attributes.fields["echo_pin"].number_value)
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
        LOGGER.info(f"HC-SR04 configured with TRIG pin: {self.trig_pin}, ECHO pin: {self.echo_pin}")

    async def get_readings(
        self, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None, **kwargs
    ) -> Mapping[str, Any]:
        """
        Measure distance using the HC-SR04 ultrasonic sensor.

        Returns:
            Mapping[str, Any]: A mapping containing distance in centimeters and inches.
        """
        try:
            # Ensure trigger is low
            GPIO.output(self.trig_pin, False)
            time.sleep(0.05)

            # Send a short 10µs pulse to trigger
            GPIO.output(self.trig_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trig_pin, False)

            # Wait for echo start (with timeout)
            timeout_start = time.time()
            while GPIO.input(self.echo_pin) == 0:
                pulse_start = time.time()
                if time.time() - timeout_start > 0.1:  # 100ms timeout
                    raise Exception("Timeout waiting for echo start")

            # Wait for echo end (with timeout)
            timeout_start = time.time()
            while GPIO.input(self.echo_pin) == 1:
                pulse_end = time.time()
                if time.time() - timeout_start > 0.1:  # 100ms timeout
                    raise Exception("Timeout waiting for echo end")

            # Calculate distance
            pulse_duration = pulse_end - pulse_start
            distance_cm = pulse_duration * 17150  # Speed of sound / 2
            distance_cm = round(distance_cm, 2)
            distance_inches = round(distance_cm / 2.54, 2)

            LOGGER.info(f"Distance: {distance_cm} cm ({distance_inches} inches)")

            # Return the readings
            return {
                "distance_cm": distance_cm,
                "distance_inches": distance_inches,
            }
        except Exception as e:
            LOGGER.error(f"Error reading HC-SR04: {e}")
            return {
                "distance_cm": -1,
                "distance_inches": -1,
                "error": str(e)
            }

    async def close(self):
        """Clean up GPIO on shutdown."""
        try:
            GPIO.cleanup()
            LOGGER.info("GPIO cleanup completed")
        except Exception as e:
            LOGGER.error(f"Error during GPIO cleanup: {e}")
