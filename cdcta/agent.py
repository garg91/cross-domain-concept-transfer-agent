from __future__ import annotations

import re
from collections import Counter
from typing import Dict, List, Tuple

from .domain_knowledge import (
    DOMAIN_KEYWORDS,
    TRANSFER_TEMPLATES,
    relationships_for,
    variables_for,
    verification_for,
)
from .models import (
    AbstractSchema,
    ConceptTransferOutput,
    SimilarDomainSchema,
    TransferredIdea,
)
from .schema_library import SCHEMA_LIBRARY


def normalize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9_+-]+", text.lower())


class CrossDomainConceptTransferAgent:
    """Rule-based MVP for schema-guided cross-domain concept transfer.

    This implementation is intentionally transparent and easy to replace with
    LLM/embedding/graph components later.
    """

    def __init__(self, top_k_schemas: int = 5):
        self.top_k_schemas = top_k_schemas

    def run(self, user_problem: str) -> ConceptTransferOutput:
        domain = self.detect_domain(user_problem)
        core_question = self.extract_core_question(user_problem, domain)
        variables = variables_for(domain)
        relationships = relationships_for(domain)
        schema_record = self.select_schema(user_problem, domain)
        abstract_schema = AbstractSchema(
            name=schema_record["name"],
            description=schema_record["description"],
            pattern=schema_record["structure"],
            reusable_structure=schema_record["structure"],
        )
        similar_schemas = self.retrieve_similar_schemas(schema_record, domain)
        transferred_ideas = self.generate_transferred_ideas(domain, similar_schemas)
        verification_plan = verification_for(domain)
        best_next_step = self.choose_best_next_step(domain, transferred_ideas)

        return ConceptTransferOutput(
            original_problem=user_problem,
            core_question=core_question,
            domain=domain,
            variables=variables,
            relationships=relationships,
            abstract_schema=abstract_schema,
            similar_schemas=similar_schemas,
            transferred_ideas=transferred_ideas,
            verification_plan=verification_plan,
            best_next_step=best_next_step,
        )

    def detect_domain(self, problem: str) -> str:
        tokens = normalize(problem)
        text = " ".join(tokens)
        scores: Dict[str, int] = {}
        for domain, keywords in DOMAIN_KEYWORDS.items():
            score = 0
            for kw in keywords:
                kw_norm = kw.lower()
                if " " in kw_norm:
                    if kw_norm in problem.lower():
                        score += 3
                elif kw_norm in tokens:
                    score += 2
                elif kw_norm in text:
                    score += 1
            scores[domain] = score
        best_domain, best_score = max(scores.items(), key=lambda kv: kv[1])
        return best_domain if best_score > 0 else "AI agents"

    def extract_core_question(self, problem: str, domain: str) -> str:
        cleaned = problem.strip().rstrip(".")
        if cleaned.endswith("?"):
            return cleaned
        domain_goal = {
            "compression": "How can we select the best compression strategy for each data region under size, speed, and overhead constraints?",
            "trading": "How can we adapt strategy selection to changing market regimes while controlling risk and cost?",
            "materials": "How can we find candidate materials that satisfy target properties while remaining stable and synthesizable?",
            "algorithms": "How can we exploit structure, representation, or symmetry to reduce problem complexity?",
            "operating systems": "How can we choose resource-allocation policies that improve throughput, latency, and fairness?",
            "databases": "How can we estimate and select the best execution plan before running an expensive query?",
            "medicine": "How can we select interventions based on patient subtype while preserving safety?",
            "robotics": "How can a robot adapt its policy to environment state and uncertainty?",
            "compiler optimization": "How can we choose optimization passes based on program structure and hardware constraints?",
            "AI agents": "How can an agent route tasks to tools or models under uncertainty, cost, and verification constraints?",
        }
        return domain_goal.get(domain, f"How can this {domain} problem be represented, transferred, and verified?")

    def select_schema(self, problem: str, domain: str) -> dict:
        tokens = Counter(normalize(problem))
        best: Tuple[int, dict] = (-1, SCHEMA_LIBRARY[0])
        for schema in SCHEMA_LIBRARY:
            score = 0
            if domain in schema["domains"]:
                score += 5
            schema_text = " ".join([schema["name"], schema["description"], schema["structure"], " ".join(schema["domains"])]).lower()
            for tok, count in tokens.items():
                if tok in schema_text:
                    score += count
            if score > best[0]:
                best = (score, schema)
        return best[1]

    def retrieve_similar_schemas(self, selected_schema: dict, target_domain: str) -> List[SimilarDomainSchema]:
        results: List[SimilarDomainSchema] = []
        for schema in SCHEMA_LIBRARY:
            shared_mechanisms = set(selected_schema.get("mechanisms", [])) & set(schema.get("mechanisms", []))
            structural_overlap = self._token_overlap(selected_schema["structure"], schema["structure"])
            score = len(shared_mechanisms) * 2 + structural_overlap
            if schema["name"] == selected_schema["name"]:
                score += 3
            if score <= 0:
                continue
            for domain in schema["domains"]:
                if domain == target_domain:
                    continue
                results.append(
                    SimilarDomainSchema(
                        domain=domain,
                        schema_name=schema["name"],
                        similarity_reason=f"Shares the structure: {schema['structure']}",
                        transferable_mechanisms=schema.get("mechanisms", [])[:4],
                    )
                )
        # Deduplicate by domain while keeping first/best occurrence.
        dedup: Dict[str, SimilarDomainSchema] = {}
        for item in results:
            dedup.setdefault(item.domain, item)
        return list(dedup.values())[: self.top_k_schemas]

    def generate_transferred_ideas(self, target_domain: str, similar_schemas: List[SimilarDomainSchema]) -> List[TransferredIdea]:
        ideas: List[TransferredIdea] = []
        for idx, similar in enumerate(similar_schemas):
            source_domain = similar.domain
            mechanism = self._mechanism_for_source(source_domain, similar)
            application = self._translate_mechanism(target_domain, source_domain, mechanism)
            benefit = self._expected_benefit(target_domain, mechanism)
            risk = self._risk(target_domain, mechanism)
            score = round(max(0.55, 0.95 - 0.07 * idx), 2)
            ideas.append(
                TransferredIdea(
                    source_domain=source_domain,
                    imported_mechanism=mechanism,
                    target_domain_application=application,
                    expected_benefit=benefit,
                    risk_or_limitation=risk,
                    score=score,
                )
            )
        return ideas

    def choose_best_next_step(self, domain: str, ideas: List[TransferredIdea]) -> str:
        if not ideas:
            return "Create a small benchmark and manually compare at least two candidate strategies."
        top = ideas[0]
        domain_steps = {
            "compression": "Implement a small feature extractor plus routing baseline, then compare it against fixed compressors and an oracle on your existing dataset.",
            "trading": "Build an out-of-sample regime-labeling/backtest notebook before adding any live trading logic.",
            "materials": "Define 5-20 candidate structures and run the cheapest stability/property screening available before deeper simulations.",
            "algorithms": "Identify invariants/equivalence classes and compare a reduced solver against brute force on small cases.",
            "operating systems": "Create a workload simulator and compare a simple adaptive scheduler against FIFO/round-robin baselines.",
            "databases": "Collect query-plan features, estimate costs, and compare chosen plans against actual runtimes.",
            "medicine": "Use only validated retrospective/public data first; measure subgroup performance and safety metrics.",
            "robotics": "Test the transferred policy in simulation across controlled environment variations before real hardware.",
            "compiler optimization": "Run a benchmark suite with a pass-selection baseline and compare runtime, compile time, and binary size.",
            "AI agents": "Build a task-routing eval set and compare rule-based routing, LLM routing, and oracle routing.",
        }
        return domain_steps.get(domain, f"Prototype the idea from {top.source_domain}: {top.imported_mechanism}")

    def _mechanism_for_source(self, source_domain: str, similar: SimilarDomainSchema) -> str:
        if source_domain in TRANSFER_TEMPLATES:
            return TRANSFER_TEMPLATES[source_domain]
        if similar.transferable_mechanisms:
            return similar.transferable_mechanisms[0]
        return "Transfer the source domain's policy-selection mechanism."

    def _translate_mechanism(self, target_domain: str, source_domain: str, mechanism: str) -> str:
        translations = {
            "compression": {
                "database query planning": "Sample each chunk, estimate compressed size/time for candidate compressors, then choose the lowest expected cost before full compression.",
                "mixture-of-experts": "Train a lightweight gating model that routes chunks to specialized compressor experts.",
                "operating systems": "Treat compression time, decompression time, memory, and size as schedulable resources with fallback policies.",
                "trading": "Detect distribution shifts inside large files and switch compression policy at regime boundaries.",
                "medicine": "Classify chunks into subtypes and apply subtype-specific compression policies rather than a global default.",
            },
            "trading": {
                "compression": "Treat market windows like heterogeneous chunks: extract features, infer regime, and route to strategy experts.",
                "medicine": "Use subtype-specific policy logic: different market regimes receive different risk controls.",
                "robotics": "Use feedback control to reduce exposure when observed error/drawdown exceeds expectation.",
            },
            "materials": {
                "drug design": "Search for structures that stabilize a desired fragile configuration while preserving target functionality.",
                "structural engineering": "Use host frameworks or internal stress distribution to replace costly external constraints.",
                "compiler optimization": "Use staged candidate transformations and reject candidates that violate stability constraints.",
            },
            "algorithms": {
                "polynomial solving": "Find transformations that preserve the problem and collapse equivalent states before solving.",
                "physics": "Use invariants to reduce the number of degrees of freedom in the search.",
                "robotics": "Canonicalize equivalent states so planning does not repeat symmetric work.",
            },
            "AI agents": {
                "database query planning": "Estimate tool cost and success probability before selecting a tool chain.",
                "operating systems": "Schedule tool calls under latency, cost, and priority constraints.",
                "medicine": "Triage tasks by risk and route high-risk tasks to stronger verification.",
                "compression": "Break large tasks into chunks and route each chunk to the best model/tool.",
            },
        }
        return translations.get(target_domain, {}).get(
            source_domain,
            f"Adapt this mechanism to {target_domain}: {mechanism}",
        )

    def _expected_benefit(self, target_domain: str, mechanism: str) -> str:
        if target_domain == "compression":
            return "Better size/time tradeoff by matching each chunk to the most suitable policy."
        if target_domain == "trading":
            return "Lower risk of applying the wrong strategy during a changed market regime."
        if target_domain == "materials":
            return "More systematic candidate generation and earlier rejection of unstable designs."
        if target_domain == "algorithms":
            return "Reduced search complexity while preserving correctness."
        if target_domain == "AI agents":
            return "Higher task success with lower unnecessary tool cost and better verification."
        return "Improves decision quality by matching policy to observed structure and constraints."

    def _risk(self, target_domain: str, mechanism: str) -> str:
        if target_domain == "medicine":
            return "High-stakes domain: any generated policy requires clinical validation and regulatory review."
        if target_domain == "trading":
            return "Backtest overfitting and transaction costs can erase apparent gains."
        if target_domain == "materials":
            return "Simulation proxies may miss synthesis constraints or real-world stability."
        if target_domain == "compression":
            return "Routing metadata and classifier errors may erase compression gains."
        return "The analogy may be structurally incomplete; verify against domain-specific baselines."

    def _token_overlap(self, a: str, b: str) -> int:
        return len(set(normalize(a)) & set(normalize(b)))
