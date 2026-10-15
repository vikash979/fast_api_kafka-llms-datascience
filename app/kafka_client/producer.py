# import json

# from kafka import KafkaProducer, KafkaConsumer


# producer = KafkaProducer(
#     bootstrap_servers=["localhost:9092"],
#     value_serializer=lambda value: json.dumps(value).encode("utf-8")
# )


# def publish_student_event(student: dict):
#     producer.send("students", student)
#     producer.flush()

# def close_sync_producer():
#     producer.close()

import asyncio
import json
import logging

from kafka import KafkaProducer, KafkaConsumer
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer


logger = logging.getLogger(__name__)

BOOTSTRAP_SERVERS = "localhost:9092"
STUDENTS_TOPIC = "students"


# ==========================================================
# 1. SYNCHRONOUS KAFKA PRODUCER
# ==========================================================

class SyncKafkaProducer:

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=[BOOTSTRAP_SERVERS],
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
            acks="all",
            retries=5,
            max_block_ms=10000,
        )

    def publish_student_event(self, student: dict):
        try:
            future = self.producer.send(
                STUDENTS_TOPIC,
                value=student,
            )

            # Wait for this message's result
            metadata = future.get(timeout=10)

            logger.info(
                "Student event published: topic=%s partition=%s offset=%s",
                metadata.topic,
                metadata.partition,
                metadata.offset,
            )

            return metadata

        except Exception:
            logger.exception("Failed to publish student event")
            raise

    def flush(self):
        self.producer.flush(timeout=10)

    def close(self):
        self.producer.close(timeout=10)


# ==========================================================
# 2. ASYNCHRONOUS KAFKA PRODUCER
# ==========================================================

class AsyncKafkaProducer:

    def __init__(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
            acks="all",
            request_timeout_ms=10000,
        )

        self.started = False

    async def start(self):
        if not self.started:
            await self.producer.start()
            self.started = True
            logger.info("Async Kafka Producer started")

    async def publish_student_event(self, student: dict):
        if not self.started:
            raise RuntimeError("Async Kafka Producer is not started")

        try:
            metadata = await self.producer.send_and_wait(
                STUDENTS_TOPIC,
                value=student,
            )

            logger.info(
                "Student event published: topic=%s partition=%s offset=%s",
                metadata.topic,
                metadata.partition,
                metadata.offset,
            )

            return metadata

        except Exception:
            logger.exception("Failed to publish student event")
            raise

    async def close(self):
        if self.started:
            await self.producer.stop()
            self.started = False
            logger.info("Async Kafka Producer stopped")


# ==========================================================
# 3. SYNCHRONOUS KAFKA CONSUMER
# ==========================================================

def consume_student_events_sync():
    consumer = KafkaConsumer(
        STUDENTS_TOPIC,
        bootstrap_servers=[BOOTSTRAP_SERVERS],
        group_id="student-sync-consumer",
        auto_offset_reset="latest",
        enable_auto_commit=False,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    logger.info("Sync Consumer started")

    try:
        for message in consumer:
            student = message.value

            try:
                logger.info("Student event received: %s", student)

                # Add your message-processing logic here.

                # Commit only after successful processing
                consumer.commit()

            except Exception:
                logger.exception("Student event processing failed")
                # Do not commit a failed message.

    except KeyboardInterrupt:
        logger.info("Sync Consumer interrupted")

    finally:
        consumer.close()
        logger.info("Sync Consumer stopped")


# ==========================================================
# 4. ASYNCHRONOUS KAFKA CONSUMER
# ==========================================================

async def consume_student_events_async():
    consumer = AIOKafkaConsumer(
        STUDENTS_TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id="student-async-consumer",
        auto_offset_reset="latest",
        enable_auto_commit=False,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    await consumer.start()
    logger.info("Async Consumer started")

    try:
        async for message in consumer:
            student = message.value

            try:
                logger.info("Student event received: %s", student)

                # Add your asynchronous processing logic here.
                # For example:
                # await process_student_event(student)

                await consumer.commit()

            except Exception:
                logger.exception("Student event processing failed")
                # Do not commit a failed message.

    finally:
        await consumer.stop()
        logger.info("Async Consumer stopped")


# ==========================================================
# 5. RUN CONSUMER FROM COMMAND LINE
# ==========================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--consumer",
        choices=["sync", "async"],
        required=True,
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    if args.consumer == "sync":
        consume_student_events_sync()
    else:
        asyncio.run(consume_student_events_async())