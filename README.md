# offensive-ai-tools

Skeleton for automating AI/chatbot pentesting workflows. Subclass `ChatInterface`
to wire up the target's HTTP/auth specifics, point the orchestrator at a JSON
dataset of test prompts, and let an LLM judge evaluate the responses.
