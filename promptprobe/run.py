"""Generic entry point. Picks the target ChatInterface subclass dynamically so
engagement-specific code can live outside this file (typically in `targets/`,
which is gitignored)."""

import argparse
import importlib
import sys
from pathlib import Path

from ai_pentest.chat_interface import ChatInterface
from ai_pentest.judge import AnthropicJudge
from ai_pentest.orchestrator import Orchestrator


def load_target(spec: str) -> ChatInterface:
    """Load a ChatInterface subclass from a 'module.path:ClassName' spec."""
    if ":" not in spec:
        raise ValueError(f"--target must be 'module.path:ClassName', got {spec!r}")
    module_path, class_name = spec.split(":", 1)
    module = importlib.import_module(module_path)
    cls = getattr(module, class_name)
    instance = cls()
    if not isinstance(instance, ChatInterface):
        raise TypeError(f"{spec} is not a ChatInterface subclass")
    return instance


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an AI pentest workflow")
    parser.add_argument(
        "--target",
        default="examples.echo_target:EchoTarget",
        help="Target ChatInterface as 'module.path:ClassName' "
             "(e.g. 'targets.acme:AcmeChat')",
    )
    parser.add_argument("--dataset", default="examples/example_prompts.json")
    parser.add_argument("--results", default="results/run.jsonl")
    parser.add_argument("--judge-model", default="claude-opus-4-6")
    args = parser.parse_args()

    # Make sibling dirs importable so users can put targets in ./targets/ etc.
    sys.path.insert(0, str(Path(__file__).parent))

    chat = load_target(args.target)
    judge = AnthropicJudge(model=args.judge_model)
    Orchestrator(chat, judge, args.dataset, args.results).run()


if __name__ == "__main__":
    main()
