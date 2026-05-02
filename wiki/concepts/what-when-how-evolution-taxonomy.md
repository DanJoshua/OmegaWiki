---
title: "What-When-How Evolution Taxonomy"
aliases:
  - what when how to evolve
  - what-when-how-where taxonomy
  - self-evolution dimensions
tags:
  - taxonomy
  - self-evolution
  - llm-agents
  - framework
maturity: emerging
key_papers:
  - survey-self-evolving-agents-what-when
first_introduced: "2025"
date_updated: 2026-05-02
related_concepts:
  - self-evolving-agent
---

## Definition

The **what-when-how (extended to where) taxonomy** is the organizing framework introduced by [[survey-self-evolving-agents-what-when]] for self-evolving agents. It decomposes any evolution mechanism along four orthogonal dimensions:

- **What to evolve**: which component of the agent system changes — the model parameters `ψ`, the context `C` (prompts and memory), the toolset `W`, or the architecture `Γ` (single- vs multi-agent topology).
- **When to evolve**: the temporal stage — *intra-test-time* (within a single task; ICL-style) or *inter-test-time* (between tasks; SFT- or RL-style).
- **How to evolve**: the methodological family — reward-based, imitation/demonstration learning (self-generated, cross-agent, hybrid), or population-based / evolutionary methods, with cross-cutting axes online/offline, on/off-policy, and reward granularity.
- **Where to evolve**: the deployment domain — general-purpose vs specialized (coding, GUI, finance, medical, education).

## Intuition

Prior surveys grouped self-evolution methods by algorithmic family (RL, distillation, prompting), which obscured that the same algorithm could target *different components* at *different stages* in *different domains*. The four-axis decomposition lets two methods that look superficially similar be placed apart when they target different components or stages, and lets two methods that look algorithmically different be grouped when they share the same locus of change.

## Formal notation

Each evolution mechanism is a tuple `(W, T, H, D)` where W ∈ {model, context, tools, architecture}, T ∈ {intra-test-time, inter-test-time}, H ∈ {reward-based, imitation, population-based}, D ∈ {general, specialized-domain}. The Cartesian product yields the design space; existing literature populates only a subset.

## Variants

- **What axis**:
  - Model: parameter updates, LoRA, full fine-tune.
  - Context: memory evolution, prompt optimization.
  - Tools: tool synthesis, tool selection policy refinement.
  - Architecture: single-agent workflow optimization, multi-agent topology evolution.
- **When axis**:
  - Intra-test-time: in-context adaptation within one task.
  - Inter-test-time: persistent updates between tasks via SFT or RL.
- **How axis**:
  - Reward-based (scalar signals).
  - Imitation/demonstration (self-generated, cross-agent, hybrid).
  - Population-based / evolutionary.
- **Cross-cutting**: online/offline, on/off-policy, reward granularity (step-level, trajectory-level, outcome-level).

## Comparison

- vs. component-only taxonomies: those tile only the *what* axis and miss stage/method splits.
- vs. method-only taxonomies (e.g., "RL for agents"): those tile only the *how* axis and miss component/stage splits.
- vs. lifelong-learning taxonomies: those center on catastrophic forgetting; this taxonomy treats it as one axis among several.

## When to use

Use to classify a new self-evolution paper, to identify under-populated cells of the design space, or to compare two methods on a common grid.

## Known limitations

- The axes are *orthogonal in principle* but real systems often touch multiple cells (e.g., evolve memory and tools jointly).
- The taxonomy is descriptive, not prescriptive: it does not say which cells are most promising.
- Boundaries between intra- and inter-test-time blur for streaming deployments.

## Open problems

- Which cells of the (what × when × how × where) grid are systematically underexplored?
- Are there evolution mechanisms outside the current axes (e.g., evolving the reward function itself)?
- Can the taxonomy be extended to embodied / multimodal agents without forcing them into LLM-shaped boxes?

## Key papers

- [[survey-self-evolving-agents-what-when]]

## My understanding

This is the right axis system for filing new self-evolving-agent papers in this wiki. When ingesting a new paper in the area, place it explicitly on `(what, when, how, where)` and note the cell — this makes coverage gaps visible in aggregate and prevents mis-grouping methods that share an algorithm but target different loci.
