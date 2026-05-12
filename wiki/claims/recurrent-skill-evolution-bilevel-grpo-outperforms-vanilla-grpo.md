---
title: "Recurrent Bi-Level GRPO Skill Evolution Outperforms Vanilla GRPO on Multi-Step Agent Tasks"
slug: recurrent-skill-evolution-bilevel-grpo-outperforms-vanilla-grpo
status: weakly_supported
confidence: 0.72
tags:
  - skill-evolution
  - reinforcement-learning
  - grpo
  - self-evolving-agents
  - agent-skills
domain: "NLP"
source_papers:
  - skill-r1-agent-skill-evolution-reinforcement
evidence:
  - source: skill-r1-agent-skill-evolution-reinforcement
    type: supports
    strength: moderate
    detail: "Skill-R1 (GRPO, Qwen3-4B skill generator + GPT-4o-mini task LLM) achieves 41.8% on GAIA (+12.1pp over Vanilla GRPO at 29.7%) and 26.0% on WebWalker (+4.0pp over Vanilla GRPO at 22.0%). The ablation between Skill-R1 Inference (19-31%, multi-generation without RL) and Skill-R1 GRPO (26-42%) shows that the learned bi-level objective accounts for the bulk of the gain beyond the rollout structure."
conditions: "Validated with frozen GPT-4o-mini as task LLM and Qwen3-4B as skill generator, on GAIA (165 tasks) and WebWalker (100 tasks). Both benchmarks require multi-step reasoning with programmatically verifiable rewards. Gains are largest on hardest subtasks."
date_proposed: 2026-05-12
date_updated: 2026-05-12
---

## Statement

Training a lightweight skill generator with a **bi-level GRPO** objective — combining intra-generation (rollout quality within a generation) and inter-generation (reward improvement across successive generations) advantages — yields consistent improvements over standard single-level GRPO on multi-step agent benchmarks with verifiable rewards. The frozen task LLM is never updated; only the skill generator is trained.

## Evidence summary

- **Skill-R1 (2026)** on GAIA: Vanilla GRPO 29.7% → Skill-R1 GRPO 41.8% (+12.1pp). Ablation confirms the inference-only multi-generation variant (30.9%) closes only 1.2pp of the gap, so ~10.9pp comes from the trained bi-level GRPO objective.
- **Skill-R1 (2026)** on WebWalker: Vanilla GRPO 22.0% → Skill-R1 GRPO 26.0% (+4.0pp). Here the inference-only variant underperforms Vanilla GRPO (19.0%), suggesting multi-generation rollouts without RL training can hurt on some distributions.
- Effect strongest on complex tasks: GAIA Level-3 jumps from 15.4% (Vanilla GRPO) to 38.5% (Skill-R1 GRPO).

## Conditions and scope

- Requires a programmatically verifiable reward signal (cannot apply to open-ended generation)
- Task LLM must be fixed (frozen); Skill-R1 becomes standard GRPO if the task LLM is the training target
- Inference-only multi-generation can *underperform* vanilla GRPO on some tasks, so the bi-level training is necessary, not just the rollout structure
- Validated on 2 benchmarks with 1 task LLM (GPT-4o-mini) and 1 skill generator size (Qwen3-4B)

## Counter-evidence

None directly. WebWalker inference-only regression (19% vs 22%) is a partial challenge — it suggests the gain is not merely from multi-generation structure, which is consistent with the claim's emphasis on the bi-level training objective.

## Linked ideas

## Open questions

- Does the bi-level GRPO advantage generalize to task LLMs other than GPT-4o-mini?
- What is the minimum number of generations G and rollout group size K for reliable gains?
- Can the inter-generation advantage be estimated more efficiently than exhaustive cross-generation rollout comparison?
