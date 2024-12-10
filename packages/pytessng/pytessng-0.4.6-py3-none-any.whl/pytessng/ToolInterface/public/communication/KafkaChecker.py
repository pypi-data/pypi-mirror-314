import traceback
from kafka import KafkaProducer, KafkaConsumer

from pytessng.Config import SimuExportConfig
from pytessng.Logger import logger


# 核验kafka的连通性
class KafkaChecker:
    @staticmethod
    def check_data(ip: str, port: str) -> bool:
        test_topic = SimuExportConfig.Kafka.TEST_TOPIC

        kafka_pull_is_ok = False
        consumer = None

        try:
            # 创建 KafkaProducer 实例，用于发送测试消息
            producer = KafkaProducer(
                bootstrap_servers=f'{ip}:{port}',
                acks=1,  # 确认级别 1 表示 leader 收到消息即确认
                retries=5,
                max_in_flight_requests_per_connection=1,
            )
            # 发送测试消息到指定 topic
            producer.send(test_topic, b'test_message')
            producer.flush()

            # 创建 KafkaConsumer 实例，用于拉取消息
            consumer = KafkaConsumer(
                test_topic,
                bootstrap_servers=f'{ip}:{port}',
                group_id='test_group',
                auto_offset_reset='earliest',
                enable_auto_commit=False,
                consumer_timeout_ms=5000  # 设置拉取消息的超时时间
            )
            # 订阅topic并拉取消息
            for _ in consumer:
                kafka_pull_is_ok = True
                message = f"Kafka can receive messages."
                logger.logger_pytessng.debug(message)
                message = "Kafka connectivity test successful!"
                logger.logger_pytessng.debug(message)
                break
        except:
            message = f"Kafka connectivity test failed with the error:\n{traceback.format_exc()}"
            logger.logger_pytessng.error(message)
        try:
            consumer.close()
        except:
            pass

        return kafka_pull_is_ok
