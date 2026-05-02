---
title: "MASE: Multi-Agent Self-Evolving paradigm"
aliases:
  - MASE
  - Multi-Agent Self-Evolving
  - self-evolving agentic systems
  - MOP-MOA-MAO-MASE trajectory
tags:
  - agents
  - self-evolution
  - multi-agent
  - lifelong-learning
maturity: emerging
key_papers:
  - comprehensive-survey-self-evolving-ai-agents
first_introduced: "2025"
date_updated: 2026-05-02
related_concepts:
  - agent-optimisation-feedback-loop
  - three-laws-self-evolving-ai-agents
---

## Definition

MASE (Multi-Agent Self-Evolving) is the fourth and final stage in a four-stage trajectory of LLM-based learning paradigms proposed by [[comprehensive-survey-self-evolving-ai-agents]]: **MOP -> MOA -> MAO -> MASE**.

- **MOP (Model Offline Pretraining)**: foundation models pretrained once on static corpora and deployed frozen.
- **MOA (Model Online Adaptation)**: post-deployment adaptation of foundation models via SFT, LoRA, RLHF, etc.
- **MAO (Multi-Agent Orchestration)**: multiple LLM agents communicate and collaborate without modifying the underlying model.
- **MASE (Multi-Agent Self-Evolving)**: a lifelong, self-evolving loop where a population of agents continually refines its prompts, memory, tool-use strategies, and even its interaction topology based on environmental feedback and meta-rewards.

Each stage subsumes the capabilities of the prior one. MASE is distinguished by *autonomous, continuous* refinement of multiple components of the agent system, rather than a one-shot or human-in-the-loop update.

## Intuition

Static configurations cannot keep up with non-stationary environments. MASE asks: instead of human engineers re-tuning prompts and re-wiring topologies whenever requirements shift, can the agent system run that loop on itself? The answer requires a closed-loop control system in which the *agent system* is the controlled variable, the *environment* provides the error signal, and an *optimiser* applies the correction.

## Formal notation

Let `A` denote the agent system (decomposable into components: LLM, prompts, memory, tools, topology). Let `I` be the system inputs and `O(A; I)` an evaluation function returning a scalar score. The MASE objective is:

```
A* = argmax_{A in S} O(A; I)
```

where `S` is the search space of agent configurations and the optimiser is a pair `(S, H)` with `H` the optimisation algorithm (RL, evolutionary, MCTS, text-gradient, etc.). MASE differs from MAO in that this update happens *online and autonomously*, not just at design time.

## Variants

- **Single-agent MASE**: only one agent self-evolves; the search space spans LLM, prompts, memory, or tools.
- **Multi-agent MASE**: multiple agents co-evolve; the search space additionally spans agent roles, communication topology, and team composition.
- **Domain-specific MASE**: optimisation objective is tightly coupled to domain constraints (biomedicine, programming, finance/legal).

## Comparison

| Stage | Foundation model | Auxiliary components | Multi-agent | Update cycle |
|-------|------------------|----------------------|-------------|--------------|
| MOP   | frozen           | none                 | no          | none |
| MOA   | tunable          | optional             | no          | offline / batch |
| MAO   | frozen           | static               | yes         | none |
| MASE  | tunable          | tunable              | yes         | online, closed-loop |

## When to use

The MASE framing is most useful when the question is *which component should evolve and under what feedback signal*. Concretely:

- when manual reconfiguration is the bottleneck;
- when a single static prompt or topology cannot cover the input distribution;
- when an environment exposes a usable feedback signal (verifiable rewards, LLM-judge scores, execution traces).

## Known limitations

- The framing is descriptively powerful but not yet predictive: it does not say which `(S, H)` will succeed for a given task.
- Convergence guarantees of LLM-based optimisers are largely empirical.
- Existing implementations approximate MASE rather than realise it — most "self-evolving" systems still rely on human-curated reward signals or fixed search spaces.

## Open problems

- Joint optimisation across components (LLM + prompts + memory + tools + topology) without combinatorial blow-up.
- Online safety guarantees during evolution (the [[three-laws-self-evolving-ai-agents]] are aspirational rather than enforceable).
- Regulatory treatment of agents whose decision logic mutates after deployment.

## Key papers

- [[comprehensive-survey-self-evolving-ai-agents]] — defines and names the MASE paradigm.

## My understanding

MASE is best read as a research agenda label, not a deployed technology. Calling something "MASE" today essentially means "we close the loop on at least one component of an agent system using LLM-mediated optimisation". The label's value is that it forces a clean separation between *what* is being optimised (search space `S`) and *how* (algorithm `H`), which makes otherwise scattered papers comparable.
