"""Trivial ChatInterface for smoke-testing the skeleton.

Does not implement multi-turn, so multi-turn cases get skipped by the
orchestrator. Echoes the prompt back as the "response".
"""

from ai_pentest.chat_interface import ChatInterface


class EchoTarget(ChatInterface):
    def send_single_turn(self, prompt: str) -> str:
        return f"[echo] {prompt}"
