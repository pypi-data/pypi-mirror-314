# EggAI Multi-Agent Framework 🤖

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge&logo=github&logoColor=white)](https://github.com/eggai-tech/eggai/pulls)
[![GitHub Issues](https://img.shields.io/github/issues/eggai-tech/eggai?style=for-the-badge&logo=github&logoColor=white)](https://github.com/eggai-tech/eggai/issues)
[![GitHub Stars](https://img.shields.io/github/stars/eggai-tech/eggai?style=for-the-badge&logo=github&logoColor=white)](https://github.com/eggai-tech/eggai/stargazers)

`EggAI Multi-Agent Framework` is an async-first framework for building, deploying, and scaling multi-agent systems for modern enterprise environments.

## Table of Contents

[Features](#-features) •
[Overview](#-overview) •
[System Architecture](#-system-architecture) •
[Installation](#-installation) •
[Getting Started](#-getting-started) •
[Core Concepts](#-core-concepts) •
[Examples](#-examples) •
[Contribution](#-contribution) •
[License](#-license)

## 🌟 Features

- 🤖 **Agent Management**: Simplify the orchestration and execution of multi-agent systems.
- 🚀 **Async-First**: Push-based APIs designed for high-concurrency, long-running AI workflows, and real-time processes.
- ⚡ **Event-Driven**: Enable real-time reactions to events for dynamic and responsive systems.
- 📈 **Horizontally Scalable**: Scale agent execution seamlessly to meet growing demands.
- 🚇 **Kafka Integration**: Native support for Kafka topics ensures seamless streaming and messaging.
- 🛠 **Flexible Architecture**: Easily adapt or extend components without disrupting workflows.
- 🔄 **Resilient by Design**: Built-in retry mechanisms and fault tolerance for production-grade robustness.

## 📖 Overview

`EggAI Multi-Agent Framework` provides the `eggai` Python library that simplifies the development of multi-agent systems.
It allows developers to focus on business logic while handling the complexities of distributed systems.

## 🏗️ System Architecture

![System Architecture](./docs/assets/system-architecture.svg)

1. **Human Interaction**:

   - Users interact with the system via various **Human Channels**, such as chat interfaces or APIs, which are routed through the **Gateway**.

2. **Gateway**:

   - The Gateway acts as the entry point for all human communications and interfaces with the system to ensure secure and consistent message delivery.

3. **Coordinator**:

   - The **Coordinator** is the central component that manages the communication between humans and specialized agents.
   - It determines which agent(s) to involve and facilitates the interaction through the **Agent Channels**.

4. **Agents**:

   - The system is composed of multiple specialized agents (Agent 1, Agent 2, Agent 3), each responsible for handling specific types of tasks or functions.
   - Agents communicate with the Coordinator through their respective **Agent Channels**, ensuring scalability and modularity.

5. **Agent and Human Channels**:
   - **Human Channels** connect the Gateway to humans for interaction.
   - **Agent Channels** connect the Coordinator to agents, enabling task-specific processing and delegation.

## 📦 Installation

Install `EggAI` via pip:

```bash
pip install eggai
```

## 🚀 Getting Started

Here's how you can quickly set up an agent to handle events in an event-driven system:

```python
import asyncio

from eggai.agent import Agent
from eggai.channel import Channel

agent = Agent("OrderAgent")
channel = Channel()

@agent.subscribe(event_name="order_requested")
async def handle_order_requested(event):
    print(f"[ORDER AGENT]: Received order request. Event: {event}")
    await channel.publish({"event_name": "order_created", "payload": event})

@agent.subscribe(event_name="order_created")
async def handle_order_created(event):
    print(f"[ORDER AGENT]: Order created. Event: {event}")

async def main():
    await agent.run()
    await channel.publish({
        "event_name": "order_requested",
        "payload": {
            "product": "Laptop",
            "quantity": 1
        }
    })

    try:
        print("Agent is running. Press Ctrl+C to stop.")
        await asyncio.Event().wait()
    except asyncio.exceptions.CancelledError:
        print("Task was cancelled. Cleaning up...")
    finally:
        # Clean up resources
        await agent.stop()
        await channel.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

This code demonstrates how to define an `Agent` and use it to process events from Kafka topics.

This repository contains a few applications you can use as a reference:

## 💡 Core Concepts

### 🤖 Agent

An `Agent` is responsible for subscribing to Kafka topics, processing events, and orchestrating tasks using user-defined handlers. The key features of the `Agent` class include:

- **Event Subscription**: Bind event handlers to specific events using the `subscribe` decorator.
- **Lifecycle Management**: Manage producer and consumer lifecycles seamlessly.
- **Minimal Boilerplate**: Focus on business logic without worrying about Kafka details.

### 🚇 Channel

A `Channel` abstracts the Kafka producer interface to publish events to specific Kafka topics. Key features include:

- **Event Publishing**: Send events to Kafka topics easily.
- **Singleton Producers**: Manage Kafka producers efficiently across multiple channels.

## 👀 Examples

For detailed examples, please refer to [examples](examples).

## 🤝 Contribution

`EggAI Multi-Agent Framework` is open-source and we welcome contributions. If you're looking to contribute, please refer to [CONTRIBUTING.md](CONTRIBUTING.md).

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
