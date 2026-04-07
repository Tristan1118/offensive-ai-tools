"""Example entry point. Copy or edit this for each engagement to wire up your
concrete ChatInterface subclass."""

import argparse
import sys
from pathlib import Path

# Make the examples/ dir importable when running from the repo root.
sys.path.insert(0, str(Path(__file__).parent / "examples"))

from ai_pentest.judge import AnthropicJudge
from ai_pentest.orchestrator import Orchestrator
from echo_target import EchoTarget


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an AI pentest workflow")
    parser.add_argument("--dataset", default="examples/example_prompts.json")
    parser.add_argument("--results", default="results/run.jsonl")
    parser.add_argument("--judge-model", default="claude-opus-4-6")
    args = parser.parse_args()

    chat = EchoTarget()
    judge = AnthropicJudge(model=args.judge_model)
    Orchestrator(chat, judge, args.dataset, args.results).run()


if __name__ == "__main__":
    main()
