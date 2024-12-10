# FMS Robot Plugin Library

## Installation

```bash
pip install fms-robot-plugin
```

## Quickstart
```python
from fms_robot_plugin.robot import Robot
from fms_robot_plugin.constants import Capability
from fms_robot_plugin.typings import Twist

capabilities = [
    "on_teleop",
    "on_stop",
    "set_pose",
    "set_lidar",
]

robot = Robot(
    plugin_name="custom_plugin",
    plugin_version="v1",
    robot_key="secret_robot_key",
    broker_host="mqtt-broker.movelrobotics.com",
    broker_port=1883,
    broker_use_tls=False,
    broker_ca_certs=None,
    api_hostname="fms-api.movelrobotics.com",
    capabilities=capabilities,
)

def handle_teleop(payload: Twist):
    pass

def handle_stop():
    pass


robot.on_teleop(handle_teleop)
robot.on_stop(handle_stop)
robot.run()
```

## Reconnect Behavior example
```python
from fms_robot_plugin.robot import Robot
from fms_robot_plugin.constants import Capability
from fms_robot_plugin.typings import ReconnectBehavior

capabilities = [
    "on_teleop",
    "on_stop",
    "set_pose",
    "set_lidar",
]

robot = Robot(
    plugin_name="custom_plugin",
    plugin_version="v1",
    robot_key="secret_robot_key",
    broker_host="mqtt-broker.movelrobotics.com",
    broker_port=1883,
    broker_use_tls=False,
    broker_ca_certs=None,
    api_hostname="fms-api.movelrobotics.com",
    capabilities=capabilities,
)

def handle_on_connect(payload: dict):
    print(f"Connected to FMS at {payload['sent_at']}")

def handle_on_disconnect(payload: dict):
    print(f"Disconnected from FMS at {payload['sent_at']}")

    if robot.reconnect_behavior == ReconnectBehavior.CANCEL_QUEUE:
        print("Stopping robot active task")
    elif robot.reconnect_behavior == ReconnectBehavior.PAUSE_QUEUE:
        print("Pausing robot active task")
    elif robot.reconnect_behavior == ReconnectBehavior.PAUSE_THEN_RESUME_QUEUE:
        print("Pausing robot active task, will resume after reconnect")

robot.on_connect = handle_on_connect
robot.on_disconnect = handle_on_disconnect
robot.run()
```