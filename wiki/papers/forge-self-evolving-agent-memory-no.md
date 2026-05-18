---
title: "FORGE: Self-Evolving Agent Memory With No Weight Updates via Population Broadcast"
slug: forge-self-evolving-agent-memory-no
arxiv: "2605.16233"
venue: "ACM CAIS '26"
year: 2026
tags:
  - self-evolving-agents
  - agent-memory
  - gradient-free-learning
  - population-based-training
  - reflexion
  - cyber-defense
  - POMDP
importance: 3
date_added: 2026-05-18
source_type: tex
s2_id: ""
keywords:
  - LLM agents
  - self-improvement
  - memory evolution
  - population-based training
  - prompt-only learning
  - cyber defense
  - POMDP
domain: "NLP"
code_url: "https://github.com/isbogdanov/forge-protocol"
cited_by: []
---

## Problem

LLM agents using Reflexion-style failure-triggered reflection improve through single-stream learning — each instance accumulates memory artifacts from its own trajectories in isolation. In stochastic, partially observable environments, this lack of selection pressure means: (1) instances can accumulate counterproductive artifacts and degrade below zero-shot, (2) even successful instances produce high-variance policies, and (3) rare strong strategies discovered by one instance are never shared with others. All four tested LLM families (Gemini-2.5-Flash-Lite, Grok-4-Fast, Llama-4-Maverick, Qwen3-235B) exhibit strongly negative, heavy-tailed zero-shot returns on CybORG CAGE-2 — a stochastic network-defense POMDP against a scripted B_line attacker over a 30-step horizon.

## Key idea

FORGE (Failure-Optimized Reflective Graduation and Evolution) adds a population outer loop to the Reflexion inner loop: after each stage, the champion (highest-checkpoint instance) broadcasts its complete memory to all active instances. A graduation criterion freezes instances whose checkpoint return exceeds threshold θ, protecting strong solutions and saving compute. No gradient updates, no stronger teacher model — the same underlying LLM generates actions and synthesizes memory artifacts.

## Method

**Agent architecture**: A hierarchical ReAct agent with three sub-agents: Planner (top-level action selector), Analyst (interprets host-level observations), and ActionChooser (ranks valid actions). All share the same LLM but differ in system prompts and injected memory.

**Memory representations** — three conditions compared:
- **Rules**: ordered lists of conditional heuristics synthesized by a Reflector agent
- **Examples**: structured few-shot demonstrations (thought/tool/observation/answer) from an Exemplifier agent
- **Mixed**: both Rules and Examples generated over the same failure context

**Inner loop (Reflexion)**: Each instance runs up to k_A=3 attempts per stage. If any per-step reward r_step < τ=−1.1 (excludes legitimate Restore penalties, captures true failures), the episode aborts and the Reflector/Exemplifier synthesizes a knowledge artifact that is appended to dynamic memory.

**Outer loop (FORGE)**:
1. N=10 instances run in parallel for S=6 stages
2. After each stage, a frozen checkpoint evaluation scores each instance
3. Champion broadcast: best instance's full memory replaces all other active instances' memory
4. Instances with checkpoint return > θ=−15 are graduated (frozen, excluded from further training)

Protocol parameters: N=10 instances, S=6 stages, k_A=3 attempts/stage.

## Results

Evaluated on CybORG CAGE-2 B_line attacker, 30-step horizon. Leaderboard reference: CardiffUni PPO DRL top score −3.47, rule-based heuristic −58.83, random −154.06.

**FORGE vs zero-shot improvement factors:**
- Gemini-2.5-Flash-Lite: −189.6 → −24.5 (Examples), **7.7×**
- Qwen3-235B: −103.3 → −24.3 (Examples), **4.3×**
- Llama-4-Maverick: −113.1 → −28.3 (Examples), **4.0×**
- Grok-4-Fast: −58.4 → −33.7 (Rules), **1.7×**

**FORGE vs Reflexion**: 29-72% improvement in all 12 model-representation conditions. Peak checkpoint return: −3.60 (Gemini Rules), approaching DRL top score of −3.47.

**Memory representation analysis**:
- Examples achieves best return for 3 of 4 models
- Rules achieves ~40% fewer tokens than Examples (106M vs 177M for Gemini), best cost-reliability profile
- Mixed falls between the two on both cost and performance

**Ablation (no graduation)**: Champion broadcast is the essential mechanism; graduation primarily contributes compute savings. Both FORGE and FORGE-without-graduation outperform Reflexion in all 12 conditions.

**Cross-model pattern**: Improvement magnitude inversely correlates with baseline strength — weaker models benefit disproportionately (Gemini 7.7× vs Grok 1.7×), suggesting FORGE functions primarily as a variance-reduction mechanism.

## Limitations

- All evidence confined to CybORG CAGE-2 B_line at a 30-step horizon; generalization to other attacker types and environments untested
- Non-Gemini models receive only 3-4 FORGE sessions per representation (directional evidence only)
- Failure trigger τ=−1.1 is not optimal; τ=−11.0 shows better results (−24.6 vs −30.6 on Gemini Rules), indicating the trigger-design space is underexplored
- Champion broadcast is brittle (single-best selection); checkpoint-evaluation misalignment exists
- No cost comparison against parameter-efficient fine-tuning (LoRA) under matched compute

## Open questions

- Does FORGE generalize to other POMDP domains, attacker types, or long-horizon planning tasks beyond CybORG?
- Can cross-model artifact transfer work (e.g., sharing champion Rules from Gemini to Qwen)?
- Does replacing the inner Reflexion loop with TextGrad or Dynamic Cheatsheet preserve population-broadcast gains?
- Multi-threshold triggering strategies and cross-strategy seeding (Mixed from Rules) remain unexplored.
- Cost-controlled comparison against LoRA fine-tuning to clarify prompt-only vs parameter-update trade-offs.

## My take

FORGE's core insight — that the bottleneck in prompt-only self-improvement is not reflection quality but the absence of selection pressure — is clean and empirically validated across four model families. The 7.7× improvement over zero-shot for Gemini on a challenging POMDP is compelling. The finding that graduation primarily saves compute (not performance) is a useful design guideline: broadcast first, graduation optional. The single-environment constraint is real but the mechanism (champion broadcast in prompt space ≅ PBT exploit step) is principle-general and extends naturally to other stochastic settings.

## Related

- [[self-evolving-memory]] — extends: FORGE instantiates population-broadcast as a specific memory update rule $U$
- [[population-broadcast-memory-evolution]] — introduces: the champion-broadcast + graduation mechanism
- [[test-time-learning]] — uses: FORGE is a test-time-learning method operating on external memory without parameter updates
- [[claim-gradient-free-agents-can-match-parameter-tuning]] — supports: 1.7-7.7× improvement over zero-shot using no weight updates in a stochastic POMDP
- [[population-broadcast-outperforms-isolated-reflexion]] — supports: 29-72% over Reflexion in all 12 conditions
