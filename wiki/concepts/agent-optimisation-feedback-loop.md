---
title: "Agent Optimisation Feedback Loop"
aliases:
  - self-evolving feedback loop
  - four-component agent framework
  - Inputs-Agent-Environment-Optimiser
tags:
  - agents
  - self-evolution
  - optimisation
  - multi-agent
maturity: emerging
key_papers:
  - comprehensive-survey-self-evolving-ai-agents
first_introduced: "2025"
date_updated: 2026-05-02
related_concepts:
  - mase-paradigm
---

## Definition

The agent optimisation feedback loop is a four-component conceptual framework proposed by [[comprehensive-survey-self-evolving-ai-agents]] that abstracts every existing self-evolving agentic technique as an iterative optimisation cycle:

1. **System Inputs (`I`)** — task specification, training/test data, contextual examples. Two regimes: *task-level* optimisation (`I = {task T, dataset D_train}`) and *instance-level* optimisation (`I = {(x, y), context C}`).
2. **Agent System (`A`)** — the optimisation target. Single- or multi-agent; decomposable into LLM, prompts, memory, tools, topology, communication protocols.
3. **Environment** — the operational context; produces feedback signals via evaluation metrics (accuracy, F1, success rate, LLM-judge scores) that quantify performance.
4. **Optimiser (`P`)** — defined by a pair `(S, H)`: a *search space* `S` (the configurations available) and an *optimisation algorithm* `H` (rule-based, gradient, Bayesian, MCTS, RL, evolutionary, learned policy).

The loop iterates: agent acts in environment, environment yields feedback, optimiser updates agent, agent re-deployed, repeat until a performance threshold or convergence criterion is met.

## Intuition

Most "agent X is self-evolving" claims in the recent literature pick a different component to update — prompts, memory, topology, the underlying LLM — but reuse the same closed-loop control structure. Naming the four components explicitly turns "self-evolving" from a marketing label into a comparison axis: two papers can be compared by stating their `(S, H)` pair and the feedback channel they consume.

## Formal notation

```
A* = argmax_{A in S} O(A; I)
```

where:
- `O(A; I)` is the evaluation function provided by the environment
- `S` is the configuration search space (granularity ranges from prompts and tool selections to LLM parameters and inter-agent topology)
- `H` chooses or generates candidates from `S`

## Variants

- **Component-level scope**: optimise only LLM, only prompts, only memory, only tools, or only topology.
- **Joint scope**: optimise multiple components together (e.g. MASS, EvoFlow, MaAS, ANN).
- **Inputs-augmenting scope**: the optimiser refines the inputs themselves by synthesising training examples (Absolute Zero, R-Zero).

## Comparison

| Search space `S`            | Typical algorithms `H`                     |
|-----------------------------|--------------------------------------------|
| Prompts                     | Edit-based, generative, text-gradient, evolutionary |
| Tools                       | SFT, RL, prompt-based, MCTS, tool creation |
| Memory                      | Summarisation, retrieval policies, RL      |
| LLM parameters              | SFT, DPO, RLHF, GRPO                       |
| Multi-agent topology        | RL, MCTS, evolutionary, GNN-based          |
| Joint multi-component       | Code-based co-evolution, alternating search, learned controllers |

## When to use

- As an organising vocabulary when comparing self-evolving agent papers.
- As a checklist when designing a new self-evolving system: did you specify `I`, `A`, the environment's feedback channel, and a concrete `(S, H)`?

## Known limitations

- The framework is *descriptive*, not *prescriptive*: it does not say which `(S, H)` choices will succeed.
- The boundaries between `A` and `Environment` blur in agentic settings where the environment includes other LLM agents.
- The loop assumes a usable feedback signal; in many real domains (medicine, scientific discovery) ground truth is contested.

## Open problems

- Co-optimisation across components without combinatorial blow-up.
- Convergence diagnostics for LLM-based optimisers.
- Feedback design when ground truth is absent (proxy metrics, LLM-as-judge calibration).

## Key papers

- [[comprehensive-survey-self-evolving-ai-agents]] — introduces the four-component framework.

## My understanding

The framework is the most reusable artefact of the survey. Whenever a new "self-evolving" paper appears, the first move is to ask: what is `S`? what is `H`? what feedback channel from the environment does the optimiser consume? If those three slots can be filled in one sentence each, the paper is doing something concrete; if they cannot, the "self-evolving" label is mostly aspirational.
