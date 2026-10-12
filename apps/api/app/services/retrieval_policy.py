from app.schemas.orchestrator import OrchestrationDecision
def should_retrieve(decision: OrchestrationDecision)->bool:
    return decision.retrieval!="none"