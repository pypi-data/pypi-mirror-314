import base64
import json
import yaml
import requests
import datetime

from typing import Callable, Dict, List, Optional
from threading import Event
from fms_robot_plugin.mqtt import MqttClient, MqttConsumer
from fms_robot_plugin.typings import (
    ConnectionStatus,
    StartCameraCommand,
    Status,
    LaserScan,
    Twist,
    Pose,
    Map,
    RobotInfo,
    Task,
    DecimatedPlan,
    Result,
    AcquireLockRequest,
    AcquireLockResponse,
    ReleaseLockRequest,
    ReleaseLockResponse,
    RetryAcquireLockCommand,
    ReconnectBehavior,
    Parameter,
)


class Robot:
    robot_key: Optional[str]
    fms_mode: bool = True
    maintenance_mode: bool = False
    __http_health_check_fail_count__: int = 0
    health_check_failure: Event = Event()

    def __init__(
        self,
        plugin_name: str,
        plugin_version: str,
        robot_key: str,
        broker_host: str = "broker.movelrobotics.com",
        broker_port: int = 1883,
        broker_use_tls: bool = False,
        broker_ca_certs: Optional[str] = None,
        broker_username: Optional[str] = None,
        broker_password: Optional[str] = None,
        api_hostname: str = "api.movelrobotics.com",
        capabilities: List[str] = [],
        parameters_file_path: Optional[str] = None,
        keepalive: int = 60,
        connection_topic: Optional[str] = None,
        client_id: Optional[str] = None,
        clean_session: Optional[bool] = None,
        auto_disconnect_on_health_check_failure: bool = False,
    ):
        self.plugin_name = plugin_name
        self.plugin_version = plugin_version
        self.capabilities = capabilities
        self.robot_key = robot_key
        self.priority: int = 0
        self.reconnect_behavior: ReconnectBehavior = ReconnectBehavior.CANCEL_QUEUE

        self.parameters_file_path = parameters_file_path
        self.parameters: List[Parameter] = []

        self.acquire_lock_message_id: Optional[str] = None
        self.release_lock_message_id: Optional[str] = None
        self.traffic_task: Optional[Task] = None
        self.node_ids: List[str] = []

        self.api_hostname = api_hostname
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.broker_use_tls = broker_use_tls
        self.broker_ca_certs = broker_ca_certs
        self.broker_username = broker_username
        self.broker_password = broker_password
        # custom mqtt client connection
        self.mqtt = MqttClient(
            broker_host,
            broker_port,
            broker_username,
            broker_password,
            broker_use_tls,
            broker_ca_certs,
            keepalive,
            client_id,
            clean_session,
        )

        self.keepalive = keepalive
        self.connection_topic = f"robots/{self.robot_key}/connection" if connection_topic is None else connection_topic
        self.on_connect: Callable[[dict], None] = lambda payload: None
        self.on_disconnect: Callable[[dict], None] = lambda payload: None
        self.auto_disconnect_on_health_check_failure = auto_disconnect_on_health_check_failure

    def run(self):
        self.load_parameters()
        self.register_default_callbacks()
        self.establish_connection()

    def stop(self):
        self.terminate_connection()
        self.unregister_default_callbacks()

    def unregister_default_callbacks(self):
        pass

    def terminate_connection(self):
        self.mqtt.disconnect()

    """
    Command Callbacks

    These methods are called when a command is published from the FMS server.
    """

    def on_teleop(self, cb: Callable[[Twist], None]):
        topic = f"robots/{self.robot_key}/teleop"
        return self.consumer(topic).consume(lambda data: cb(Twist(**data)))

    def on_stop(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/stop"
        return self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_start_mapping(self, cb: Callable[[str], None]):
        topic = f"robots/{self.robot_key}/mapping/start"
        return self.consumer(topic).consume(lambda map_id: cb(map_id), serialize=False)

    def on_save_mapping(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/mapping/save"
        return self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_localize(self, cb: Callable[[str, Pose], None]):
        topic = f"robots/{self.robot_key}/localize"
        return self.consumer(topic).consume(lambda data: cb(data["map_id"], Pose(**data["initial_pose"])))

    def on_load_navigation_map_pgm(self, cb: Callable[[bytes, str, Optional[Pose], bool], None]):
        topic = f"robots/{self.robot_key}/maps/:map_id/load/navigation_pgm"
        return self.consumer(topic).consume(
            lambda data, url_params: cb(
                base64.b64decode(data["file"]),
                url_params["map_id"],
                Pose(**data["initial_pose"]) if data.get("initial_pose") else None,
                data.get("publish_result", False),
            )
        )

    def on_load_navigation_map_yaml(self, cb: Callable[[bytes, str, Optional[Pose], bool], None]):
        topic = f"robots/{self.robot_key}/maps/:map_id/load/navigation_yaml"
        return self.consumer(topic).consume(
            lambda data, url_params: cb(
                base64.b64decode(data["file"]),
                url_params["map_id"],
                Pose(**data["initial_pose"]) if data.get("initial_pose") else None,
                data.get("publish_result", False),
            )
        )

    def on_load_localization_map_pgm(self, cb: Callable[[bytes, str, Optional[Pose], bool], None]):
        topic = f"robots/{self.robot_key}/maps/:map_id/load/localization_pgm"
        return self.consumer(topic).consume(
            lambda data, url_params: cb(
                base64.b64decode(data["file"]),
                url_params["map_id"],
                Pose(**data["initial_pose"]) if data.get("initial_pose") else None,
                data.get("publish_result", False),
            )
        )

    def on_load_localization_map_yaml(self, cb: Callable[[bytes, str, Optional[Pose], bool], None]):
        topic = f"robots/{self.robot_key}/maps/:map_id/load/localization_yaml"
        return self.consumer(topic).consume(
            lambda data, url_params: cb(
                base64.b64decode(data["file"]),
                url_params["map_id"],
                Pose(**data["initial_pose"]) if data.get("initial_pose") else None,
                data.get("publish_result", False),
            )
        )

    def on_unload_map(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/maps/unload"
        return self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_execute_task(self, cb: Callable[[Task], None]):
        topic = f"robots/{self.robot_key}/tasks/execute"
        return self.consumer(topic).consume(lambda data: cb(Task(**data)))

    def on_resume_task(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/tasks/resume"
        return self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_pause_task(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/tasks/pause"
        return self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_set_priority(self, cb: Callable[[int], None]):
        topic = f"robots/{self.robot_key}/priority"
        return self.consumer(topic).consume(lambda priority: cb(int(priority.decode("utf-8"))), serialize=False)

    def on_robot_info(self, cb: Callable[[RobotInfo], None]):
        topic = f"robots/{self.robot_key}/info/receive"
        return self.consumer(topic).consume(lambda data: cb(RobotInfo(**data)))

    def on_preview_map(self, cb: Callable[[], None]):
        topic = f"robots/{self.robot_key}/mapping/import"
        return self.consumer(topic).consume(lambda _: cb(), serialize=False)

    def on_acquire_lock_response(self, cb: Callable[[AcquireLockResponse], None]):
        topic = f"robots/{self.robot_key}/locks/acquire/response"
        return self.consumer(topic, 2).consume(lambda data: cb(AcquireLockResponse(**data)))

    def on_release_lock_response(self, cb: Callable[[ReleaseLockResponse], None]):
        topic = f"robots/{self.robot_key}/locks/release/response"
        return self.consumer(topic, 2).consume(lambda data: cb(ReleaseLockResponse(**data)))

    def on_retry_acquire_lock(self, cb: Callable[[RetryAcquireLockCommand], None]):
        topic = f"robots/{self.robot_key}/locks/retry-acquire"
        return self.consumer(topic).consume(lambda data: cb(RetryAcquireLockCommand(**data)))

    def on_start_camera_feed(self, cb: Callable[[StartCameraCommand], None]):
        # TODO: camera fix serialize True and use map_id and rostopic payload
        topic = f"robots/{self.robot_key}/camera/start"
        return self.consumer(topic).consume(lambda data: cb(StartCameraCommand(**data)))

    def on_set_reconnect_behavior(self, cb: Callable[[ReconnectBehavior], None]):
        topic = f"robots/{self.robot_key}/reconnect_behavior"
        return self.consumer(topic).consume(
            lambda data: cb(ReconnectBehavior(str(data.decode("utf-8")))), serialize=False
        )

    def on_set_parameters(self, cb: Callable[[Parameter], None]):
        topic = f"robots/{self.robot_key}/parameters/set"
        return self.consumer(topic).consume(lambda data: cb(Parameter(**data)))

    """
    Publishers

    These methods are called to publish data to the FMS server.
    """

    def set_camera_feed(self, data: str):
        self.mqtt.publish(f"robots/{self.robot_key}/camera", data, serialize=False)

    def set_lidar(self, data: LaserScan):
        self.mqtt.publish(f"robots/{self.robot_key}/lidar", data.dict())

    def set_pose(self, data: Pose):
        self.mqtt.publish(f"robots/{self.robot_key}/pose", data.dict())

    def set_map_data(self, data: Map):
        self.mqtt.publish(f"robots/{self.robot_key}/mapping/data", data.dict())

    def set_status(self, data: Status):
        self.mqtt.publish(f"robots/{self.robot_key}/status", data, serialize=False)

    def set_battery_percentage(self, data: float):
        self.mqtt.publish(f"robots/{self.robot_key}/battery", data, serialize=False)

    def set_map_result(self, pgm: bytes, yaml: bytes):
        url = f"{self.api_hostname}/api/robots/{self.robot_key}/mapping/result"
        files = [
            ("files", ("mapping_result.pgm", pgm)),
            ("files", ("mapping_result.yaml", yaml)),
        ]

        return requests.post(url=url, files=files)

    def check_map_existance(self, filenames: List[str]):
        url = f"{self.api_hostname}/api/robots/{self.robot_key}/check-map"
        data = {
            "filenames": filenames,
        }

        response = requests.post(url, json=data)
        return response

    def set_map_preview_result(self, name: str, pgm: bytes, yaml: bytes):
        url = f"{self.api_hostname}/api/robots/{self.robot_key}/mapping/preview/result"
        files = [
            ("files", pgm),
            ("files", yaml),
        ]
        data = {
            "name": name,
        }
        response = requests.post(url, data=data, files=files)
        return response

    def set_cpu_usage(self, data: float):
        self.mqtt.publish(f"robots/{self.robot_key}/monitor/cpu", data, serialize=False)

    def set_memory_usage(self, data: float):
        self.mqtt.publish(f"robots/{self.robot_key}/monitor/memory", data, serialize=False)

    def set_battery_usage(self, data: float):
        self.mqtt.publish(f"robots/{self.robot_key}/monitor/battery", data, serialize=False)

    def set_robot_info(self, data: RobotInfo):
        self.mqtt.publish(f"robots/{self.robot_key}/info/reply", data.dict())

    def set_decimated_plan(self, data: DecimatedPlan):
        self.mqtt.publish(f"robots/{self.robot_key}/decimated-plan", data.dict())

    def set_result(self, data: Result):
        self.mqtt.publish(f"robots/{self.robot_key}/result", data.dict())

    def set_obstacle_notification(self, data: bool):
        self.mqtt.publish(f"robots/{self.robot_key}/obstacle", data, serialize=False)

    def set_notification_message(self, data: str):
        self.mqtt.publish(f"robots/{self.robot_key}/notification", data, serialize=False)

    def set_acquire_lock_request(self, data: AcquireLockRequest):
        self.acquire_lock_message_id = data.message_id
        self.mqtt.publish(f"robots/{self.robot_key}/locks/acquire/request", data.dict(), qos=2)

    def set_release_lock_request(self, data: ReleaseLockRequest):
        self.release_lock_message_id = data.message_id
        self.mqtt.publish(f"robots/{self.robot_key}/locks/release/request", data.dict(), qos=2)

    def set_map_id(self, map_id: str):
        self.mqtt.publish(f"robots/{self.robot_key}/maps/{map_id}/set", data=None)

    def set_fms_mode(self, fms_mode: bool):
        self.fms_mode = fms_mode

    def set_maintenance_mode(self, maintenance_mode: bool):
        self.maintenance_mode = maintenance_mode

    """
    Utilities
    """

    def consumer(self, topic: str, qos: int = 0):
        return MqttConsumer(
            topic,
            qos,
            self.mqtt,
        )

    def load_parameters(self, parameters_file_path: Optional[str] = None):
        if parameters_file_path is None and self.parameters_file_path is None:
            return

        if parameters_file_path is None:
            parameters_file_path = self.parameters_file_path

        assert parameters_file_path is not None
        with open(parameters_file_path) as parameters_file:
            parameters = yaml.safe_load(parameters_file)
            parameters = parameters["parameters"]
            self.parameters = []

            for parameter in parameters:
                if parameter["type"] not in ["int", "float", "string", "bool"]:
                    continue

                self.parameters.append(
                    Parameter(
                        name=parameter["name"],
                        type=parameter["type"],
                        value=parameter["value"],
                        ros_params=Parameter.ROSParams(**parameter["ros"]),
                    )
                )

    def register_default_callbacks(self):
        self.on_set_priority(self.set_priority)
        self.on_set_reconnect_behavior(self.set_reconnect_behavior)

    def set_priority(self, priority: int):
        self.priority = priority

    def set_reconnect_behavior(self, behavior: ReconnectBehavior):
        self.reconnect_behavior = behavior

    def setup_client(self):
        def _on_connect(client, userdata, flags, rc):
            self.mqtt.publish(
                self.connection_topic,
                data={
                    "status": ConnectionStatus.Connected.value,
                    "sent_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "name": self.plugin_name,
                    "version": self.plugin_version,
                    "capabilities": self.capabilities,
                    "parameters": [parameter.model_dump() for parameter in self.parameters],
                },
                qos=1,
                retain=True,
            )

            payload = {"sent_at": datetime.datetime.now().isoformat()}
            self.on_connect(payload)
            self.consumer("fms/ping", 0).consume(lambda data: self.on_ping_message(data))

        def _on_disconnect(client, userdata, rc):
            payload = {"sent_at": datetime.datetime.now().isoformat()}
            self.on_disconnect(payload)

        self.mqtt.add_on_connect(_on_connect)
        self.mqtt.add_on_disconnect(_on_disconnect)

        self.mqtt.client.will_set(
            self.connection_topic,
            payload=json.dumps(
                {
                    "status": ConnectionStatus.Disconnected.value,
                    "sent_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                }
            ),
            qos=0,
            retain=True,
        )
        print("[ROBOT-PLUGIN] client configuration is done")

    def establish_connection(self):
        print("[ROBOT-PLUGIN] client is starting connection")
        self.mqtt.connect()
        print("[ROBOT-PLUGIN] client is connected")

    def on_ping_message(self, data: Dict):
        server_time_stamp: datetime.datetime = datetime.datetime.fromisoformat(data["time"])
        data["fms_mode"] = self.fms_mode
        data["maintenance_mode"] = self.maintenance_mode
        self.mqtt.publish(f"robots/{self.robot_key}/ping", data)
        if server_time_stamp.second % 5 == 0:  # ping http for every 5 seconds
            url = f"{self.api_hostname}/api/robots/{self.robot_key}/health-check"
            try:
                resp = requests.get(url=url, timeout=3)

                if resp.status_code == 204:
                    if self.__http_health_check_fail_count__ > 0:
                        print("[ROBOT-PLUGIN] FMS Health check failure cleared")

                    self.__http_health_check_fail_count__ = 0

                    if self.health_check_failure.is_set() and not self.auto_disconnect_on_health_check_failure:
                        self.health_check_failure.clear()
                else:
                    print("[ROBOT-PLUGIN] FMS Health check failure detected")
                    self.__http_health_check_fail_count__ += 1

            except Exception:
                print("[ROBOT-PLUGIN] FMS Health check failure detected")
                self.__http_health_check_fail_count__ += 1

            if self.__http_health_check_fail_count__ > 3:
                print("[ROBOT-PLUGIN] FMS Health check failure over the threshold limit, setting the flag")
                self.health_check_failure.set()
                if self.auto_disconnect_on_health_check_failure:
                    self.stop()
