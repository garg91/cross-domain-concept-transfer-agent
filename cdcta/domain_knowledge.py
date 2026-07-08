from __future__ import annotations

from .models import Variable, Relationship, VerificationStep

DOMAIN_KEYWORDS = {
    "compression": ["compression", "compressor", "chunk", "entropy", "zstd", "gzip", "lzma", "archive"],
    "trading": ["trading", "market", "volatility", "portfolio", "strategy", "price", "regime", "drawdown"],
    "materials": ["material", "superconductor", "crystal", "phonon", "lattice", "dopant", "pressure", "stability"],
    "algorithms": ["algorithm", "polynomial", "symmetry", "complexity", "search", "invariant", "graph", "solve"],
    "operating systems": ["os", "operating system", "scheduler", "process", "thread", "cpu", "memory", "latency"],
    "databases": ["database", "query", "index", "join", "cardinality", "sql", "optimizer", "table"],
    "medicine": ["medicine", "patient", "treatment", "symptom", "biomarker", "diagnosis", "dose", "clinical"],
    "robotics": ["robot", "robotics", "sensor", "control", "terrain", "policy", "actuator", "navigation"],
    "compiler optimization": ["compiler", "optimization", "pass", "loop", "binary", "runtime", "compile", "llvm"],
    "AI agents": ["agent", "tool", "llm", "model", "routing", "task", "workflow", "planner"],
}

DOMAIN_VARIABLES = {
    "compression": [
        ("entropy", "Randomness or unpredictability of a chunk.", "measurable"),
        ("repetition", "Amount of repeated local or global patterns.", "measurable"),
        ("chunk type", "Text, binary, tensor, image, archive, log, or mixed data.", "hidden/measurable"),
        ("compressor choice", "Selected algorithm or codec.", "controllable"),
        ("compression level", "Intensity setting for a compressor.", "controllable"),
        ("chunk size", "Granularity at which decisions are made.", "controllable"),
        ("compression ratio", "Compressed size divided by original size.", "output"),
        ("compression/decompression time", "Runtime cost of encoding and decoding.", "output"),
        ("metadata overhead", "Header/model information required to decode chunks.", "constraint"),
    ],
    "trading": [
        ("volatility", "Magnitude and instability of price changes.", "measurable"),
        ("trend strength", "Persistence of directional price movement.", "measurable"),
        ("liquidity", "Ability to enter/exit positions without large price impact.", "measurable"),
        ("hidden market regime", "Latent state such as trending, mean-reverting, crisis, or calm.", "hidden"),
        ("strategy choice", "Selected trading rule or portfolio policy.", "controllable"),
        ("position size", "Capital allocated to a trade.", "controllable"),
        ("transaction cost", "Spread, slippage, and fees.", "constraint"),
        ("return and drawdown", "Performance and downside risk.", "output"),
    ],
    "materials": [
        ("crystal structure", "Atomic arrangement and symmetry.", "measurable/controllable"),
        ("bond length", "Distance between atoms affecting electronic and phonon behavior.", "measurable"),
        ("carrier density", "Number of mobile charge carriers.", "measurable/controllable"),
        ("phonon modes", "Lattice vibrations that can mediate pairing.", "measurable"),
        ("electron-phonon coupling", "Interaction strength between electrons and lattice vibrations.", "hidden/measurable"),
        ("formation energy", "Thermodynamic stability of a candidate.", "output"),
        ("pressure", "External constraint used to stabilize phases.", "constraint"),
        ("dopants", "Elements introduced to modify structure or carriers.", "controllable"),
    ],
    "algorithms": [
        ("state space", "Set of candidate states or solutions.", "measurable"),
        ("invariants", "Properties preserved under transformations.", "hidden/measurable"),
        ("equivalence classes", "Groups of states that can be treated as the same.", "hidden"),
        ("constraints", "Rules that valid solutions must satisfy.", "constraint"),
        ("branching factor", "Number of choices at each search step.", "measurable"),
        ("representation", "How the problem is encoded.", "controllable"),
        ("runtime", "Execution time or complexity.", "output"),
    ],
    "operating systems": [
        ("CPU demand", "How much computation a task needs.", "measurable"),
        ("I/O demand", "How much waiting on disk/network/device operations occurs.", "measurable"),
        ("memory pressure", "Memory requirement and contention.", "measurable"),
        ("latency sensitivity", "How delay-sensitive the task is.", "constraint"),
        ("priority", "Relative importance of task execution.", "controllable"),
        ("scheduler policy", "Rule for selecting which task runs.", "controllable"),
        ("throughput/fairness", "Aggregate performance and fairness outcome.", "output"),
    ],
    "databases": [
        ("table size", "Number of rows and storage size.", "measurable"),
        ("index availability", "Indexes usable by the query.", "measurable/controllable"),
        ("join order", "Order in which tables are joined.", "controllable"),
        ("selectivity", "Fraction of rows passing a predicate.", "hidden/measurable"),
        ("cardinality estimate", "Predicted row counts during planning.", "hidden"),
        ("query plan", "Chosen execution strategy.", "controllable"),
        ("execution time", "Runtime latency of query.", "output"),
    ],
    "medicine": [
        ("symptoms", "Observed patient complaints or signs.", "measurable"),
        ("biomarkers", "Lab or biological measurements.", "measurable"),
        ("medical history", "Prior conditions, medications, and context.", "constraint"),
        ("disease subtype", "Latent patient or disease category.", "hidden"),
        ("treatment", "Selected intervention.", "controllable"),
        ("dosage", "Amount and schedule of intervention.", "controllable"),
        ("side effects", "Negative outcomes or safety events.", "output"),
        ("clinical outcome", "Measured patient improvement or decline.", "output"),
    ],
    "robotics": [
        ("sensor input", "Camera, lidar, proprioception, force, or other observations.", "measurable"),
        ("environment type", "Terrain/object/task context.", "hidden/measurable"),
        ("robot state", "Joint angles, velocity, pose, and internal state.", "measurable"),
        ("uncertainty", "Ambiguity or noise in perception/control.", "hidden"),
        ("control policy", "Chosen action-generation method.", "controllable"),
        ("energy use", "Power or battery consumption.", "output"),
        ("task success", "Whether the robot completes the goal.", "output"),
    ],
    "compiler optimization": [
        ("code structure", "Loops, branches, memory accesses, and data dependencies.", "measurable"),
        ("target hardware", "CPU/GPU/cache/vector architecture.", "constraint"),
        ("optimization pass", "Transformation applied by compiler.", "controllable"),
        ("compile-time budget", "Time allowed to search optimizations.", "constraint"),
        ("runtime", "Execution time of produced program.", "output"),
        ("binary size", "Size of compiled output.", "output"),
    ],
    "AI agents": [
        ("user intent", "Goal implied by the user request.", "hidden/measurable"),
        ("task type", "Math, coding, search, writing, planning, vision, etc.", "hidden/measurable"),
        ("available tools", "APIs, databases, solvers, browsers, code execution, or models.", "constraint"),
        ("tool choice", "Selected external tool or model.", "controllable"),
        ("latency/cost budget", "Time and money allowed for a response.", "constraint"),
        ("verification method", "How the result is checked.", "controllable"),
        ("task success", "Correctness or user satisfaction.", "output"),
    ],
}

DOMAIN_RELATIONSHIPS = {
    "compression": [
        ("entropy", "compression ratio", "negatively affects"),
        ("repetition", "dictionary-compressor performance", "positively affects"),
        ("chunk type", "best compressor", "influences"),
        ("chunk size", "pattern detection", "affects"),
        ("compression level", "compression time", "increases"),
        ("metadata overhead", "net compression gain", "reduces"),
    ],
    "trading": [
        ("volatility", "risk exposure", "increases"),
        ("hidden market regime", "best strategy", "determines"),
        ("liquidity", "transaction cost", "affects"),
        ("position size", "drawdown", "influences"),
    ],
    "materials": [
        ("crystal structure", "phonon modes", "determines"),
        ("bond length", "electron-phonon coupling", "affects"),
        ("dopants", "carrier density", "modify"),
        ("pressure", "phase stability", "increases or changes"),
        ("formation energy", "synthesis plausibility", "affects"),
    ],
    "algorithms": [
        ("invariants", "search space", "reduce"),
        ("equivalence classes", "branching factor", "reduce"),
        ("representation", "runtime", "affects"),
        ("constraints", "valid solutions", "define"),
    ],
    "operating systems": [
        ("CPU demand", "scheduler policy", "influences"),
        ("I/O demand", "waiting time", "increases"),
        ("latency sensitivity", "priority", "affects"),
        ("context-switch cost", "throughput", "reduces"),
    ],
    "databases": [
        ("selectivity", "cardinality estimate", "determines"),
        ("cardinality estimate", "query plan", "influences"),
        ("index availability", "execution time", "reduces when useful"),
        ("join order", "execution time", "affects"),
    ],
    "medicine": [
        ("disease subtype", "best treatment", "influences"),
        ("biomarkers", "disease subtype", "help infer"),
        ("dosage", "side effects", "affects"),
        ("medical history", "treatment safety", "constrains"),
    ],
    "robotics": [
        ("sensor input", "environment type", "helps infer"),
        ("environment type", "best control policy", "influences"),
        ("uncertainty", "failure risk", "increases"),
        ("control policy", "task success", "affects"),
    ],
    "compiler optimization": [
        ("code structure", "best optimization pass", "influences"),
        ("target hardware", "runtime", "affects"),
        ("compile-time budget", "optimization search", "constrains"),
        ("optimization pass", "binary size", "affects"),
    ],
    "AI agents": [
        ("user intent", "tool choice", "influences"),
        ("task type", "best model/tool", "determines"),
        ("latency/cost budget", "tool choice", "constrains"),
        ("verification method", "task success", "improves"),
    ],
}

DOMAIN_VERIFICATION = {
    "compression": [
        ("Compressor routing benchmark", "Compare selector against fixed compressors and oracle.", "size/time Pareto frontier", "Selector improves Pareto frontier or approaches oracle."),
        ("Cost estimator test", "Predict compressed size/time from samples and features.", "prediction error", "Low error relative to actual compression."),
        ("Metadata overhead test", "Measure archive overhead per chunk.", "overhead percent", "Net gains survive metadata cost."),
    ],
    "trading": [
        ("Regime backtest", "Backtest regime-specific strategies out-of-sample.", "Sharpe, drawdown, turnover", "Improves risk-adjusted return after costs."),
        ("Transaction-cost stress test", "Increase spread/slippage assumptions.", "net return", "Performance remains robust after costs."),
    ],
    "materials": [
        ("Candidate stability screening", "Relax candidate structures with simulation or database screening.", "formation energy", "Candidate is stable or metastable enough to study."),
        ("Property estimation", "Estimate electronic/phonon properties.", "target property score", "Meets threshold compared with baseline materials."),
    ],
    "algorithms": [
        ("Search-space reduction test", "Compare brute force vs symmetry-reduced solver.", "states visited/runtime", "Reduction preserves correctness and lowers runtime."),
        ("Correctness proof/check", "Use tests or formal proof for transformations.", "pass/fail", "Reduced solver matches known answers."),
    ],
    "operating systems": [
        ("Scheduling benchmark", "Simulate workloads with mixed CPU/I/O/latency profiles.", "throughput/latency/fairness", "Improves selected metrics without starving jobs."),
    ],
    "databases": [
        ("Plan-estimate calibration", "Compare estimated vs actual plan costs.", "cost error and query latency", "Better plan choices than baseline optimizer."),
    ],
    "medicine": [
        ("Retrospective subgroup validation", "Evaluate treatment policy on historical validated data.", "outcome and adverse event rate", "Improves outcome without violating safety constraints."),
    ],
    "robotics": [
        ("Simulated environment sweep", "Test policies across terrain/task variations.", "success/collision/energy", "Improves success and safety across environments."),
    ],
    "compiler optimization": [
        ("Benchmark suite evaluation", "Run optimized outputs across representative programs.", "runtime/compile-time/binary size", "Improves runtime within compile-time budget."),
    ],
    "AI agents": [
        ("Tool-routing eval", "Run benchmark tasks requiring different tools.", "success/cost/latency", "Improves success rate or cost-adjusted performance."),
    ],
}

TRANSFER_TEMPLATES = {
    "mixture-of-experts": "Use a lightweight gating model to route inputs to specialized experts.",
    "database query planning": "Estimate candidate plan cost before committing to full execution.",
    "operating systems": "Borrow resource-aware scheduling and fallback policies under constraints.",
    "trading": "Detect hidden regimes and switch policies when the regime changes.",
    "medicine": "Use subtype-specific intervention logic instead of a one-size-fits-all policy.",
    "robotics": "Use closed-loop feedback to update policy based on observed error.",
    "compiler optimization": "Apply staged transformations selected by structure and cost budget.",
    "AI agents": "Route tasks to tools based on intent, uncertainty, cost, and verification needs.",
    "polynomial solving": "Look for invariants and symmetries that reduce the problem representation.",
}


def variables_for(domain: str):
    return [Variable(name=n, description=d, type=t) for n, d, t in DOMAIN_VARIABLES.get(domain, DOMAIN_VARIABLES["AI agents"])]


def relationships_for(domain: str):
    return [Relationship(source=s, target=t, relation=r) for s, t, r in DOMAIN_RELATIONSHIPS.get(domain, DOMAIN_RELATIONSHIPS["AI agents"])]


def verification_for(domain: str):
    return [VerificationStep(test_name=n, method=m, metric=metric, success_condition=sc) for n, m, metric, sc in DOMAIN_VERIFICATION.get(domain, DOMAIN_VERIFICATION["AI agents"])]
