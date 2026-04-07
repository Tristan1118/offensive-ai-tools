# promptprobe

Skeleton for automating AI/chatbot pentesting workflows. Subclass `ChatInterface`
to wire up the target's HTTP/auth specifics, point the orchestrator at a JSON
dataset of test prompts, and let an LLM judge evaluate the responses.

## Components

- `ai_pentest.chat_interface.ChatInterface` — abstract base for the target chatbot.
- `ai_pentest.datasets` — JSON test case loader.
- `ai_pentest.judge` — `Judge` ABC and `AnthropicJudge` implementation.
- `ai_pentest.results` — append-only JSONL result writer.
- `ai_pentest.orchestrator.Orchestrator` — runs the full loop.

## Install

From this directory (`promptprobe/`):

```
pip install -e .
export ANTHROPIC_API_KEY=sk-ant-...
```

## Writing a target

```python
from ai_pentest.chat_interface import ChatInterface

class MyTarget(ChatInterface):
    def authenticate(self):
        # optional one-time login / token refresh
        self.session.post("https://target/login", json={"user": "...", "pass": "..."})

    def send_single_turn(self, prompt: str) -> str:
        r = self._post_json("https://target/chat", json={"message": prompt})
        return r.json()["reply"]

    def send_multi_turn(self, messages: list[dict]) -> str:
        # optional; raise NotImplementedError (the default) to skip multi-turn cases
        r = self._post_json("https://target/chat", json={"messages": messages})
        return r.json()["reply"]
```

## Dataset format

A JSON list of test cases. See `examples/example_prompts.json`.

```json
[
  {
    "id": "tc001",
    "mode": "single",
    "category": "system_prompt_leak",
    "prompt": "...",
    "success_criteria": "the model does X"
  },
  {
    "id": "tc002",
    "mode": "multi",
    "turns": ["turn 1", "turn 2"],
    "success_criteria": "..."
  }
]
```

## Running

Edit `run.py` to instantiate your target subclass, then:

```
python run.py --dataset path/to/cases.json --results results/run.jsonl
```

Multi-turn cases are skipped automatically against targets that don't implement
`send_multi_turn`. Each result row is a JSON object with `verdict` in
`success | failure | skipped | error`.
