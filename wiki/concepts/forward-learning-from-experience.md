---
title: "Forward learning from experience"
aliases:
  - forward learning
  - gradient-free agent learning
  - semantic-gradient learning
tags:
  - self-evolving-agents
  - llm-agents
  - gradient-free-learning
  - meta-mdp
maturity: emerging
key_papers:
  - flex-continuous-agent-evolution-forward-learning
  - learning-supervision-semantic-episodic-memory-reflective
  - skill-r1-agent-skill-evolution-reinforcement
first_introduced: "FLEX (Cai et al., 2025)"
date_updated: 2026-05-02
related_concepts:
  - experience-library
  - experience-inheritance
---

## Definition

**Forward learning from experience** is a gradient-free learning paradigm in which an LLM agent improves over time by accumulating natural-language experience entries — rather than by updating model parameters. Optimization runs entirely on forward passes: an actor explores trajectories, a critic supplies semantic feedback, and an updater agent integrates distilled experiences into a persistent library. There is no backpropagation through the policy LLM.

## Intuition

Conventional learning computes $\theta_{i+1} = \theta_i - \eta \nabla_\theta \mathcal{J}(\theta_i)$. Forward learning replaces parameter $\theta$ with experience library $\mathcal{E}$ and the gradient with a forward probabilistic update from an updater agent $\mu$. The "semantic gradient" — the difference $\mu(\cdot \mid \mathcal{E}_i, \{\tau_i \mid X_i, \pi\}) - \mathcal{E}_i$ — captures what the library should change to make future reasoning more correct, expressed as natural-language deltas instead of numerical differentials.

## Formal notation

Optimization objective:
$$\mathcal{J}(\mathcal{E}) = \mathbb{E}_{(X,Y)\sim\mathcal{D}, \varepsilon\sim\rho(\cdot\mid X,\mathcal{E})} \big[\Phi(\pi(\cdot\mid X,\varepsilon),Y)\big],\quad \mathcal{E}^* = \arg\max_{\mathcal{E}} \mathcal{J}(\mathcal{E}).$$

Forward update rule:
$$\mathcal{E}_{i+1} \sim \mu(\cdot \mid \mathcal{E}_i, \{\tau_i \mid X_i, \pi\}),\qquad \nabla_{\mathcal{E}}\mathcal{J}(\mathcal{E}_i) \triangleq \mu(\cdot \mid \mathcal{E}_i, \{\tau_i \mid X_i, \pi\}) - \mathcal{E}_i.$$

Operationalized as a hierarchical Meta-MDP: a Base-level MDP per query handles trajectory exploration and per-sample experience distillation; a Meta-level MDP integrates distilled experiences across samples to evolve the global library.

## Variants

- **Actor-critic refinement** (FLEX, Reflexion-style): critic provides per-trajectory semantic feedback that drives sequential actor refinement.
- **Group-relative semantic advantage** (TF-GRPO): mimics GRPO with semantic rewards.
- **Textual gradients** (TextGrad, REVOLVE): natural-language analogs to gradients used to optimize prompts and chains.

## Comparison

- vs. **gradient-based fine-tuning** (SFT, RLHF, DPO): no parameter updates, no backpropagation; works against closed-weight LLMs.
- vs. **prompt-engineering / ICL**: optimizes a persistent, evolving knowledge structure rather than a static exemplar set.
- vs. **architecture / workflow evolution** (AgentSquare, AutoFlow): evolves the *content* of the agent's memory, not its computational graph.

## When to use

Closed-source LLM deployments; settings where catastrophic forgetting from parameter updates would degrade general capability; multi-agent ecosystems where learned knowledge must be transferable; small-data adaptation scenarios.

## Known limitations

- Reliability depends on the critic and updater being well-calibrated; miscalibration leads to noisy or harmful library entries.
- Theoretical guarantees (convergence, sample complexity) are largely heuristic.
- Computational savings vs. PEFT (LoRA) are not directly benchmarked.

## Open problems

- Formalizing the "semantic gradient" enough to produce convergence theorems.
- Robustness to adversarial or low-quality trajectories during exploration.
- Curriculum design — how should the order of training samples shape library quality?

## Key papers

- [[flex-continuous-agent-evolution-forward-learning]]
- [[learning-supervision-semantic-episodic-memory-reflective]] — implements forward learning via critique-grounded episodic/semantic memory in a supervised setting; no gradients, no retraining.

## My understanding

Forward learning is best read as a structural reframe of "experience-driven prompting" rather than a fundamentally new optimizer — but the reframe pays off: it unifies prompt evolution, workflow evolution, and memory accumulation under one Meta-MDP and surfaces empirical regularities (the experience scaling law) that earlier ad-hoc approaches did not.
