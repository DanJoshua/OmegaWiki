---
title: "Recurrent Skill Evolution"
aliases:
  - multi-generation skill optimization
  - iterative skill generation
  - skill evolution via RL
tags:
  - agent-skills
  - reinforcement-learning
  - self-evolving-agents
  - grpo
maturity: emerging
key_papers:
  - skill-r1-agent-skill-evolution-reinforcement
first_introduced: "2605.09359"
date_updated: 2026-05-12
related_concepts:
  - agentic-skill
  - skill-lifecycle
  - experience-library
  - forward-learning-from-experience
  - experience-driven-self-evolution-lifecycle
---

## Definition

**Recurrent skill evolution** is a paradigm for improving agent skills through a multi-generation, reward-driven loop in which a *separate trainable skill generator* — not the task LLM — iteratively revises external skills based on accumulated rollout outcomes. Each generation produces a new skill, which is evaluated by a frozen task LLM through a population of rollouts scored by a verifier; the resulting evidence is appended to a history that conditions the next skill revision.

Formally, given task instance x, initial skill s₀, frozen task policy π_task, and learnable skill generator π_θ:

1. s_g ~ π_θ(· | x, H_{g-1}), where H_{g-1} is the accumulated history of (skill, rollouts, rewards)
2. K rollouts y_g^(i) ~ π_task(· | x, s_g), verified to produce rewards r_g^(i)
3. H_g ← H_{g-1} ∪ {(s_g, rollouts, rewards)}
4. Repeat for G generations

π_θ is optimized with a **bi-level group-relative policy optimization (GRPO)** objective combining:
- **Intra-generation advantage**: relative performance of rollouts within the same generation, capturing local skill quality
- **Inter-generation advantage**: improvement in mean reward across successive generations, capturing directional progress

## Intuition

Static skills are designed once and used unchanged. Recurrent skill evolution treats skill improvement as a sequential decision problem: each revision should not just be "better in isolation" but should steer the task LLM toward progressively higher-reward rollout distributions across multiple attempts. The skill generator learns to diagnose recurring failure modes from the rollout history and produce targeted revisions, rather than making one-shot edits.

## Formal notation

- π_task: frozen task LLM (black box; open- or closed-source)
- π_θ: learnable skill generator (lightweight; e.g., Qwen3-4B)
- s_g ∈ S: skill at generation g (natural-language procedure)
- H_g: per-instance history of (skill, rollout, reward) tuples up to generation g
- f: verifier assigning scalar reward to each rollout
- G: number of generations; K: rollout group size per generation

Bi-level objective (simplified):
```
J(θ) = E_x [ Σ_g γ^{g-1} · (1/K) Σ_i r_g^(i) ]
     + λ · (inter-generation improvement term)
```

## Variants

- **Inference-only variant**: Skill-R1 with frozen skill generator — multi-generation loop without gradient updates; tests whether rollout structure alone helps
- **GRPO-trained variant**: Full Skill-R1 — skill generator trained online as skills evolve

## Comparison

| Mechanism | Who is trained | Optimization signal | Compatible with closed-source task LLMs? |
|---|---|---|---|
| Direct task LLM SFT/RLHF | Task LLM | Outcome reward | No |
| Heuristic skill rewriting | None (prompt only) | None | Yes |
| SkillOS skill curation | Skill curator LLM | Executor alignment via RL | Yes |
| EvoTool blame attribution | Tool-use policy components | Blame + evolutionary selection | Partially |
| **Recurrent skill evolution** | **Skill generator only** | **Bi-level GRPO on rollout rewards** | **Yes** |

## Known limitations

- Requires a verifier (programmatic reward signal); not directly applicable to open-ended tasks without ground truth
- Rollout cost scales with G × K; compute budget grows multiplicatively
- Inference-only multi-generation can underperform vanilla GRPO when the skill generator lacks training

## Key papers

- [[skill-r1-agent-skill-evolution-reinforcement]] — introduces this mechanism with Skill-R1
