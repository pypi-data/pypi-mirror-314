# Sophy

A simple Slack notification utility.

## Installation

```bash
pip install sophy-python
```

## Usage

```python
from sophy import Slackbot

# Set SLACK_TOKEN environment variable first
bot = Slackbot('user@example.com')
bot.notify('Hello from Sophy!')
```
