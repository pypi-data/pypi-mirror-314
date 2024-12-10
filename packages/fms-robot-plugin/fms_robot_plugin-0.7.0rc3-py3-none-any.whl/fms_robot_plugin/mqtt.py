from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field
from functools import partial
import paho.mqtt.client as mqtt
import json

SHARED_CLIENT: Optional[mqtt.Client] = None


def get_mqtt_client(client_id: Optional[str] = None, clean_session: Optional[bool] = None) -> mqtt.Client:
    global SHARED_CLIENT

    if SHARED_CLIENT is None:
        SHARED_CLIENT = mqtt.Client(client_id=client_id, clean_session=clean_session)

    return SHARED_CLIENT


@dataclass
class Subscriber:
    topic: str
    qos: int
    callback: Callable[[dict, dict], None]
    serialize: bool
    url_params: list[tuple[int, str]] = field(default_factory=list)


class MqttClient:
    def __init__(
        self,
        host: str,
        port: int,
        broker_username: Optional[str] = None,
        broker_password: Optional[str] = None,
        use_tls: bool = False,
        ca_certs: Optional[str] = None,
        keepalive: int = 60,
        client_id: Optional[str] = None,
        clean_session: Optional[bool] = None,
    ):
        self.client = get_mqtt_client(client_id, clean_session)
        self.connected = False
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self._subscribers: Dict[str, Subscriber] = {}
        self._on_connect_callback: List[Callable[[mqtt.Client, Any, Any, int], None]] = []
        self._on_disconnect_callback: List[Callable[[mqtt.Client, Any, int], None]] = []

        if use_tls:
            self.client.tls_set(ca_certs)

        if broker_username and broker_password:
            self.client.username_pw_set(broker_username, broker_password)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_messages

    def connect(self):
        self.client.connect(self.host, self.port, self.keepalive)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()

    def publish(self, topic: str, data: Any, serialize: bool = True, qos: int = 0, retain: bool = False):
        if serialize:
            data = json.dumps(data, default=str)

        self.client.publish(topic, data, qos, retain)

    def add_on_connect(self, callback: Callable[[mqtt.Client, Any, Any, int], None]):
        self._on_connect_callback.append(callback)

    def add_on_disconnect(self, callback: Callable[[mqtt.Client, Any, int], None]):
        self._on_disconnect_callback.append(callback)

    def on_connect(self, client: mqtt.Client, userdata, flags, rc):
        self.connected = True
        for topic, subscriber in self._subscribers.items():
            client.subscribe(topic, subscriber.qos)
        for on_connect in self._on_connect_callback:
            on_connect(client, userdata, flags, rc)

    def on_disconnect(self, client: mqtt.Client, userdata, rc):
        self.connected = False
        for on_disconnect in self._on_disconnect_callback:
            on_disconnect(client, userdata, rc)

    def on_messages(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage, original_topic: Optional[str] = None):
        subscriber: Optional[Subscriber] = self._subscribers.get(msg.topic, None)

        if subscriber is None:
            print(f"Found no Subscriber - {msg.topic}")
            return

        if original_topic is not None:
            msg.topic = original_topic.encode("utf-8")  # type: ignore

        payload = msg.payload

        if subscriber.serialize:
            payload = json.loads(payload.decode("utf-8"))

        url_params = {}

        for index, param in subscriber.url_params:
            url_params[param] = msg.topic.split("/")[index]

        if len(url_params.keys()) > 0:
            subscriber.callback(payload, url_params)  # type: ignore
        else:
            subscriber.callback(payload)  # type: ignore

    def on_wildcard_messages(self, topic: str, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        original_topic = str(msg.topic)
        msg.topic = topic.encode("utf-8")  # type: ignore
        self.on_messages(client, userdata, msg, original_topic)

    def subscribe(self, topic: str, qos: int, cb: Callable[[dict, dict], None], serialize: bool = True):
        url_params = []
        for index, section in enumerate(topic.split("/")):
            if section.startswith(":"):
                topic = topic.replace(section, "+")
                url_params.append((index, section[1:]))

        self._subscribers[topic] = Subscriber(topic, qos, cb, serialize, url_params)

        if len(url_params) > 0:
            self.client.message_callback_add(topic, partial(self.on_wildcard_messages, topic))

        if self.connected:
            self.client.subscribe(topic, qos)

        return self.client


class MqttConsumer:
    def __init__(self, topic: str, qos: int, client: MqttClient):
        self.topic = topic
        self.qos = qos
        self.url_params: list[tuple[int, str]] = []
        self.client = client

    def consume(self, cb: Callable[[dict, dict], None], serialize: bool = True):
        return self.client.subscribe(self.topic, self.qos, cb, serialize)
