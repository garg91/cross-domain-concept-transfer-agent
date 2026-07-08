from __future__ import annotations

SCHEMA_LIBRARY = [
    {
        "name": "Adaptive Expert Selection",
        "description": "Different input regions require different specialized models, tools, or policies.",
        "domains": [
            "compression",
            "mixture-of-experts",
            "medicine",
            "database query planning",
            "operating systems",
            "trading",
            "AI agents",
            "compiler optimization",
        ],
        "structure": "input -> feature extraction -> hidden type/regime inference -> expert/policy selection -> feedback",
        "mechanisms": [
            "gating model",
            "expert routing",
            "fallback policy",
            "confidence-based escalation",
            "feedback-based policy update",
        ],
    },
    {
        "name": "Regime-Switching Policy Selection",
        "description": "A system changes behavior across hidden states, requiring state inference and policy changes.",
        "domains": ["trading", "robotics", "compression", "medicine", "AI agents"],
        "structure": "observations -> hidden state -> selected policy -> outcome -> state update",
        "mechanisms": [
            "regime detector",
            "hidden-state inference",
            "transition monitoring",
            "policy switching",
        ],
    },
    {
        "name": "Symmetry Reduction",
        "description": "Exploit invariance or equivalence classes to reduce search or solution complexity.",
        "domains": ["algorithms", "polynomial solving", "physics", "robotics", "computer vision"],
        "structure": "problem -> invariance/symmetry -> equivalence classes -> reduced search space -> solution",
        "mechanisms": [
            "invariant extraction",
            "canonicalization",
            "equivalence-class pruning",
            "group-action analysis",
        ],
    },
    {
        "name": "Cost-Based Planning",
        "description": "Estimate the cost of candidate strategies before committing to execution.",
        "domains": ["databases", "compiler optimization", "compression", "AI agents", "operating systems", "robotics"],
        "structure": "candidate plans -> estimated cost -> selected plan -> measured result -> updated estimator",
        "mechanisms": [
            "cost estimator",
            "sampling before commitment",
            "plan enumeration",
            "runtime feedback calibration",
        ],
    },
    {
        "name": "Feedback Control",
        "description": "Use observed error between goal and outcome to adjust future actions.",
        "domains": ["robotics", "trading", "AI agents", "medicine", "operating systems"],
        "structure": "goal -> action -> observation -> error -> policy update",
        "mechanisms": [
            "closed-loop control",
            "error correction",
            "online adaptation",
            "stability monitoring",
        ],
    },
    {
        "name": "Representation Change",
        "description": "Solve a hard problem by mapping it into a more useful representation.",
        "domains": ["algorithms", "polynomial solving", "compression", "materials", "AI agents"],
        "structure": "original representation -> transformed representation -> easier operation -> mapped-back result",
        "mechanisms": [
            "feature transformation",
            "latent representation",
            "basis change",
            "problem reparameterization",
        ],
    },
    {
        "name": "Constraint Substitution and Stability Optimization",
        "description": "Replace an expensive or difficult external constraint with an internal structural mechanism.",
        "domains": ["materials", "drug design", "structural engineering", "control systems"],
        "structure": "desired state -> expensive constraint -> substitute mechanism -> stability test -> optimized candidate",
        "mechanisms": [
            "host stabilization",
            "constraint relaxation",
            "candidate screening",
            "stability verification",
        ],
    },
]
