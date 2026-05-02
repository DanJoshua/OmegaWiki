---
title: "Trajectory-Grounded Blame Attribution"
aliases:
  - module-level blame
  - blame attribution
  - trajectory blame
tags:
  - llm-agents
  - tool-use
  - credit-assignment
  - prompt-optimization
maturity: emerging
key_papers:
  - evotool-self-evolving-tool-use-policy
first_introduced: "2026"
date_updated: 2026-05-02
related_concepts:
  - modular-tool-use-policy
  - diversity-aware-population-selection
---

## Definition

Trajectory-Grounded Blame Attribution is a credit-assignment mechanism for self-evolving LLM agents: structured intermediate signals from a tool-interaction trajectory (schema violations, tool-choice outcomes, execution outcomes, grounding consistency) are converted by a "Blamer" LLM into per-module blame scores $b_\pi(e) \in [0,1]$, identifying which module of a modular tool-use policy is most responsible for an observed failure. The module with the highest blame score becomes the next mutation target, replacing global blind search with localized repair.

## Intuition

Tool environments emit far richer feedback than the scalar end-of-trajectory reward. A Blamer LLM is asked: given the full trajectory and these structured diagnostic events, which module — Planner, Selector, Caller, or Synthesizer — is most responsible for the failure? Schema-invalid calls implicate the Caller; wrong / missing / unnecessary tool invocations implicate the Selector; redundant loops or missing subgoals implicate the Planner; ungrounded final responses implicate the Synthesizer.

## Formal notation

Given an episode record $e = (x, \tau, \hat{y}, R(x, \hat{y}))$ where $\tau = \{(s_t, a_t, o_t)\}_{t=1}^T$, extract diagnostic events $D = \textsc{ExtractDiagnostics}(\tau)$. The Blamer LLM produces module-wise scores
$$\{b_\pi(e)\}_{\pi \in \Pi} = \textsc{BlamerLLM}(e, D), \quad b_\pi(e) \in [0,1].$$
The mutation target is $\pi^* = \arg\max_{\pi \in \Pi} b_\pi(e)$.

## Variants

- **Hard $\arg\max$ attribution** (EvoTool default): commit to one module per failure.
- **Soft attribution** (not explored in EvoTool): treat $b_\pi(e)$ as weights and edit multiple modules proportionally — would address co-causal failures but increases regression risk.
- **Heuristic attribution**: deterministic mapping from diagnostic event types to modules, bypassing the Blamer LLM (mentioned in EvoTool's appendix as a fallback pattern).

## Comparison

Vs. **monolithic prompt optimization** (OPRO, PromptBreeder, EvoPrompt): blame attribution localizes edits, avoiding entanglement of heterogeneous behaviors.

Vs. **single-aspect optimization** (AdaPlanner, EasyTool, DRAFT, AnyTool): blame attribution adapts which module is edited per failure, instead of fixing the target module ahead of time.

Vs. **textual / verbal RL** (Reflexion, Self-Refine): blame attribution adds an explicit module-decomposition layer between the trace and the edit, rather than treating reflection as a global rewrite of the agent prompt.

## When to use

- Long-horizon, multi-stage agent policies where errors can originate from distinct competencies.
- Tool environments that emit structured intermediate signals (API errors, schema validators, execution traces).
- Settings where weight-based fine-tuning is expensive or impossible and gradient-free optimization is the only path.

## Known limitations

- Quality is bounded by the Blamer LLM's diagnostic accuracy, which is not validated against human annotation in the introducing paper.
- The hard-$\arg\max$ choice cannot represent multi-cause failures.
- Diagnostic extraction depends on the tool environment exposing structured signals; weakly-instrumented tools collapse blame attribution back toward global guesswork.

## Open problems

- Calibration: do Blamer scores match human module-attribution?
- Joint training: can blame and mutation be co-optimized rather than independent zero-shot calls?
- Scaling: does the mechanism extend cleanly to richer module decompositions (e.g., memory, verifier, critic)?

## Key papers

- [[evotool-self-evolving-tool-use-policy]] — introduces the mechanism for self-evolving tool-use policy optimization

## My understanding

This concept reframes credit assignment in agent self-evolution as a *diagnostic* problem rather than an *optimization* problem: the LLM is competent enough to *read* a trajectory and localize blame, so the harder optimization step (which-module-to-edit) is offloaded to inference rather than learned. Whether that offloading is reliable depends on the Blamer's accuracy, which is the open empirical question.
