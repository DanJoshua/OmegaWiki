---
title: "Three Laws of Self-Evolving AI Agents"
aliases:
  - Three Laws (Endure, Excel, Evolve)
  - Endure-Excel-Evolve
  - Three Laws of Self-Evolution
tags:
  - agents
  - self-evolution
  - safety
  - alignment
  - ethics
maturity: emerging
key_papers:
  - comprehensive-survey-self-evolving-ai-agents
first_introduced: "2025"
date_updated: 2026-05-02
related_concepts:
  - mase-paradigm
  - agent-optimisation-feedback-loop
---

## Definition

A hierarchical set of priority constraints proposed by [[comprehensive-survey-self-evolving-ai-agents]], inspired by Asimov's *Three Laws of Robotics*, intended to guide the design of any self-evolving AI agent:

1. **Endure (Safety Adaptation)** — Self-evolving AI agents must maintain safety and stability during any modification.
2. **Excel (Performance Preservation)** — Subject to the First Law, self-evolving AI agents must preserve or enhance existing task performance.
3. **Evolve (Autonomous Evolution)** — Subject to the First and Second Laws, self-evolving AI agents must be able to autonomously optimise their internal components in response to changing tasks, environments, or resources.

The laws are *hierarchical*: the Second cannot override the First, and the Third cannot override the First or Second.

## Intuition

A purely accuracy-driven optimisation loop will trade away safety for marginal score improvements; a purely safety-driven loop will refuse to evolve. The Three Laws encode a principled tie-breaking order that matches typical engineering priorities for deployed agents: never regress safety, then preserve task performance, then improve autonomously.

## Formal notation

The survey presents the laws in natural language. They function as a *priority ordering* over objective components:

```
prioritise(safety) > prioritise(performance) > prioritise(autonomy)
```

A concrete operationalisation would express the agent's update rule as a constrained optimisation:

```
A_{t+1} = argmax_{A in S}  performance(A)
         subject to        safety(A) >= safety_threshold
                           performance(A) >= performance(A_t) - eps
```

The survey does not yet supply a canonical formal definition; subsequent work is expected to propose evaluation protocols.

## Variants

- **Strict priority**: each lower-numbered law is an absolute hard constraint.
- **Soft priority**: laws are weighted, with safety receiving the largest multiplier.
- **Audited priority**: an external auditor enforces the laws between optimisation rounds.

## Comparison

vs. **Asimov's Three Laws of Robotics**: structural inspiration only. Asimov's laws govern the agent's external action policy; these govern the agent's *self-modification* policy.

vs. **Constitutional AI / RLHF**: those align a *static* model's outputs with human values. The Three Laws aim to constrain the *evolution* loop itself.

## When to use

- As a normative checklist when designing a self-evolving system.
- As a structuring device for safety-aware optimisation objectives.
- As a discussion frame when reasoning about regulatory or audit requirements for adaptive agents.

## Known limitations

- The laws are stated as priorities but not operationalised: no reference protocol, metric, or audit procedure is supplied.
- Determining whether an update preserves "safety" or "performance" requires a measurable definition of each, which is itself an open problem in many domains.
- In adversarial environments the laws can conflict in subtle ways (a "safe" refusal may degrade performance below a contractual threshold).

## Open problems

- Formal safety predicates that an optimiser can check without running the new agent in deployment.
- Audit mechanisms compatible with regulations such as the EU AI Act and GDPR for agents whose decision logic mutates after deployment.
- Reconciling the Three Laws with empirical findings that strong safety constraints often reduce capability.

## Key papers

- [[comprehensive-survey-self-evolving-ai-agents]] — proposes and articulates the Three Laws.

## My understanding

The Three Laws are currently a research-agenda artefact rather than a deployable constraint set. Their utility today is rhetorical: naming the priority ordering (safety > performance > autonomy) gives the field a Schelling point, and any future operationalisation work must explicitly engage with this ordering. A wiki entry is justified because subsequent papers will reference the laws by name even before formal protocols exist.
