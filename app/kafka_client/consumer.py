import json
from kafka import KafkaConsumer

consumer  = KafkaConsumer(
    "students",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="student-consumer-group",

    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)