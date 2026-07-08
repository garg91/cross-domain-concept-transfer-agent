from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cdcta.agent import CrossDomainConceptTransferAgent

PROBLEMS = {
    "compression": "How can I improve adaptive compression by choosing different compressors for different file chunks?",
    "trading": "How can a trading system adapt its strategy when market behavior changes?",
    "materials": "How can we discover a stable high-temperature superconductor at lower pressure?",
    "algorithms": "How can symmetry reduce the complexity of solving a polynomial or search problem?",
    "operating systems": "How should an operating system schedule tasks with different CPU, I/O, memory, and latency needs?",
    "databases": "How can a database choose the best query execution plan before running the query?",
    "medicine": "How can treatment be personalized for different patient subtypes while preserving safety?",
    "robotics": "How can a robot adapt its behavior across different environments and uncertainty levels?",
    "compiler optimization": "How can a compiler choose the best optimization strategy for different code sections?",
    "AI agents": "How can an AI agent choose the right tool or model for a user task?",
}


def main() -> None:
    agent = CrossDomainConceptTransferAgent()
    outputs = {}
    for name, problem in PROBLEMS.items():
        result = agent.run(problem)
        outputs[name] = json.loads(result.model_dump_json())
        print(f"{name:22s} -> {result.abstract_schema.name:55s} | ideas: {len(result.transferred_ideas)}")

    out_path = Path(__file__).parent / "sample_outputs.json"
    out_path.write_text(json.dumps(outputs, indent=2), encoding="utf-8")
    print(f"\nSaved outputs to {out_path}")


if __name__ == "__main__":
    main()
