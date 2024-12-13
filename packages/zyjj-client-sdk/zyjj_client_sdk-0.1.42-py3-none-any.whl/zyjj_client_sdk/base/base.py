import logging
import os
import uuid


class Base:
    def __init__(
        self,
        username=os.environ.get("zyjj_username"),
        password=os.environ.get("zyjj_password"),
        host=os.environ.get("zyjj_host"),
        mqtt_proxy=os.environ.get("zyjj_mqtt_proxy"),
        knowledge_host=os.environ.get("zyjj_knowledge"),
    ):
        self.username = username
        self.password = password
        self.host = host
        self.knowledge_host = knowledge_host
        self.mqtt_proxy = mqtt_proxy
        self.tmp_dir = "/tmp"

    # 生成一个文件名
    @staticmethod
    def generate_filename(extend: str) -> str:
        return f"{str(uuid.uuid4())}.{extend}"

    # 生成一个临时文件
    def generate_local_file(self, extend: str) -> str:
        return f"{self.tmp_dir}/{str(uuid.uuid4())}.{extend}"

    # 根据路径生成一个新的同名文件
    def generate_file_with_path(self, path: str) -> str:
        return self.generate_local_file(path.split(".")[-1])
