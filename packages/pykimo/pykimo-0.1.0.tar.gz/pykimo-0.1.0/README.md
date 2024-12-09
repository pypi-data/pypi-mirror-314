# PyKimo

A lean and powerful AI chat agent library.

## Installation

bash
pip install pykimo

## Quick Start
python
from pykimo import KimoAgent
agent = KimoAgent("claude-3-sonnet")
response = agent.run_sync("Hello!")
print(response.data)
