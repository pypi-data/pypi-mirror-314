import asyncio
import json
from aiokafka import AIOKafkaProducer

from eggai.constants import DEFAULT_CHANNEL_NAME
from eggai.settings.kafka import KafkaSettings


class Channel:
    """
    A standalone class to send events to Kafka channels.
    """

    _producers = {}  # Singleton dictionary to hold producers for each channel

    def __init__(self, name: str = DEFAULT_CHANNEL_NAME):
        """
        Initialize the Channel.

        Args:
            name (str): The name of the Kafka channel (topic).
        """
        self.name = name
        self.kafka_settings = KafkaSettings()

    async def _get_producer(self):
        """
        Get or create a Kafka producer for the channel.

        Returns:
            AIOKafkaProducer: Kafka producer for the channel.
        """
        if self.name not in Channel._producers:
            producer = AIOKafkaProducer(
                bootstrap_servers=self.kafka_settings.BOOTSTRAP_SERVERS,
            )
            await producer.start()
            Channel._producers[self.name] = producer
        return Channel._producers[self.name]

    async def publish(self, event: dict):
        """
        Publish an event to the Kafka channel.

        Args:
            event (dict): The event payload.
        """
        producer = await self._get_producer()
        await producer.send_and_wait(self.name, json.dumps(event).encode("utf-8"))

    @staticmethod
    async def stop():
        """
        Close all Kafka producers in the singleton list.
        """
        for producer in Channel._producers.values():
            await producer.stop()
        Channel._producers.clear()