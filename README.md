# [hcsr04 modular service](https://app.viam.com/module/wootter/hcsr04)

This module implements the [rdk sensor API](https://github.com/rdk/sensor-api) in a `wootter:sensor:hcsr04` model.
With this model, you can measure distance using the HC-SR04 ultrasonic sensor.

## Requirements

The HC-SR04 sensor must be connected to a Raspberry Pi GPIO pins.

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the [`wootter:sensor:hcsr04` module](https://app.viam.com/module/wootter/hcsr04).

## Configure your sensor

> [!NOTE]  
> Before configuring your sensor, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

* Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com/).
* Click on the **Components** subtab and click the `sensor` subtab.
* Select the `wootter:sensor:hcsr04` model. 
* Enter a name for your sensor and click **Create**.
* On the new component panel, copy and paste the following attribute template into your sensor's **Attributes** box:

```json
{
  "trig_pin": 23,
  "echo_pin": 24
}
```
* Save and wait for the component to finish setup

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `wootter:sensor:hcsr04` sensor:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `trig_pin` | integer | **Required** | GPIO pin number for the trigger pin |
| `echo_pin` | integer | **Required** | GPIO pin number for the echo pin |

### Example Configuration

```json
{
  "trig_pin": 23,
  "echo_pin": 24
}
```

## Hardware Setup

Connect your HC-SR04 sensor:
- **VCC** → 5V
- **GND** → Ground
- **TRIG** → GPIO pin (e.g., GPIO 23)
- **ECHO** → GPIO pin (e.g., GPIO 24) - Use a voltage divider (1kΩ and 2kΩ resistors) to reduce 5V to 3.3V

## Readings

The sensor returns:

```json
{
  "distance_cm": 15.23,
  "distance_inches": 6.00
}
```

## License

MIT
