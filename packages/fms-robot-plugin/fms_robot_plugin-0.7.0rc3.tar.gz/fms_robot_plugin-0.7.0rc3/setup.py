# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fms_robot_plugin']

package_data = \
{'': ['*']}

install_requires = \
['aiomqtt>=1.2.1,<2.0.0',
 'paho-mqtt>=1.6.1,<2.0.0',
 'pydantic>=2.3.0,<3.0.0',
 'requests>=2.31.0,<3.0.0',
 'types-pyyaml>=6.0.12.20240917,<7.0.0.0']

setup_kwargs = {
    'name': 'fms-robot-plugin',
    'version': '0.7.0rc3',
    'description': '',
    'long_description': '# FMS Robot Plugin Library\n\n## Installation\n\n```bash\npip install fms-robot-plugin\n```\n\n## Quickstart\n```python\nfrom fms_robot_plugin.robot import Robot\nfrom fms_robot_plugin.constants import Capability\nfrom fms_robot_plugin.typings import Twist\n\ncapabilities = [\n    "on_teleop",\n    "on_stop",\n    "set_pose",\n    "set_lidar",\n]\n\nrobot = Robot(\n    plugin_name="custom_plugin",\n    plugin_version="v1",\n    robot_key="secret_robot_key",\n    broker_host="mqtt-broker.movelrobotics.com",\n    broker_port=1883,\n    broker_use_tls=False,\n    broker_ca_certs=None,\n    api_hostname="fms-api.movelrobotics.com",\n    capabilities=capabilities,\n)\n\ndef handle_teleop(payload: Twist):\n    pass\n\ndef handle_stop():\n    pass\n\n\nrobot.on_teleop(handle_teleop)\nrobot.on_stop(handle_stop)\nrobot.run()\n```\n\n## Reconnect Behavior example\n```python\nfrom fms_robot_plugin.robot import Robot\nfrom fms_robot_plugin.constants import Capability\nfrom fms_robot_plugin.typings import ReconnectBehavior\n\ncapabilities = [\n    "on_teleop",\n    "on_stop",\n    "set_pose",\n    "set_lidar",\n]\n\nrobot = Robot(\n    plugin_name="custom_plugin",\n    plugin_version="v1",\n    robot_key="secret_robot_key",\n    broker_host="mqtt-broker.movelrobotics.com",\n    broker_port=1883,\n    broker_use_tls=False,\n    broker_ca_certs=None,\n    api_hostname="fms-api.movelrobotics.com",\n    capabilities=capabilities,\n)\n\ndef handle_on_connect(payload: dict):\n    print(f"Connected to FMS at {payload[\'sent_at\']}")\n\ndef handle_on_disconnect(payload: dict):\n    print(f"Disconnected from FMS at {payload[\'sent_at\']}")\n\n    if robot.reconnect_behavior == ReconnectBehavior.CANCEL_QUEUE:\n        print("Stopping robot active task")\n    elif robot.reconnect_behavior == ReconnectBehavior.PAUSE_QUEUE:\n        print("Pausing robot active task")\n    elif robot.reconnect_behavior == ReconnectBehavior.PAUSE_THEN_RESUME_QUEUE:\n        print("Pausing robot active task, will resume after reconnect")\n\nrobot.on_connect = handle_on_connect\nrobot.on_disconnect = handle_on_disconnect\nrobot.run()\n```',
    'author': 'Dionesius Agung',
    'author_email': 'dionesius@movel.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
