---
title: "Skill Intervention Verification"
aliases:
  - interventional skill evaluation
  - skill net-effect verification
  - repair-regression verification
tags:
  - agents
  - skills
  - skill-synthesis
  - causal-inference
  - intervention
  - credit-assignment
maturity: emerging
key_papers:
  - skillgen-verified-inference-time-agent-skill
first_introduced: "2026"
date_updated: 2026-05-13
related_concepts:
  - skill-lifecycle
  - contrastive-induction-skill-synthesis
  - trajectory-grounded-blame-attribution
---

## Definition

**Skill intervention verification** is the practice of treating an agent skill as a causal intervention and empirically measuring its net effect Δ(s) = E[Y^s(x) − Y^0(x)] by running the base agent with and without the skill on *identical* inputs. The key metrics are:

- **Repairs** (n₀₁): instances where the baseline agent fails (Y^0 = 0) but the skilled agent succeeds (Y^s = 1).
- **Regressions** (n₁₀): instances where the baseline succeeds (Y^0 = 1) but the skilled agent fails (Y^s = 0).
- **Net gain** G_m = n₀₁ − n₁₀.

A **verification gate** marks a skill `active` only when G_m exceeds a threshold γ_m = max{g_abs, ⌈g_rel · m⌉, 1}; otherwise the skill is `deprecated` and the empty intervention is used.

## Intuition

Prior skill synthesis methods optimize for repairing failures but have no mechanism to prevent introducing regressions. The interventional framing — borrowed from the potential outcome framework in causal inference — makes this trade-off explicit and computable, ensuring that a deployed skill has a provably positive net effect on the same input distribution it was evaluated on.

## Key papers

- [[skillgen-verified-inference-time-agent-skill]] — introduces the concept and the generation–verification–refinement loop that operationalizes it.
