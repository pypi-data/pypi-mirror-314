import json
import logging
import sys
import time
import traceback

from zyjj_client_sdk.base import Base, ApiService, MqttServer, MqttEventType
from zyjj_client_sdk.base.entity import TaskInfo, TaskStatus
from zyjj_client_sdk.base.exception import ServerError
from zyjj_client_sdk.flow import FlowBase, FlowService
from threading import Thread
import queue

from zyjj_client_sdk.lib import OSSService


# 本地服务端
class Service:
    # 初始化基本服务
    def __init__(self, thread_size: int = 4):
        self.__base = Base()
        self.__api = ApiService(self.__base)
        self.__oss = OSSService(self.__base, self.__api)
        self.__handle = {}
        self.__mqtt = MqttServer(self.__base, self.__api)
        self.__global_data = {}
        # 初始化一个任务队列，把我们的任务给加到队列里去
        self.__task_queue = queue.Queue(maxsize=thread_size)
        # 后台起一个消费者不断去消费数据
        Thread(target=self.__start_consumer).start()

    # 添加全局变量
    def add_global(self, key: str, value: any) -> 'Service':
        self.__global_data[key] = value
        return self

    # 启动服务
    def start(self) -> 'Service':
        # 后台启动mqtt
        self.__mqtt.start_backend()
        return self

    # 停止服务
    def stop(self):
        logging.info("stop service")
        self.__mqtt.close()
        self.__task_queue.put('close')
        sys.exit(0)

    # 发送成功的消息
    def __success(self, uid: str, task_id: str, data: dict):
        self.__api.task_update_task(
            task_id,
            status=TaskStatus.Success,
            output=json.dumps(data, ensure_ascii=False),
            progress=100,
        )
        self.__mqtt.send_task_event(
            uid,
            task_id,
            MqttEventType.Success,
            data
        )

    # 发送失败消息
    def __fail(self, uid: str, task_id: str, code: int, msg: str):
        self.__api.task_update_task(
            task_id,
            status=TaskStatus.Fail,
            code=code,
            msg=msg,
        )
        self.__mqtt.send_task_event(
            uid,
            task_id,
            MqttEventType.Fail,
            msg,
            code
        )

    # 给队列中添加一个新任务
    def __add_new_task(self):
        now = time.time()
        self.__task_queue.put(now)

    # 后台启动一个线程不断去消费任务
    def __start_consumer(self):
        while True:
            task = self.__task_queue.get()
            # 如果收到了退出命令就直接退出
            if task == 'close':
                return
            logging.info(f'get task create offset {time.time() - task} s')
            # 直接后台执行
            Thread(target=self.__execute_task).start()

    # 执行任务
    def __execute_task(self):
        try:
            self.execute_one_task()
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())
        finally:
            self.__task_queue.task_done()

    # 后台异步通知
    def notify(self):
        logging.info(f'notify new task')
        Thread(target=self.__add_new_task).start()

    # 执行一个任务
    def execute_one_task(self) -> dict | None:
        # 拉取任务
        task_info = self.__api.task_pull_task()
        if task_info is None:
            logging.info("[task] task not found")
            return None
        logging.info(f'[task] pull task is {task_info}')
        # 获取任务信息
        task_info = TaskInfo(
            task_info['id'],
            task_info['uid'],
            task_info['task_type'],
            json.loads(task_info['input']),
            task_info['source']
        )
        try:
            _base = FlowBase(
                self.__base,
                self.__api,
                self.__mqtt,
                self.__oss,
                self.__global_data,
                task_info
            )
            # 如果是代码节点，我们就可以直接去执行代码
            if task_info.task_type == 1:
                _input = task_info.input
                data = _base.tiger_code(_input["entity_id"], _input["input"], _base)
                self.__success(task_info.uid, task_info.task_id, data)
                return data
            # 否则我们正常去执行流程
            flow_info = self.__api.task_pull_flow(task_info.task_type)
            logging.info(f"flow info {flow_info}")
            # 初始化流程服务并触发流程
            data = FlowService(_base, flow_info['flow_info']).tiger_flow()
            self.__success(task_info.uid, task_info.task_id, data)
            return data
        # 捕获服务错误
        except ServerError as e:
            traceback.print_exc()
            self.__fail(task_info.uid, task_info.task_id, e.code, e.message)
            return {"msg": str(e)}
        except Exception as e:
            traceback.print_exc()
            self.__fail(task_info.uid, task_info.task_id, -1, str(e))
            return {"msg": str(e)}
