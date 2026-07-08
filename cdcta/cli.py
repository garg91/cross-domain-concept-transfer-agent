from __future__ import annotations

import argparse
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .agent import CrossDomainConceptTransferAgent


def render_output(result) -> None:
    console = Console()
    console.rule("Cross-Domain Concept Transfer Agent")
    console.print(f"[bold]Problem:[/bold] {result.original_problem}")
    console.print(f"[bold]Core question:[/bold] {result.core_question}")
    console.print(f"[bold]Domain:[/bold] {result.domain}")

    table = Table(title="Variables")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Description")
    for v in result.variables:
        table.add_row(v.name, v.type, v.description)
    console.print(table)

    rel_table = Table(title="Relationships")
    rel_table.add_column("Source")
    rel_table.add_column("Relation")
    rel_table.add_column("Target")
    for r in result.relationships:
        rel_table.add_row(r.source, r.relation, r.target)
    console.print(rel_table)

    console.print("[bold]Abstract schema:[/bold]")
    console.print(f"  {result.abstract_schema.name}: {result.abstract_schema.description}")
    console.print(f"  Pattern: {result.abstract_schema.pattern}")

    sim_table = Table(title="Similar Schemas")
    sim_table.add_column("Domain")
    sim_table.add_column("Schema")
    sim_table.add_column("Transferable mechanisms")
    for s in result.similar_schemas:
        sim_table.add_row(s.domain, s.schema_name, ", ".join(s.transferable_mechanisms))
    console.print(sim_table)

    idea_table = Table(title="Transferred Ideas")
    idea_table.add_column("Score")
    idea_table.add_column("Source")
    idea_table.add_column("Mechanism")
    idea_table.add_column("Application")
    for idea in result.transferred_ideas:
        idea_table.add_row(str(idea.score), idea.source_domain, idea.imported_mechanism, idea.target_domain_application)
    console.print(idea_table)

    ver_table = Table(title="Verification Plan")
    ver_table.add_column("Test")
    ver_table.add_column("Method")
    ver_table.add_column("Metric")
    ver_table.add_column("Success")
    for step in result.verification_plan:
        ver_table.add_row(step.test_name, step.method, step.metric, step.success_condition)
    console.print(ver_table)

    console.print(f"[bold]Best next step:[/bold] {result.best_next_step}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Cross-Domain Concept Transfer Agent MVP")
    parser.add_argument("problem", help="User problem to analyze")
    parser.add_argument("--json", dest="json_path", help="Optional path to save JSON output")
    args = parser.parse_args()

    agent = CrossDomainConceptTransferAgent()
    result = agent.run(args.problem)
    render_output(result)

    if args.json_path:
        path = Path(args.json_path)
        path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
        print(f"Saved JSON to {path}")


if __name__ == "__main__":
    main()
