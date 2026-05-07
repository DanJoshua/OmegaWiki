---
title: "Self-evolving Memory"
aliases:
  - evolving memory
  - dynamic memory
  - test-time memory evolution
tags:
  - llm-agents
  - memory
  - continual-learning
  - test-time
maturity: emerging
key_papers:
  - evo-memory-benchmarking-llm-agent-test
  - learning-supervision-semantic-episodic-memory-reflective
first_introduced: "2025"
date_updated: 2026-05-02
related_concepts:
  - test-time-learning
---

## Definition

**Self-evolving memory** is a memory mechanism for LLM agents in which the memory state $M_t$ is treated as a first-class, mutable variable that the agent **retrieves from, integrates into its working context, and actively updates** after every interaction during deployment. Unlike static dialogue buffers or read-only retrieval indices, self-evolving memory supports continuous *test-time evolution*: the agent's stored experiences are pruned, reorganized, and refined in response to feedback, so that future tasks benefit from accumulated procedural and strategic knowledge rather than only past factual content.

## Intuition

Static recall asks "what was said?"; self-evolving memory asks "what was learned?". A traditional RAG agent retrieves prior text to compensate for context limits but never edits its store. A self-evolving memory agent treats $M_t$ as part of the policy state — every step generates a new memory entry $m_t = h(x_t, \hat{y}_t, f_t)$, the update rule $U$ may compress, replace, or reorganize entries, and retrieval $R$ pulls strategy-level abstractions (e.g. "use the quadratic formula") rather than verbatim facts (e.g. "the user once asked $2x^2 + 3x - 1 = 0$").

## Formal notation

A self-evolving memory agent is a tuple $(F, U, R, C)$ with base LLM $F$, update operator $U$, retriever $R$, and context constructor $C$. At step $t$:

$$R_t = R(M_t, x_t), \qquad \tilde{C}_t = C(x_t, R_t), \qquad \hat{y}_t = F(\tilde{C}_t),$$
$$m_t = h(x_t, \hat{y}_t, f_t), \qquad M_{t+1} = U(M_t, m_t).$$

The signature $U: \mathcal{M} \times \mathcal{E} \to \mathcal{M}$ is the defining feature: a non-trivial $U$ (one that does more than append) is what distinguishes self-evolving memory from passive context buffers.

## Variants

- **Append-only retrieval memory** — $U(M_t, m_t) = M_t \cup \{m_t\}$. ExpRAG and similar baselines.
- **Compression / summarization memory** — $U$ replaces multiple entries with a learned summary; long-term storage like MemoryBank, Zep.
- **Workflow / procedural memory** — $U$ extracts reusable workflow templates from successful trajectories; Agent Workflow Memory, Dynamic Cheatsheet.
- **Refine-style memory** — $U$ is invoked as an explicit *Refine* action interleaved with reasoning and acting; ReMem.
- **Hierarchical / OS-style memory** — $U$ promotes/demotes entries across short, mid, long-term tiers; MemGPT, MemOS.

## Comparison

|  | static retrieval (RAG) | conversational memory | self-evolving memory |
|---|---|---|---|
| What is stored? | static documents | dialogue history | task experiences with feedback |
| Mutates over time? | no | append | rewrite, prune, reorganize |
| Goal | factual grounding | recall consistency | strategy abstraction and reuse |
| Failure mode | retrieval miss | context bloat | catastrophic forgetting / drift |

## When to use

- Multi-turn or long-horizon agents where strategy-level transfer across episodes matters more than factual recall.
- Streaming task settings where the same reasoning template recurs (high within-cluster task similarity), e.g. PDDL, AlfWorld, math-olympiad streams.
- Settings with a usable feedback signal $f_t$ (correctness, success/failure) that can drive memory pruning or reweighting.

## Known limitations

- Gains correlate with within-dataset task similarity; on diverse, low-coherence streams self-evolving memory adds little.
- Memory growth is unbounded unless $U$ includes pruning; naive append accumulates noise.
- Strongly dependent on the quality of $f_t$; without ground-truth feedback, self-evolution can amplify mistakes.
- Increased per-step token cost when reflection / refinement is interleaved with action.

## Open problems

- Unsupervised self-evolution: how to refine memory without explicit feedback signals.
- Catastrophic interference between self-evolving memory and parameter-level test-time learning (LoRA adapters, in-context fine-tuning).
- Theoretical complexity / transfer guarantees for experience reuse beyond cluster-similarity heuristics.

## Key papers

- [[evo-memory-benchmarking-llm-agent-test]] — introduces the streaming benchmark and the ReMem refine operator that operationalize the concept.
- [[learning-supervision-semantic-episodic-memory-reflective]] — instantiates the episodic+semantic memory split in a supervised classification setting; introduces the suggestibility metric to explain variance in memory augmentation gains.

## My understanding

Self-evolving memory is the natural endpoint of treating LLM agents as MDPs whose state includes external storage. The conceptual leap from RAG is small but consequential: once $U$ is allowed to be non-trivial, memory becomes a *learned policy* over what to remember, and the agent's quality is bounded by the quality of that policy as much as by the underlying LLM. The most important empirical finding so far is that simple task-level appends (ExpRAG) capture most of the gain — elaborate workflow / hierarchical schemes underperform on the streaming benchmark — which suggests the field's first-order question is *what to retrieve*, not *how to compress*.
