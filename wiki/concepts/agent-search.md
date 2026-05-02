---
title: "Agent Search"
aliases:
  - agent retrieval
  - agent discovery
  - agent selection
tags:
  - agents
  - retrieval
  - reranking
  - llm-agents
maturity: emerging
key_papers:
  - agentsearchbench-benchmark-ai-agent-search-wild
first_introduced: "2026"
date_updated: 2026-05-02
related_concepts: []
---

## Definition

Agent search is the problem of retrieving and ranking suitable AI agents from a (potentially very large) candidate repository, given a task specification supplied by a user, an orchestrator, or another agent. A scoring function `f(a, T)` estimates the relevance of each agent `a` in the candidate pool `C` to the task `T`, and produces an ordered list `O = argsort_a f(a, T)`. The two coupled objectives are (i) retrieving top-k *capable* agents and (ii) ranking them by expected task-execution quality.

## Intuition

Unlike traditional tool retrieval, where a tool's functionality is largely captured by a description or schema, agent capability is **compositional and execution-dependent**: two agents with near-identical descriptions can have very different real-world performance, and semantically dissimilar agents can solve the same task. Agent search therefore cannot be solved by document matching alone — it requires (or approximates) signal from actual agent execution.

## Formal notation

- `T_q`: an executable task query (concrete instruction; can be run directly on an agent).
- `T_d`: a high-level task description; not directly executable but associated with a set `Q(T_d) = {T_{q_1}, ..., T_{q_m}}` of executable queries that instantiate it.
- `y(a, T_q) = E(a, T_q)`: an execution-grounded relevance score (e.g. LLM-as-judge) for agent `a` on query `T_q`.
- `y(a, T_d) = (1/|Q(T_d)|) * sum_{T_q in Q(T_d)} y(a, T_q)`: aggregated relevance over the description's instantiations.

Documentation-performance alignment can be folded in as a discount: agents that succeed on a task whose required capability they do not document are weighted below those whose execution matches their description.

## Variants

- **Retrieval-only agent search** (top-k from the full repository, binary relevance).
- **Reranking** (refining a small candidate pool using graded execution-based labels).
- **Single-agent vs multi-agent search** (a single agent for the whole task vs a team covering complementary subtasks).
- **Description-driven vs query-driven** (high-level `T_d` vs concrete `T_q`).
- **Execution-aware probing** as augmentation (full-document indexing including usage examples; explicit probe queries whose responses become extra ranking features).

## Comparison

- *Tool retrieval* (e.g. ToolBench, ToolRet) assumes well-specified, mostly-deterministic tools with structured schemas.
- *Model selection / routing* (e.g. TREC MLLM 2025) ranks LLMs over a small controlled pool, usually without compositional capability concerns.
- *Automated agentic system design* (e.g. AgentSquare, OKC Bench) optimises the *configuration* of agents over a small candidate set rather than searching open ecosystems.

Agent search differs by combining open large-scale ecosystems, capability uncertainty, compositional/execution-dependent skills, and support for both `T_q` and `T_d`.

## When to use

Use the agent-search frame whenever a system must pick from a large, heterogeneous, third-party agent pool (e.g. GPT Store, marketplaces, MCP registries) and the relevance signal of interest is real task completion, not just textual similarity.

## Known limitations

- Execution is expensive; full evaluation over thousands of agents is rarely feasible without a hybrid pre-retrieval cap.
- Description-based retrievers struggle on `T_d` because high-level intent rarely lexically aligns with low-level documentation.
- Execution probing helps but is not strictly additive — strong LLM-based rerankers can regress under poorly-designed probes.

## Open problems

- Cheap, transferable behavioural fingerprints for agents.
- Composition-aware retrieval that returns *teams* rather than top-1 individuals.
- Handling capability drift in self-evolving agents.

## Key papers

- [[agentsearchbench-benchmark-ai-agent-search-wild]] — formalises the problem and provides the first execution-grounded benchmark.

## My understanding

Agent search is the natural successor to tool retrieval once agents become first-class actors with non-trivial, execution-dependent behaviour. The defining signal is *what the agent actually does on a task*, not *what its docs claim*. The most interesting research question is how cheaply we can recover that execution signal at indexing time.
