##################################kafka Feature configure#################################
from contextlib import asynccontextmanager
from kafka_client.producer import (
    SyncKafkaProducer,
    AsyncKafkaProducer,
)
###########################################################################################

from fastapi import FastAPI

from routes.student import router as student_router


#######################################kafka server start######################################
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Start both producers
    app.state.sync_kafka_producer = SyncKafkaProducer()

    app.state.async_kafka_producer = AsyncKafkaProducer()
    await app.state.async_kafka_producer.start()

    print("Kafka producers started")

    try:
        yield

    finally:
        # Stop both producers
        app.state.sync_kafka_producer.close()
        await app.state.async_kafka_producer.close()

        print("Kafka producers stopped")
###########################################and end############################################


app = FastAPI(
    title="Student Management API",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(student_router)