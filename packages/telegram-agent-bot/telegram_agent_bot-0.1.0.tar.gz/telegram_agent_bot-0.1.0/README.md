Below is the updated README with the requested sections removed:

---

# Telegram Bot Creation Tool (For Gemini Agents Toolkit)

`telegram-agent-bot` helps you build and run Telegram chatbots backed by **agents developed using [Gemini Agents Toolkit](https://github.com/GeminiAgentsToolkit/gemini-agents-toolkit/blob/main/README.md)**. It provides a simple interface for defining these agents and exposing them through Telegram.

## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)

---

## Overview

`telegram-agent-bot` bridges Telegram’s Bot API and the Gemini Agents Toolkit. With minimal setup, you can:

- Create a Telegram bot out of your Gemini Agents Toolkit-based agent.
- Allow the agent to execute custom functions or tasks as defined in your Gemini Agents Toolkit configuration.
- Interact with your intelligent agent in real-time through Telegram conversations.

**Important:** This library only works with agents built on top of the [Gemini Agents Toolkit](https://github.com/GeminiAgentsToolkit/gemini-agents-toolkit/blob/main/README.md). It is not a general-purpose framework for any Gemini models; it specifically integrates with the Toolkit’s agent ecosystem.

---

## Requirements

- **Python 3.8+**
- **Gemini Agents Toolkit** configured properly, including a Google Cloud project with Vertex AI and billing enabled. For details, see the [Gemini Agents Toolkit README](https://github.com/GeminiAgentsToolkit/gemini-agents-toolkit/blob/main/README.md).
- **Telegram Bot Token:** Obtain one via [@BotFather](https://t.me/BotFather).

---

## Installation

Once you have your environment ready, simply install from PyPI:

```zsh
pip install telegram-agent-bot
```

---

## Configuration

Set the required environment variables for the Gemini Agents Toolkit:

```zsh
export GOOGLE_PROJECT=my-google-project
export GOOGLE_API_KEY=my-google-api-key
export GOOGLE_REGION=us-west1 # or another supported region if desired
```

Set your Telegram token either as an environment variable or pass it directly to the code:

```zsh
export TELEGRAM_TOKEN=your_telegram_bot_token
```

If you have custom modules or configurations for your agent, ensure they are on your `PYTHONPATH`:

```zsh
export PYTHONPATH=/path/to/gemini-agents-toolkit:$PYTHONPATH
```

---

## Usage

Here’s a basic example. The key method `create_agent_from_functions_list` originates from the [Gemini Agents Toolkit](https://github.com/GeminiAgentsToolkit/gemini-agents-toolkit/blob/main/README.md). Refer to that repo’s README for more detailed usage and advanced patterns.

```python
from telegram_agent_bot import start_agent_bot
from gemini_agents_toolkit import agent

def create_agent(on_message):
    return agent.create_agent_from_functions_list(
        model_name="gemini-flash-experimental",
        debug=True,
        system_instruction="You are a test agent. Respond concisely and helpfully.",
        on_message=on_message
    )

if __name__ == "__main__":
    start_agent_bot(
        telegram_token="YOUR_TELEGRAM_BOT_TOKEN",
        generate_agent_fn=create_agent
    )
```

Run it:

```zsh
python your_bot_launcher.py
```

Open Telegram and start interacting with your bot. The agent, powered by the Gemini Agents Toolkit, will handle user messages and respond accordingly.

---

## How It Works

1. **Telegram Integration:**  
   `start_agent_bot` uses `python-telegram-bot` to set up handlers for incoming text messages and commands, passing them seamlessly to the agent for processing.

2. **Gemini Agents Toolkit Integration:**  
   The `generate_agent_fn` callback creates a Gemini Agents Toolkit-based agent. The agent:
   - Interacts with Gemini models through Vertex AI.
   - Executes custom functions you define to provide dynamic responses or perform tasks.

3. **Conversation Flow:**
   - User messages arrive to the Telegram bot.
   - The bot forwards them to the agent’s `on_message` callback.
   - The agent responds using its LLM reasoning and custom functions.
   - The bot sends the agent’s response back to the user.

---

**Happy building!** With `telegram-agent-bot` and the Gemini Agents Toolkit, you can quickly create and deploy powerful LLM-driven agents directly to your Telegram users.