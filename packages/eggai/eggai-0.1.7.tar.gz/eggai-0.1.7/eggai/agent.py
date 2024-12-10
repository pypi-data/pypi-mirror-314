import asyncio
import json
from typing import Dict, List, Callable

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from eggai.constants import DEFAULT_CHANNEL_NAME
from eggai.settings.kafka import KafkaSettings

class Agent:
    """
    A message-based agent for subscribing to events and handling messages with user-defined functions.
    """

    def __init__(self, name: str):
        """
        Initialize the Agent.

        Args:
            name (str): The name of the agent.
        """
        self.name = name
        self.kafka_settings = KafkaSettings()
        self._producer = None
        self._consumer = None
        self._handlers: Dict[str, List[Callable]] = {}  # Maps channel:event_name to list of handlers
        self._channels = set()  # Keep track of all subscribed channels
        self._running_task = None  # Task to manage the lifecycle of the agent

    def subscribe(self, event_name: str, channel_name: str = DEFAULT_CHANNEL_NAME):
        """
        Decorator for subscribing to a channel and binding a handler to an event name.

        Args:
            event_name (str): Name of the event within the channel.
            channel_name (str): The name of the channel.

        Returns:
            Callable: The decorator for wrapping the handler function.
        """
        def decorator(func: Callable):
            topic_event = f"{channel_name}:{event_name}"
            if topic_event not in self._handlers:
                self._handlers[topic_event] = []
            self._handlers[topic_event].append(func)  # Allow multiple handlers for the same event
            self._channels.add(channel_name)  # Register the channel name
            return func
        return decorator

    async def _start_producer(self):
        """
        Start the message producer.
        """
        if self._producer is None:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.kafka_settings.BOOTSTRAP_SERVERS
            )
            await self._producer.start()

    async def _start_consumer(self):
        """
        Start the message consumer and process incoming messages.
        """
        if self._consumer is None:
            self._consumer = AIOKafkaConsumer(
                *self._channels,  # Use the registered channels
                bootstrap_servers=self.kafka_settings.BOOTSTRAP_SERVERS,
                group_id=f"{self.name}_group",
                auto_offset_reset="latest",
            )
            await self._consumer.start()

    async def _handle_messages(self):
        try:
            async for msg in self._consumer:
                channel_name = msg.topic
                try:
                    message = json.loads(msg.value.decode("utf-8"))
                    event_name = message.get("event_name")
                    payload = message.get("payload")

                    topic_event = f"{channel_name}:{event_name}"
                    if topic_event in self._handlers:
                        # Call all handlers for this event
                        for handler in self._handlers[topic_event]:
                            await handler(payload)
                except Exception as e:
                    print(f"Failed to process message from {channel_name}: {e}")
        except asyncio.CancelledError:
            pass
        finally:
            print(f"Stopping agent '{self.name}'...")
            await self._consumer.stop()
            print(f"Agent '{self.name}' stopped.")

    async def run(self):
        """
        Start the agent by initializing the producer and consumer, then handling messages.
        """
        if self._running_task:
            raise RuntimeError("Agent is already running.")
        await self._start_producer()
        await self._start_consumer()
        self._running_task = asyncio.create_task(self._handle_messages())

    async def stop(self):
        """
        Stop the agent gracefully by cancelling the running task.
        """
        if not self._running_task:
            raise RuntimeError("Agent is not running.")
        await self._producer.stop()
        self._running_task.cancel()
        try:
            await self._running_task
        except asyncio.CancelledError:
            pass
