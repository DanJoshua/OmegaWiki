---
title: "Contrastive Induction for Skill Synthesis"
aliases:
  - contrastive trajectory induction
  - contrastive skill induction
  - contrastive behavioral induction
tags:
  - agents
  - skills
  - skill-synthesis
  - contrastive-learning
  - trajectory-analysis
maturity: emerging
key_papers:
  - skillgen-verified-inference-time-agent-skill
first_introduced: "2026"
date_updated: 2026-05-13
related_concepts:
  - skill-lifecycle
  - skill-intervention-verification
---

## Definition

**Contrastive induction for skill synthesis** is a method for extracting reusable agent skills from a mixed pool of successful and failed trajectories by explicitly surfacing the *contrastive signal* between the two strata. Rather than summarizing successes in isolation, the approach identifies: (a) cluster-level failure modes with corrective rules, (b) cluster-level success patterns with robustness checks, and (c) local contrastive observations — for each failed trajectory, the nearest successful trajectory on the same task type is retrieved and the agent writes a targeted observation noting which behavior was present in the success but absent in the failure.

The resulting diagnostic summary Z = (a₀, F, S, C) serves as a compact, interpretable input to a downstream skill generation stage.

## Intuition

Success-only learning cannot answer "what did the agent do differently in the failed case?" Contrastive induction anchors skill advice in behaviors the base agent has *already demonstrated* on similar tasks — making the generated guidance grounded in actual agent capability rather than hypothetical best practice. The local nearest-neighbor pairing is especially powerful for isolating small action choices (e.g., an intermediate validation step) that cluster-level summaries miss.

## Key papers

- [[skillgen-verified-inference-time-agent-skill]] — introduces the concept and the (F, S, C) diagnostic decomposition.
