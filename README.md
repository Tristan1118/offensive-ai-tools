# offensive-ai-tools

A collection of tools for offensive AI work / AI pentesting.

## Tools

- [`promptprobe/`](./promptprobe) — skeleton for automating chatbot pentest
  workflows. Subclass an abstract `ChatInterface` per target, run a JSON
  dataset of prompts through it, and have an LLM judge evaluate the responses.
