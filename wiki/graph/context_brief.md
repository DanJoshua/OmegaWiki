# Query Pack (general)

_Auto-generated compressed context. Do not edit._

## Claims (19 total)
- [weakly_supported] LLM-agent performance follows a scaling law in experience-library size (conf: 0.55)
- [weakly_supported] Hierarchical experience memory enables LLM agents to self-evolve at test time on long-horizon tasks (conf: 0.55)
- [weakly_supported] Gradient-free experience-library learning can match or exceed gradient-based parameter tuning on agentic reasoning benchmarks (conf: 0.45)
- [weakly_supported] Self-evolution introduces emergent safety risks (misevolution, reward hacking, alignment drift) not present in static agents (conf: 0.7)
- [weakly_supported] Static LLM-based agents are a critical bottleneck in open-ended deployments and require self-evolution (conf: 0.65)
- [supported] Contrastive induction over success+failure trajectories outperforms success-only skill synthesis (conf: 0.82)
- [weakly_supported] Critique-grounded episodic+semantic memory improves agent task accuracy without parameter updates (conf: 0.65)
- [weakly_supported] Curated agentic skills outperform self-generated skills (conf: 0.65)
- [weakly_supported] Instance-wins (diversity-aware) selection outperforms greedy and top-k selection in evolutionary prompt search for heterogeneous tool-use tasks (conf: 0.6)
- [weakly_supported] Description-based retrieval underperforms execution-grounded relevance for selecting AI agents (conf: 0.7)
- [weakly_supported] Self-evolving memory's gain correlates with within-dataset task similarity (conf: 0.65)
- [weakly_supported] Module-level blame attribution enables stable, targeted improvement of modular tool-use policies under sparse end-of-trajectory supervision (conf: 0.6)
- [weakly_supported] Recurrent Bi-Level GRPO Skill Evolution Outperforms Vanilla GRPO on Multi-Step Agent Tasks (conf: 0.72)
- [weakly_supported] RL-Trained Skill Curator Outperforms Frontier Model Curator Due to Executor Alignment (conf: 0.68)
- [weakly_supported] Self-distilled experience principles outperform external-teacher distillation once the agent's base model c
## Open Gaps
_Auto-generated open questions. Do not edit._
- [paper/agentsearchbench-benchmark-ai-agent-search-wild] Can execution-aware probing be made cheap enough (e.g. shared probe banks, cached responses) to deploy as a standard pre-rank layer in production agent stores?
- [paper/agentsearchbench-benchmark-ai-agent-search-wild] How should ranking handle *capability composition*: when no single agent covers a multi-step task, should retrievers surface complementary teams rather than top-1 individuals?
- [paper/agentsearchbench-benchmark-ai-agent-search-wild] What is the right unit of evaluation for self-evolving agents whose capabilities change between probing and deployment?
- [paper/agentsearchbench-benchmark-ai-agent-search-wild] Can the documentation-performance gap be closed at the *source* by inducing agent providers to publish execution traces or behavioural fingerprints?
- [paper/comprehensive-survey-self-evolving-ai-agents] How do we evaluate self-evolving agents whose target distribution itself is non-stationary? Static benchmarks under-represent the lifelong setting.
- [paper/comprehensive-survey-self-evolving-ai-agents] Can the search space `S` be co-optimised across components (LLM + prompts + memory + topology) without combinatorial blow-up? Existing "unified" methods (MASS, EvoFlow, MaAS, ANN) only scratch this surface.
- [paper/comprehensive-survey-self-evolving-ai-agents] How should regulators (EU AI Act, GDPR) treat agents whose decision logic mutates after deploymen
## Papers (14 total)
- [3] SkillGen: Verified Inference-Time Agent Skill Synthesis (NLP)
- [3] SkillOS: Learning Skill Curation for Self-Evolving Agents (NLP)
- [3] Skill-R1: Agent Skill Evolution via Reinforcement Learning (NLP)
- [4] EvoTool: Self-Evolving Tool-Use Policy Optimization in LLM Agents via Blame-Aware Mutation and Diversity-Aware Selection (NLP)
- [4] SoK: Agentic Skills - Beyond Tool Use in LLM Agents (ML Systems)
- [3] Learning from Supervision with Semantic and Episodic Memory: A Reflective Approach to Agent Adaptation (NLP)
- [4] A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems (NLP)
- [4] Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory (NLP)
- [4] FLEX: Continuous Agent Evolution via Forward Learning from Experience (NLP)
- [4] A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence (NLP)
- [3] EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle (NLP)
- [3] AgentSearchBench: A Benchmark for AI Agent Search in the Wild (NLP)
- [3] DeepWideSearch: Benchmarking Depth and Width in Agentic Information Seeking (NLP)
- [3] Learning on the Job: An Experience-Driven Self-Evolving Agent for Long-Horizon Tasks (NLP)
## Recent Relationships (68 total)
  papers/skillos-learning-skill-curation-self-evolving --extends_concept--> concepts/skill-lifecycle
  papers/skillos-learning-skill-curation-self-evolving --uses_concept--> concepts/agentic-skill
  papers/skillos-learning-skill-curation-self-evolving --uses_concept--> concepts/experience-library
  papers/skillos-learning-skill-curation-self-evolving --uses_concept--> concepts/experience-driven-self-evolution-lifecycle
  papers/skillos-learning-skill-curation-self-evolving --builds_on--> papers/comprehensive-survey-self-evolving-ai-agents
  papers/skillos-learning-skill-curation-self-evolving --compares_against--> papers/evo-memory-benchmarking-llm-agent-test
  papers/skillos-learning-skill-curation-self-evolving --supports--> claims/rl-trained-skill-curator-outperforms-frontier-curator
  papers/skill-r1-agent-skill-evolution-reinforcement --uses_concept--> concepts/agentic-skill
  papers/skill-r1-agent-skill-evolution-reinforcement --introduces_concept--> concepts/recurrent-skill-evol
