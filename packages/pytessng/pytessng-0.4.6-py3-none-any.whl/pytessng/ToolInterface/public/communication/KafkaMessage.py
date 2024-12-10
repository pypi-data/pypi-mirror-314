from kafka import KafkaProducer

from pytessng.Logger import logger


# 消息生产者
class KafkaMessageProducer:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            api_version=(0, 10),
            max_request_size=20 * 1024 * 1024,
            acks=0,  # 不等待确认
            max_in_flight_requests_per_connection=100,  # 控制最大同时未确认的请求
        )
        self.topic = topic

    # 发数据
    def send_message(self, message: str) -> bool:
        try:
            self.producer.send(self.topic, message.encode('utf-8'))
            logger.logger_pytessng.debug(f"Kafka: Message sent successfully.")
            return True
        except Exception as e:
            logger.logger_pytessng.error(f"Kafka: An error happened while sending the message. {e}")
            return False

    # 关闭
    def close(self) -> None:
        self.producer.close()
