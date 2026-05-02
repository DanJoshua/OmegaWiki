---
title: "Module-level blame attribution enables stable, targeted improvement of modular tool-use policies under sparse end-of-trajectory supervision"
slug: module-level-blame-attribution-enables-stable
status: weakly_supported
confidence: 0.6
tags:
  - llm-agents
  - tool-use
  - credit-assignment
  - prompt-optimization
domain: "NLP"
source_papers:
  - evotool-self-evolving-tool-use-policy
evidence:
  - source: evotool-self-evolving-tool-use-policy
    type: supports
    strength: moderate
    detail: "Blame-targeted mutation outperforms random module mutation by ~17 average points and outperforms monolithic mutation by ~8 average points on Qwen3-8B across four benchmarks (Table: Blame-targeting ablations). Single-module variants (always mutating one fixed module) generalize poorly, confirming that the choice of which module to mutate carries the optimization signal."
conditions: "LLM-based agent with a modular tool-use decomposition (Planner / Selector / Caller / Synthesizer); tool environment that emits structured intermediate diagnostics (schema validation, execution outcomes); a Blamer LLM available with reasonable diagnostic competence."
date_proposed: 2026-05-02
date_updated: 2026-05-02
---

## Statement

Routing each mutation to the module identified by per-trajectory blame scores (rather than mutating a fixed module, a randomly chosen module, or all modules at once) produces stable, monotonically improving tool-use policies under sparse end-of-trajectory supervision, on both open-source and closed-source backbone LLMs.

## Evidence summary

The introducing paper's blame-targeting ablation on Qwen3-8B compares (i) static (no evolution), (ii) random module targeting, (iii) four single-module variants, (iv) monolithic (mutate everything), and (v) the full blame-aware EvoTool. Random mutation degrades performance below static (-9 avg), each single-module variant excels in one niche but lags elsewhere, monolithic only modestly improves, and blame-aware EvoTool achieves the best average (57.0). The pattern repeats on GPT-4.1 in the main results table and on the learning-curve analysis (monotonic improvement vs. plateauing baselines).

## Conditions and scope

- Applies to settings with a clean module decomposition; un-decomposed (monolithic) policies cannot benefit from blame routing.
- Applies to tool environments that produce structured trajectories — without intermediate signals, blame attribution degrades to global guesswork.
- Validated only on textual / API-based benchmarks (ToolBench, RestBench, $\tau$-Bench, BFCL); multi-modal and embodied settings are untested.

## Counter-evidence

- The Blamer LLM's accuracy is not directly measured (e.g., against human module-attribution annotation); high benchmark gains might still co-exist with noisy module targeting if mutations are robust to mis-blame.
- Hard $\arg\max$ attribution may underperform on multi-cause failures; soft attribution is unexplored, so the claim's strength on co-causal failures is unverified.

## Linked ideas

(none yet)

## Open questions

- How robust is the claim under Blamer LLM noise (calibrated mis-attribution rate)?
- Does the claim hold for richer module decompositions (5+ modules)?
- Does the claim hold when the held-out evaluation set $S_{\text{sel}}$ shrinks?
