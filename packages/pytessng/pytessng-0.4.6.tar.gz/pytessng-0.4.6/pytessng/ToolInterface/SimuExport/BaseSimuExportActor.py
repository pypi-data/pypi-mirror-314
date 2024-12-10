import os
import time
import json
from typing import Optional
from datetime import datetime
from abc import ABC
from queue import Queue
from threading import Thread

from ..public.communication.KafkaMessage import KafkaMessageProducer
from pytessng.Logger import logger


class BaseSimuExportActor(ABC):
    # 数据名称
    data_name: str = ""
    # 启动时间字符串
    shared_data: dict = {"start_time": None}

    def __init__(self, netiface, simuiface, Online):
        # TESSNG接口
        self._netiface = netiface
        self._simuiface = simuiface

        # JSON配置
        self._json_config: Optional[dict] = None
        # kafka配置
        self._kafka_config: Optional[dict] = None
        # JSON保存路径
        self._json_save_path: Optional[str] = None
        # kafka生产者对象
        self._kafka_producer: Optional[KafkaMessageProducer] = None

        # 数据队列
        self._data_queue: Queue = Queue()
        # 是否正在运行
        self._is_running: bool = False
        # 发送数据线程
        self._send_data_thread: Optional[Thread] = None

    def init_data(self, params: dict) -> None:
        self._json_config = params.get("json_config", dict())
        self._kafka_config = params.get("kafka_config", dict())

        # =============== kafka ===============
        # 上传到kafka的配置信息
        if self._kafka_config:
            ip = self._kafka_config["ip"]
            port = self._kafka_config["port"]
            topic = self._kafka_config["topic"]
            self._kafka_producer = KafkaMessageProducer(f"{ip}:{port}", topic)

    def ready(self):
        # 初始化启动时间
        if self.shared_data["start_time"] is None:
            self.shared_data["start_time"] = datetime.now().strftime("%Y%m%d%H%M%S")

        # =============== JSON ===============
        # 保存为JSON的配置信息
        if self._json_config:
            # 文件夹根路径
            base_folder_path = self._json_config["folder_path"]
            # 文件夹名称
            folder_name = f"{self.data_name}_{self.shared_data['start_time']}"
            # 数据文件夹路径
            folder_path = os.path.join(base_folder_path, folder_name)
            # 创建文件夹
            os.makedirs(folder_path, exist_ok=True)
            self._json_save_path = os.path.join(folder_path, "{}.json")

        # 更改运行状态
        self._is_running = True
        # 数据发送线程
        self._send_data_thread = Thread(target=self._apply_send_data)
        self._send_data_thread.start()

    def operate(self):
        # 计算数据
        basic_data = self._get_basic_data()
        # 放入队列
        self._data_queue.put(basic_data)

    def finish(self):
        # 清空队列
        while not self._data_queue.empty():
            time.sleep(0.01)
        # 更改运行状态
        self._is_running = False
        # 数据发送线程
        self._send_data_thread = None
        # 启动时间置为None
        self.shared_data["start_time"] = None

    def _apply_send_data(self):
        logger.logger_pytessng.info(f"{self.data_name}发送线程已经启动.")

        while True:
            time.sleep(0.01)

            # 如果队列为空
            if self._data_queue.empty():
                # 如果在运行就继续
                if self._is_running:
                    continue
                # 如果不在运行就退出
                else:
                    logger.logger_pytessng.info(f"{self.data_name}发送线程已经关闭.")
                    break

            # 从队列中获取数据
            basic_data = self._data_queue.get()  # 使用堵塞模式
            data = self._get_complete_data(basic_data)

            # 当前仿真计算批次
            batch_num = data["batchNum"]

            # =============== JSON ===============
            t1 = time.time()
            if self._json_save_path:
                file_path = self._json_save_path.format(batch_num)
                with open(file_path, 'w', encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False)

            # =============== kafka ===============
            t2 = time.time()
            if self._kafka_producer:
                data_json = json.dumps(data)
                self._kafka_producer.send_message(data_json)

            t3 = time.time()
            json_time = round((t2 - t1) * 1000, 1)
            kafka_time = round((t3 - t2) * 1000, 1)
            if batch_num % 10 == 0:
                print(f"[{self.data_name}]  仿真批次：{batch_num}，导出时间：{json_time}ms，上传时间：{kafka_time}ms，队列大小：{self._data_queue.qsize()}")

    # 获取基础数据
    def _get_basic_data(self) -> dict:
        pass

    # 获取完整数据
    def _get_complete_data(self, basic_data: dict) -> dict:
        pass
