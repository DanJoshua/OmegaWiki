---
title: "Hierarchical Experience Memory"
aliases:
  - hierarchical memory module
  - experience memory
  - memory module for agents
  - strategic-procedural-tool memory
tags:
  - agents
  - memory
  - self-evolution
  - continual-learning
maturity: emerging
key_papers:
  - learning-job-experience-driven-self-evolving
first_introduced: "2025"
date_updated: 2026-05-02
related_concepts: []
---

## Definition

A natural-language memory store for LLM-based agents that organizes accumulated experience along multiple abstraction levels, typically: a *strategic* layer (high-level dilemma → resolution patterns), a *procedural* layer (reusable sub-task workflows or SOPs, often indexed by application), and a *tool* layer (per-tool descriptions and post-action guidance). The hierarchy is updated autonomously by a reflection process after each sub-task and each full task, allowing test-time learning without modifying model parameters.

## Intuition

Flat memory stores (single buffer of past trajectories or summaries) face two competing pressures: include enough context to be useful, but stay small enough to fit the LLM context window. Splitting memory by abstraction level resolves this — coarse strategic guidance is small and always loaded, fine procedural detail is indexed and retrieved on demand, and per-tool memory rides alongside the relevant observation. The hierarchy mirrors how human experts compress experience into heuristics, SOPs, and muscle memory.

## Formal notation

Following MUSE: $\mathcal{M} = \{\mathcal{M}_{strat}, \mathcal{M}_{proc}, \mathcal{M}_{tool}\}$, with

- $\mathcal{M}_{strat}$ = set of $\langle \text{Dilemma}, \text{Strategy} \rangle$ pairs, fully loaded into system prompt
- $\mathcal{M}_{proc}$ = set of SOPs $p = (index_p, content_p)$; only $\{index_p\}$ is loaded, $content_p$ retrieved via tool $a_{mem}$
- $\mathcal{M}_{tool} = \{D_{static}, I_{dynamic}\}$ where $D_{static}$ sits in the system prompt and $I_{dynamic}$ rides with each observation $o_t$

## Variants

- **MUSE (this paper).** Three layers (strategic / procedural / tool), reflect-driven update, SOP index-content split.
- **Two-layer working/long-term memory** (mainstream cognitive-inspired baseline) — e.g. short-term context plus vector-DB long-term store. Less hierarchical structure within long-term memory.
- **Single-procedural-store memories** (ExpeL, Agent Workflow Memory, Memp) — collapse strategic and tool layers into a single library of distilled rules or workflows.

## Comparison

Distinct from generic *retrieval-augmented* memory by (a) being agent-trajectory-derived rather than corpus-derived and (b) being structured by *role of knowledge* rather than by document. Distinct from *Reflexion-style* episodic memory by storing reusable abstractions (SOPs, dilemma-strategy pairs) rather than per-episode reflections.

## When to use

- Long-horizon agent tasks where each task spans many sub-tasks across applications.
- Settings where fine-tuning is impractical (compute, closed-source LLMs) and RL reward design is brittle.
- Cross-LLM portability is desired — natural-language memory transfers across base models without retraining.

## Known limitations

- Strategic memory must be kept concise to avoid system-prompt bloat; merging/dedup quality bounds the architecture.
- Procedural-memory retrieval relies on the agent proactively querying a dedicated tool; failure to query is a silent capability loss.
- No theoretical guarantee that newly distilled SOPs do not contradict older ones; relies on the reflect agent's dedup/generalization pass.
- Limited handling of *negative experience*: failures are summarized for replanning but not stored as reusable cautionary memory at the same granularity as successes.

## Open problems

- How to scale procedural memory to thousands of SOPs without degrading retrieval precision or context cost.
- How to learn structurally from failures, not just successes.
- How to formalize when two SOPs should be merged versus kept distinct.

## Key papers

- [[learning-job-experience-driven-self-evolving]] — introduces MUSE, the strategic/procedural/tool hierarchical decomposition, and the SOP index/content split.

## My understanding

Hierarchical experience memory is shaping up as the dominant approach to *test-time learning* for LLM agents now that flat memory stores are saturating on long-horizon benchmarks. The key open question is whether the hierarchy should be hand-designed (as in MUSE: strat/proc/tool) or *discovered* by the agent itself.
