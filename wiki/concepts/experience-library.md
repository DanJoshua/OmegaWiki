---
title: "Experience library"
aliases:
  - experience bank
  - experience memory
  - experiential memory
tags:
  - self-evolving-agents
  - llm-agents
  - memory
  - retrieval
maturity: emerging
key_papers:
  - flex-continuous-agent-evolution-forward-learning
first_introduced: "FLEX (Cai et al., 2025)"
date_updated: 2026-05-02
related_concepts:
  - forward-learning-from-experience
  - experience-inheritance
---

## Definition

An **experience library** is a persistent, external store of natural-language strategies, reasoning patterns, and failure-mode diagnostics distilled from an LLM agent's prior interaction trajectories. Unlike model parameters, the library is updated forwardly (without backpropagation) and can be retrieved at inference time to condition the agent's reasoning on past lessons.

## Intuition

Frozen LLMs cannot learn after deployment. An experience library externalizes the "learned" component into a textual data structure, decoupling knowledge accumulation from parameter optimization. The library plays a role analogous to long-term memory: at inference, the agent retrieves relevant entries, treating them as additional context that reduces predictive uncertainty about the target output.

## Formal notation

Let $\mathcal{E}$ denote the library and $\rho(\cdot \mid X, \mathcal{E})$ the retrieval distribution. The agent computes $\pi(\cdot \mid X, \varepsilon)$ where $\varepsilon \sim \rho(\cdot \mid X, \mathcal{E})$. The library is updated forwardly as $\mathcal{E}_{i+1} \sim \mu(\cdot \mid \mathcal{E}_i, \{\tau_i \mid X_i, \pi\})$, where $\mu$ is an updater agent that distills new trajectories into entries. Information-theoretically, optimizing $\mathcal{E}$ minimizes $\mathcal{H}(Y \mid X, \varepsilon)$ — equivalently, maximizing the mutual information $\mathcal{I}(Y; \varepsilon \mid X)$.

## Variants

- **Hierarchical**: organized into strategic principles, reasoning patterns, and concrete instances (used for AIME25 and USPTO50k in FLEX).
- **Flat / non-hierarchical**: a single retrieval pool (used for GSM8k and ProteinGym in FLEX).
- **Dual-zone (golden vs. warning)**: separate stores for lessons from successes and from failure-mode diagnostics.
- **Trajectory-stored** (e.g., Memento): raw reasoning trajectories stored verbatim, no semantic distillation.

## Comparison

- vs. **vector memory / RAG corpora**: experience libraries are agent-authored and abstracted, not raw documents; retrieval can be contextualized rather than pure cosine-similarity.
- vs. **prompt engineering / ICL**: ICL injects fixed exemplars; an experience library evolves online and can re-organize entries based on new trajectories.
- vs. **fine-tuned weights**: weights are opaque and model-locked; the library is interpretable, transferable across agents, and gradient-free.

## When to use

When the deployment environment is closed-source or compute-limited; when continual cross-task learning is needed; when interpretability or human-in-the-loop curation matters; when knowledge should be portable across agents.

## Known limitations

- Retrieval quality bounds end-task performance; semantically similar but pragmatically wrong entries can mislead.
- Library growth must be curated — naive accumulation degenerates into redundant memory.
- The "schema" (hierarchy / zones) is hand-designed and currently benchmark-specific.
- Quality of distilled entries depends on the critic / updater agent's calibration.

## Open problems

- Negative transfer when mixing libraries from differently-aligned source agents.
- Convergence guarantees for forward probabilistic library updates.
- Schemas that auto-adapt to a new domain rather than being pre-specified.

## Key papers

- [[flex-continuous-agent-evolution-forward-learning]]

## My understanding

The experience library is one of the more compelling externalizations of "memory" for LLM agents: it sits above raw trajectory storage (Memento) and below fine-tuning, and its key empirical claim (a scaling law of experience) suggests it can extract structured returns from accumulated interaction. Whether it scales beyond curated benchmark settings is the open question.
