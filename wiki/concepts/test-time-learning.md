---
title: "Test-time Learning"
aliases:
  - test-time adaptation
  - test-time evolution
  - TTA
  - TTL
tags:
  - continual-learning
  - llm-agents
  - adaptation
  - deployment
maturity: active
key_papers:
  - evo-memory-benchmarking-llm-agent-test
first_introduced: "2020"
date_updated: 2026-05-02
related_concepts:
  - self-evolving-memory
---

## Definition

**Test-time learning (TTL)** is the family of techniques that allow a model to update some part of its state — parameters, prompts, retrieved context, or external memory — using *only the examples it sees during deployment*, without offline supervised retraining. Test-time learning generalizes the earlier notion of **test-time adaptation (TTA)**, which focused on parameter-level adjustment under distribution shift, to include adaptation of prompts, retrieval indices, agent memory, and reasoning policies.

## Intuition

A statically trained model is brittle when its deployment distribution drifts away from training. Test-time learning admits that drift is the norm and asks: *what is the smallest, safest update I can perform on the fly using only what I observe at inference?* For LLM agents, that update target has shifted from network weights (TENT, MEMO, T3A, TTT++) to higher-level policy state — chain-of-thought traces, retrieved exemplars, agent workflows, or self-evolving memory entries — because for frozen API-served LLMs the weights are simply not accessible.

## Formal notation

Let $\mathcal{D}_{\text{train}}$ be the training distribution and $\mathcal{D}_{\text{test}}$ the deployment stream. A TTL agent maintains policy state $\theta_t$ and observes $(x_t, [f_t])$, where $f_t$ is an *optional* feedback signal. After producing $\hat{y}_t$, it updates:

$$\theta_{t+1} = G(\theta_t, x_t, \hat{y}_t, f_t),$$

without revisiting $\mathcal{D}_{\text{train}}$. TTL methods differ in (i) what $\theta$ is — weights, prompts, memory $M_t$, retrieval index — and (ii) whether $f_t$ is available.

## Variants

- **Parameter-level TTA** — TENT (entropy minimization), MEMO (augmentation-marginal), T3A (template adjuster), TTT++. Updates a small subset of model parameters using self-supervised signals.
- **Prompt / context-level TTL** — adjusts prompts, demonstrations, or chains-of-thought based on observed inputs (e.g., self-discover, in-context learning with online demonstration selection).
- **Memory-level TTL (test-time evolution)** — updates an external memory store rather than weights or prompts; ExpRAG, ReMem, Dynamic Cheatsheet.
- **Self-improvement loops** — Reflexion, Voyager, Eureka — combine action, reflection, and skill / curriculum learning across episodes.

## Comparison

| Axis | TTA | Memory-level TTL |
|---|---|---|
| What is updated | small parameter subsets | external memory $M_t$ |
| Feedback signal | self-supervised (entropy, augmentations) | environment feedback $f_t$ if available |
| Reversibility | hard to undo | easy (drop memory entries) |
| Compatible with frozen LLMs | no | yes |

## When to use

- Deployment under distribution shift where retraining is infeasible or unsafe.
- Streaming or lifelong settings where each input carries small but cumulative signal.
- LLM-agent settings with frozen backbones and access to environment feedback.

## Known limitations

- Easy to amplify systematic errors when feedback is noisy or absent.
- Compounding drift across episodes if updates are not gated.
- Compute / latency overhead at inference time.
- Theoretical guarantees are limited; most TTL methods are empirical.

## Open problems

- Unsupervised TTL with no feedback at all.
- Combining parameter-level and memory-level TTL without interference.
- Characterizing which deployment streams admit transferable test-time updates and which do not.

## Key papers

- [[evo-memory-benchmarking-llm-agent-test]] — operationalizes test-time learning for LLM agents as memory-level *test-time evolution*, providing the first unified streaming benchmark for it.

## My understanding

For LLM agents, "test-time learning" has effectively become a synonym for *anything you can change at inference*, with weights mostly off-limits because backbones are API-gated. The most useful framing is to fix the policy-state object — memory, prompts, or retrieval index — and ask which update operator $G$ is stable under drift. Evo-Memory's contribution is to standardize the benchmark for the memory-state instantiation; the prompt-state and weight-state instantiations remain less unified.
