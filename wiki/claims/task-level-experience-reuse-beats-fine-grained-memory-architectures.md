---
title: "Task-level experience reuse beats fine-grained memory architectures for streaming LLM agents"
slug: task-level-experience-reuse-beats-fine-grained-memory-architectures
status: weakly_supported
confidence: 0.6
tags:
  - llm-agents
  - memory
  - benchmark
  - test-time-learning
domain: NLP
source_papers:
  - evo-memory-benchmarking-llm-agent-test
evidence:
  - source: evo-memory-benchmarking-llm-agent-test
    type: supports
    strength: moderate
    detail: "On the Evo-Memory streaming benchmark, simple task-level retrieval (ExpRAG / ExpRecent) is competitive with the more elaborate Refine-style ReMem and outperforms hierarchical / workflow / dynamic-cheatsheet baselines (MemOS, Mem0, LangMem, AWM, DC-Cu, DC-RS) across both Gemini-2.5 and Claude backbones; ExpRAG reaches 0.66 success on AlfWorld and 0.56 on ScienceWorld vs <=0.40 for most non-evolving baselines."
conditions: "Holds when (i) feedback signal f_t is available per task, (ii) within-dataset task similarity is non-trivial, and (iii) memory entries are stored at task granularity rather than fine-grained turn-level. May not hold for purely factual recall benchmarks or for streams with very low task similarity (e.g., AIME-25, GPQA)."
date_proposed: 2026-05-02
date_updated: 2026-05-02
---

## Statement

For streaming LLM agents on the Evo-Memory benchmark, **task-level experience reuse** — storing each completed task as a single memory entry $(x_i, \hat{y}_i, f_i)$ and retrieving the top-$k$ most similar past tasks — is competitive with or superior to more elaborate memory architectures (hierarchical, workflow-extraction, dynamic-cheatsheet, learned read/write controllers). The implication is that the field's first-order question for streaming agents is **what to retrieve at the task level**, not how to compress or hierarchically organize fine-grained memory.

## Evidence summary

- The Evo-Memory paper unifies ten representative memory modules under a fixed `search-synthesis-evolve` protocol with identical prompts and backbones, isolating memory-design effects.
- ExpRAG (a deliberately simple task-level baseline) outperforms SelfRAG, Mem0, LangMem, MemOS, Dynamic Cheatsheet (Cu/RS), and Agent Workflow Memory on multi-turn AgentBoard tasks.
- ReMem's additional Refine operator yields further gains over ExpRAG, but the gap between ExpRAG and the best non-evolving baseline is consistently larger than the gap between ExpRAG and ReMem, indicating that the dominant lift comes from task-level reuse, not from refinement.
- The pattern reproduces on both Gemini-2.5 (Flash, Flash-Lite, Pro) and Claude (3.5-Haiku, 3.7-Sonnet) families, ruling out a single-backbone artifact.

## Conditions and scope

- Requires per-task feedback $f_t$ (correctness signal). Without it, the simplest retrieval becomes unreliable because there is no quality filter on stored experiences.
- Requires non-trivial within-dataset task similarity — see [[memory-evolution-gain-correlates-with-task-similarity]]. On low-similarity streams (AIME-25, GPQA), the advantage of task-level reuse over fine-grained baselines shrinks.
- Holds at the granularity of *tasks*, not turns. Conversational-recall settings (LongMemEval, MemoryBank-style benchmarks) are explicitly out of scope and may favor different architectures.
- Currently single-paper evidence; classified `weakly_supported` until independent replication outside the Evo-Memory protocol.

## Counter-evidence

- Workflow-memory baselines (AWM, DC) perform competitively on highly structured single-turn tasks (AIME) where reusable templates dominate; the claim is weakest there.
- A reasonable a-priori expectation is that elaborate memory designs *should* help most on long horizons; their underperformance here may partly reflect that the unifying protocol forces them through interfaces they were not designed for.

## Linked ideas

(none yet)

## Open questions

- Does the result reproduce on benchmarks not authored by the same group?
- What happens when feedback signals are noisy or partial — does task-level reuse still dominate, or do refinement-based architectures pull ahead?
- Is there a regime (very long streams, very heterogeneous tasks) where hierarchical memory eventually wins because flat task-level stores become unsearchable?
