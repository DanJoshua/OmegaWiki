---
title: "Population broadcast improves over isolated Reflexion in all tested model-representation conditions"
slug: population-broadcast-outperforms-isolated-reflexion-across
status: weakly_supported
confidence: 0.65
tags:
  - self-evolving-agents
  - agent-memory
  - gradient-free-learning
  - population-based-training
  - reflexion
domain: "NLP"
source_papers:
  - forge-self-evolving-agent-memory-no
evidence:
  - source: forge-self-evolving-agent-memory-no
    type: supports
    strength: moderate
    detail: "FORGE (Reflexion + champion broadcast) improves over isolated Reflexion by 29-72% in all 12 model-representation conditions (4 LLM families × 3 memory representations). The no-graduation variant (broadcast only, no graduation) also outperforms Reflexion in all 12 conditions, confirming that broadcast — not graduation — carries the performance gains."
conditions: "Evaluated on CybORG CAGE-2 B_line attacker at 30-step horizon only. All four model families tested (Gemini-2.5-Flash-Lite as primary with 7 sessions; Grok-4-Fast, Llama-4-Maverick, Qwen3-235B as directional probes with 3-4 sessions each). Generalization to other POMDP environments, longer horizons, or different attacker types has not been tested."
date_proposed: 2026-05-18
date_updated: 2026-05-18
---

## Statement

Adding champion broadcast to an isolated Reflexion loop — propagating the best-performing instance's memory to all active instances between training stages — consistently improves post-session evaluation returns over isolated Reflexion (no broadcast) by 29-72% across all four tested LLM families and all three memory representations (Rules, Examples, Mixed). This holds regardless of whether graduation is enabled, confirming broadcast as the essential mechanism.

## Evidence summary

FORGE is tested against a Reflexion baseline (identical inner loop, no cross-instance knowledge transfer) under 12 conditions (4 models × 3 representations) on CybORG CAGE-2:

- **Gemini-2.5-Flash-Lite**: FORGE improvements over Reflexion are +51% (Rules), +69% (Examples), +61% (Mixed).
- **Grok-4-Fast**: +58%, +34%, +63%.
- **Llama-4-Maverick**: +29%, +48%, +33%.
- **Qwen3-235B**: +72%, +58%, +64%.

The no-graduation ablation (broadcast without memory-freeze) also outperforms Reflexion in all 12 conditions, isolating broadcast as the mechanism. Graduation primarily reduces compute cost (graduated instances excluded from further stages) rather than driving performance.

## Conditions and scope

- Environment: CybORG CAGE-2 B_line attacker, 30 steps, stochastic POMDP.
- All evidence from a single cyber-defense benchmark; cross-environment generalization is future work.
- Gemini is the primary model (7 independent sessions per representation); other families are directional probes (3-4 sessions per representation), so cross-family findings have wider confidence intervals.
- Results pertain to prompt-only adaptation; no comparison against parameter-efficient fine-tuning under matched compute.

## Counter-evidence

- Reflexion alone outperforms FORGE in some specific model-representation conditions when graduation is enabled (Grok and Qwen benefit from no-graduation variant), suggesting graduation can prematurely freeze instances in some models.
- Single-best champion selection may be brittle in environments with higher stochasticity or when the champion's return is driven by luck rather than genuine strategy quality.
- No published comparison outside CybORG CAGE-2.

## Linked ideas

(none yet)

## Open questions

- Does population broadcast improve over Reflexion in non-POMDP, non-cyber settings (e.g., coding agents, web navigation)?
- Can soft broadcast (weighted population selection) outperform single-best replacement?
- What is the minimum population size N required for broadcast to provide meaningful signal?
