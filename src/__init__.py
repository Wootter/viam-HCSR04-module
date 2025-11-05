"""
This file registers the model with the Python SDK.
"""

from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .hcsr04 import hcsr04

Registry.register_resource_creator(Sensor.API, hcsr04.MODEL, ResourceCreatorRegistration(hcsr04.new, hcsr04.validate))
