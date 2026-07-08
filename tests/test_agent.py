from cdcta.agent import CrossDomainConceptTransferAgent


def test_compression_domain_detection():
    agent = CrossDomainConceptTransferAgent()
    result = agent.run("Improve compression by selecting compressors for chunks based on entropy")
    assert result.domain == "compression"
    assert result.variables
    assert result.relationships
    assert result.transferred_ideas
    assert result.verification_plan


def test_algorithm_symmetry_schema():
    agent = CrossDomainConceptTransferAgent()
    result = agent.run("Use symmetry and invariants to solve a polynomial more easily")
    assert result.domain == "algorithms"
    assert "Symmetry" in result.abstract_schema.name or "Representation" in result.abstract_schema.name
