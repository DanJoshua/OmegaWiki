---
title: "Skill-R1: Agent Skill Evolution via Reinforcement Learning"
slug: skill-r1-agent-skill-evolution-reinforcement
arxiv: "2605.09359"
venue: "COLM 2026 (submitted)"
year: 2026
tags:
  - agent-skills
  - reinforcement-learning
  - skill-evolution
  - grpo
  - self-evolving-agents
  - frozen-llm
importance: 3
date_added: 2026-05-12
source_type: tex
s2_id: ""
keywords:
  - skill evolution
  - bi-level GRPO
  - skill generator
  - recurrent skill optimization
  - frozen task LLM
  - verifiable rewards
  - multi-generation rollouts
domain: NLP
code_url: ""
cited_by: []
---

## Problem

Agent skills — reusable natural-language procedures that guide LLM planning, tool use, and action — are typically static artifacts. Existing approaches either predefined skills and leave them fixed, revise them through heuristic prompt engineering, or align the task LLM itself to revised skills. The latter is costly, model-specific, and infeasible for closed-source models. More fundamentally, skill improvement is not a one-step prompt-editing problem but a **recurrent** bi-level credit-assignment problem: a useful skill must improve rollout quality under current conditioning, while a useful revision must convert observed successes and failures into a better skill for the next generation.

## Key idea

Train a **separate, lightweight skill generator** (not the task LLM) with reinforcement learning. The skill generator conditions on the task context, prior rollouts, and their verified outcomes to produce skills that steer a **frozen** task LLM. A **bi-level GRPO** objective with intra-generation and inter-generation advantages optimizes the skill generator over multiple generations of skill → rollout → reward → revision cycles.

## Method

**Architecture**: Decoupled execution from skill refinement. A frozen task LLM π_task generates rollout trajectories conditioned on the current skill. A trainable skill generator π_θ revises skills based on accumulated history.

**Multi-generation loop**: For each task instance x, starting from initial skill s₀:
1. Task LLM produces K rollouts conditioned on s_g; verifier assigns rewards r_g^(i)
2. History H_g = {(x, s_g, rollouts, rewards)} is accumulated
3. Skill generator produces next skill: s_{g+1} ~ π_θ(· | x, H_g)
4. Repeat for G generations

**Bi-level GRPO objective**:
- *Intra-generation advantage*: compares rollout quality within a generation under shared skill conditioning — captures local relative performance
- *Inter-generation advantage*: rewards skill revisions that improve average verified performance across successive generations — captures directional progress
- Combined objective: J(θ) = Σ_g γ^{g-1} · mean reward of generation g

**Skill initialization**: Two-stage distillation — GPT-4o-mini on seed tasks collects trajectories; a stronger LLM (Claude Opus 4.6) abstracts patterns into reusable skill guides.

**Training vs Inference**: Skill-R1 (GRPO) trains the Qwen3-4B skill generator online; Skill-R1 (Inference) runs the multi-generation loop with a frozen Qwen editor (no gradient updates).

## Results

GPT-4o-mini used as frozen task LLM; Qwen3-4B as skill generator.

**GAIA** (165 multi-step real-world QA tasks):
- No skills: 6.1%
- Vanilla GRPO: 29.7%
- Skill-R1 (Inference): 30.9%
- **Skill-R1 (GRPO): 41.8%** (+12.1 pp over Vanilla GRPO)
- Largest gain on Level-3 tasks: 0% → 38.5%

**WebWalker** (100 multi-hop web navigation tasks):
- No skills: 2.0%
- Vanilla GRPO: 22.0%
- Skill-R1 (Inference): 19.0%
- **Skill-R1 (GRPO): 26.0%** (+4.0 pp over Vanilla GRPO)

Analysis: early generations drive most capability improvement; later iterations enhance reliability and consistency. Bi-level advantages both necessary — intra-generation alone underfits, inter-generation alone is noisy.

## Limitations

- Evaluated on only two benchmarks (GAIA, WebWalker); generality to other agent task distributions unknown
- Task LLM fixed as GPT-4o-mini; interaction between skill generator and different task LLMs unexplored
- Inference-only variant (Skill-R1 Inference) sometimes underperforms Vanilla GRPO (WebWalker: 19% vs 22%), suggesting rollout structure alone is insufficient without trained editing
- Small task model: Qwen3-4B skill generator; scaling behavior with larger editors unstudied
- No direct comparison to other skill-evolution baselines (e.g., SkillOS, MemSkill)

## Open questions

- Can the bi-level GRPO objective be extended to multi-agent settings where skills must generalize across agents?
- What is the sample efficiency of Skill-R1 relative to direct task LLM RLHF?
- Does experience inheritance hold for the skill generator (i.e., can a generator trained on one benchmark transfer to another)?

## My take

Skill-R1 cleanly formalizes a previously informal insight: that skill improvement is a sequential decision problem, not a one-shot edit. The bi-level GRPO decomposition is principled and the separation of skill generator from frozen task LLM is practically significant — it preserves compatibility with closed-source models. The GAIA gain (+12.1 pp over Vanilla GRPO) is substantial. The WebWalker inference-only regression (19% vs 22%) hints that the rollout structure may hurt when the skill generator is not yet trained to navigate the task distribution — worth monitoring.

## Related

- [[agentic-skill]] — Skill-R1 operates on agentic skills as first-class objects
- [[skill-lifecycle]] — Multi-generation skill evolution is a new lifecycle mechanism
- [[recurrent-skill-evolution]] — New concept introduced by this paper
- [[experience-library]] — Rollout history functions as a per-instance experience accumulator
- [[experience-driven-self-evolution-lifecycle]] — Skill-R1 fits the lifecycle pattern but adds RL training of the evolution component
- [[skillos-learning-skill-curation-self-evolving]] — SkillOS trains an RL curator; Skill-R1 trains an RL skill generator/editor
- [[evotool-self-evolving-tool-use-policy]] — EvoTool uses blame attribution + evolutionary selection; Skill-R1 uses bi-level GRPO
- [[sok-agentic-skills-beyond-tool-use]] — SoK surveys the skill layer this paper contributes to
- [[forward-learning-from-experience]] — Skill-R1 updates skill generator (not task LLM parameters) via rollout experience
