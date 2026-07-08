from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class Variable(BaseModel):
    name: str
    description: str
    type: str = Field(description="measurable, hidden, controllable, constraint, or output")
    examples: List[str] = Field(default_factory=list)


class Relationship(BaseModel):
    source: str
    target: str
    relation: str
    direction: str = "source_to_target"
    confidence: float = 0.7


class AbstractSchema(BaseModel):
    name: str
    description: str
    pattern: str
    reusable_structure: str


class SimilarDomainSchema(BaseModel):
    domain: str
    schema_name: str
    similarity_reason: str
    transferable_mechanisms: List[str]


class TransferredIdea(BaseModel):
    source_domain: str
    imported_mechanism: str
    target_domain_application: str
    expected_benefit: str
    risk_or_limitation: str
    score: float = 0.0


class VerificationStep(BaseModel):
    test_name: str
    method: str
    metric: str
    success_condition: str


class ConceptTransferOutput(BaseModel):
    original_problem: str
    core_question: str
    domain: str
    variables: List[Variable]
    relationships: List[Relationship]
    abstract_schema: AbstractSchema
    similar_schemas: List[SimilarDomainSchema]
    transferred_ideas: List[TransferredIdea]
    verification_plan: List[VerificationStep]
    best_next_step: str
