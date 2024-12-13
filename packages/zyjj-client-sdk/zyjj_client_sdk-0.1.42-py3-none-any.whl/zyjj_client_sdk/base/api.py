import json
import logging
import requests
from zyjj_client_sdk.base.base import Base
from zyjj_client_sdk.base.entity import TaskStatus
from zyjj_client_sdk.base.exception import RemoteError


class ApiService:
    def __init__(self, base: Base):
        self.__header = {
            "x-username": base.username,
            "x-password": base.password,
            "Content-Type": "application/json",
            "referer": "https://zyjj.cc"
        }
        self.__base = f"{base.host}/api/v1/client"
        self.__knowledge = f"{base.knowledge_host}/api/v1/client"
        self.__session = requests.session()
        self.__timeout = 60

    def __request(self, method: str, path: str, data: dict = None, host: str = None):
        url = f"{self.__base}/{path}"
        if host is not None:
            url = f"{host}/{path}"
        logging.info(f"request url {url}")
        res = None
        if method == "get":
            res = self.__session.get(url, timeout=self.__timeout, headers=self.__header)
        elif method == "put":
            res = self.__session.put(url, timeout=self.__timeout, data=json.dumps(data), headers=self.__header)
        elif method == "post":
            res = self.__session.post(url, timeout=self.__timeout, data=json.dumps(data), headers=self.__header)
        elif method == "delete":
            res = self.__session.delete(url, timeout=self.__timeout, headers=self.__header)
        if res is None:
            logging.info("[request] request res is none")
        elif res.status_code != 200:
            logging.info(f"[request] request status code is {res.status_code}, res is {res.text}")
            raise RemoteError(res.status_code, "http请求错误")
        else:
            res = res.json()
            if "code" in res and res["code"] != 0:
                raise RemoteError(res["code"], res["msg"])
            else:
                return res["data"]
        return {}

    # 获取腾讯云token
    def could_get_tencent_token(self):
        return self.__request("get", "cloud/tencent/token")

    # 获取腾讯云cos秘钥信息
    def could_get_tencent_cos(self):
        return self.__request("get", "cloud/tencent/cos")

    # 获取阿里云oss秘钥
    def cloud_get_aliyun_oss(self):
        return self.__request("get", "cloud/aliyun/oss")

    # 获取火山语音信息
    def cloud_get_volcano_voice(self):
        return self.__request("get", "cloud/volcano/voice")

    # 获取MQTT
    def cloud_get_mqtt(self):
        return self.__request("get", f"cloud/mqtt/task")

    # 拉取任务
    def task_pull_task(self):
        return self.__request("get", "task/pull")

    # 拉取任务流程
    def task_pull_flow(self, task_type: int):
        return self.__request("get", f"flow/{task_type}")

    # 更新任务状态
    def task_update_task(
            self,
            task_id: str,
            status: TaskStatus = None,
            output: str = None,
            point_cost: int = None,
            code: int = None,
            msg: str = None,
            progress: float = None,
    ):
        """
        任务状态更新
        :param task_id: 任务id
        :param status: 任务状态
        :param point_cost: 消耗积分
        :param output: 任务输出
        :param code: 错误码
        :param msg: 错误信息
        :param progress: 执行进度
        :return:
        """
        data = {}
        if status is not None:
            data["status"] = status.value
        if output is not None:
            data["output"] = output
        if point_cost is not None:
            data["point_cost"] = point_cost
        if code is not None:
            data["code"] = code
        if msg is not None:
            data["msg"] = msg
        if progress is not None:
            data["progress"] = progress

        return self.__request("put", f"task/{task_id}", data)

    # 获取用户积分
    def get_user_point(self, uid: str) -> int:
        return self.__request("get", f"point/user/{uid}", {})

    # 扣除用户积分
    def use_user_point(self, task_id: str, uid: str, name: str, point: int, desc='') -> bool:
        if len(desc) > 20:
            desc = f'{desc[:20]}...'
        logging.info(f"[api] {uid} use point {point}")
        try:
            self.__request("post", "point/deducting", {
                "uid": uid,
                "name": name,
                "point": int(point),
                "desc": desc,
            })
            # 更新任务id消耗的积分
            self.task_update_task(task_id, point_cost=point)
            return True
        except Exception as e:
            logging.error(f"[api] use_user_point error {e}")
            return False

    # 获取配置
    def get_config(self, key: str) -> str:
        return self.__request("get", f"config/{key}")["value"]

    # 上传流程日志
    def upload_flow_log(self, data):
        return self.__request("post", "flow/log", data)

    # 获取流程数据
    def get_entity_data(self, entity_id: str) -> dict:
        res = self.__request("get", f"entity/{entity_id}")
        return json.loads(res['data'])

    # 获取流程信息
    def get_entity_info(self, entity_id: str) -> dict:
        return self.__request("get", f"entity/{entity_id}")

    # 文档检索
    def doc_query(self, query: str, tag: str, size: int) -> list:
        return self.__request("get", f"doc/query?query={query}&tag={tag}&size={size}", {}, host=self.__knowledge)

    # 图像检索
    def img_query(self, embedding: list[float], tag: str, size: int):
        return self.__request(
            'post',
            'img/query',
            {"embedding": embedding, "tag": tag, "size": size},
            host=self.__knowledge
        )
