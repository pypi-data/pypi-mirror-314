import json
import logging
import threading
from enum import Enum
from typing import Callable

import requests

from zyjj_client_sdk.base.base import Base
from zyjj_client_sdk.base.api import ApiService
import paho.mqtt.client as mqtt


class MqttEventType(Enum):
    Start = 1  # 开始任务
    Progress = 2  # 进度事件
    Success = 3  # 成功
    Fail = 4  # 失败
    DetailAppend = 5  # 详情追加
    DetailSet = 6  # 详情覆盖


class MqttServer:
    def __init__(self, base: Base, api: ApiService):
        self.__close = False
        self.__subscribe = {}
        self.__proxy = None
        self.__client = None
        self.__base = base
        # 获取客户端信息
        info = api.cloud_get_mqtt()
        self.__host, self.__client_id, self.__username, self.__password = (info['host'], info['client_id'], info['username'], info['password'])
        logging.info(f"[mqtt] info host {self.__host} client_id {self.__client_id} username {self.__username} password {self.__password}")
        # 如果不是代理我们才建立mqtt连接
        if self.__base.mqtt_proxy is None:
            logging.info(f'[mqtt] mqtt_proxy is None')
            self.__client = mqtt.Client(client_id=self.__client_id, protocol=mqtt.MQTTv311)
            self.__client.connect(self.__host, 1883, 30)
            self.__client.username_pw_set(self.__username, self.__password)
            self.__client.on_connect = lambda client, userdata, flags, rc: self.__on_connect()
            self.__client.on_message = lambda client, userdata, msg: self.__on_message(msg)
        else:
            self.__proxy = requests.session()

    def __on_connect(self):
        logging.info(f'[mqtt] connect success')
        # 启动后自动订阅topic
        for topic, handle in self.__subscribe.items():
            logging.info(f'[mqtt] subscribe {topic}')
            self.__client.subscribe(topic, qos=2)
        if self.__close:
            self.close()

    def __run(self):
        if self.__client is not None:
            self.__client.loop_forever()

    def __on_message(self, msg: mqtt.MQTTMessage):
        logging.info(f'[mqtt] from {msg.topic} get message {msg.payload}')
        event = json.loads(msg.payload)
        for topic, handle in self.__subscribe.items():
            if topic.endswith('/+'):
                if msg.topic.startswith(topic[:topic.index('/+')] + '/'):
                    handle(msg.topic, event)
            elif msg.topic == topic:
                handle(topic, event)

    def start_backend(self):
        threading.Thread(target=self.__run).start()

    def start(self):
        self.__run()

    def close(self):
        self.__close = True
        if self.__client is not None:
            self.__client.disconnect()

    # 发送event事件
    def send_task_event(self, uid: str, task_id: str, event_type: MqttEventType, data=None, code=-1):
        topic = f"task_event/{uid}"
        data = json.dumps({
            'task_id': task_id,
            'event_type': event_type.value,
            'code': code,
            'data': data
        }, ensure_ascii=False).encode()
        logging.info(f'[mqtt] {topic} send message {event_type} data {data}')
        if self.__client is not None:
            logging.info(f"[mqtt] use mqtt")
            self.__client.publish(topic, data, qos=1, retain=True)
        else:
            host = self.__base.mqtt_proxy
            logging.info(f"[mqtt] use proxy {host}")
            res = self.__proxy.post(
                f"{host}/{topic}",
                data=data,
                headers={
                    "x-cid": self.__client_id,
                    "x-username": self.__username,
                    "x-password": self.__password
                }
            )
            res.raise_for_status()

    # 监听topic
    def add_subscribe(self, topic: str, handle: Callable[[str, dict], None]):
        self.__subscribe[topic] = handle
