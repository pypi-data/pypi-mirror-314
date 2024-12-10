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
        self.producer = None
        self.consumer = None
        self.handlers: Dict[str, List[Callable]] = {}  # Maps channel:event_name to list of handlers
        self.channels = set()  # Keep track of all subscribed channels
        self.running_task = None  # Task to manage the lifecycle of the agent

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
            if topic_event not in self.handlers:
                self.handlers[topic_event] = []
            self.handlers[topic_event].append(func)  # Allow multiple handlers for the same event
            self.channels.add(channel_name)  # Register the channel name
            return func
        return decorator

    async def _start_producer(self):
        """
        Start the message producer.
        """
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.kafka_settings.BOOTSTRAP_SERVERS
        )
        await self.producer.start()

    async def _start_consumer(self):
        """
        Start the message consumer and process incoming messages.
        """
        self.consumer = AIOKafkaConsumer(
            *self.channels,  # Use the registered channels
            bootstrap_servers=self.kafka_settings.BOOTSTRAP_SERVERS,
            #group_id=f"{self.name}_group",
            auto_offset_reset="latest",
        )
        await self.consumer.start()

        print(f"Agent '{self.name}' is ready to receive messages. Channels: {self.channels}")

        try:
            async for msg in self.consumer:
                channel_name = msg.topic
                try:
                    message = json.loads(msg.value.decode("utf-8"))
                    event_name = message.get("event_name")
                    payload = message.get("payload")

                    topic_event = f"{channel_name}:{event_name}"
                    if topic_event in self.handlers:
                        # Call all handlers for this event
                        for handler in self.handlers[topic_event]:
                            await handler(payload)
                except Exception as e:
                    print(f"Failed to process message from {channel_name}: {e}")
        except asyncio.CancelledError:
            pass
        finally:
            print(f"Stopping agent '{self.name}'...")
            await self.consumer.stop()
            print(f"Agent '{self.name}' stopped.")

    async def _lifecycle(self):
        """
        Internal lifecycle management for the agent.
        """
        try:
            await self._start_producer()
            await self._start_consumer()
        finally:
            await self.producer.stop()

    async def run(self):
        """
        Run the agent lifecycle, blocking until it is stopped.
        """
        if self.running_task:
            raise RuntimeError("Agent is already running.")
        try:
            self.running_task = asyncio.create_task(self._lifecycle())
            await self.running_task  # Block until the lifecycle completes
        except asyncio.CancelledError:
            print("Agent lifecycle was cancelled.")
        finally:
            self.running_task = None

    async def stop(self):
        """
        Stop the agent gracefully by cancelling the running task.
        """
        if not self.running_task:
            raise RuntimeError("Agent is not running.")
        self.running_task.cancel()
        try:
            await self.running_task  # Ensure the task finishes
        except asyncio.CancelledError:
            pass  # Task was cancelled
