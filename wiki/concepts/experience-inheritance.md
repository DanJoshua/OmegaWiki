---
title: "Experience inheritance"
aliases:
  - experience transfer
  - cross-agent memory transfer
  - plug-and-play experience
tags:
  - self-evolving-agents
  - llm-agents
  - knowledge-transfer
  - multi-agent
maturity: emerging
key_papers:
  - flex-continuous-agent-evolution-forward-learning
first_introduced: "FLEX (Cai et al., 2025)"
date_updated: 2026-05-02
related_concepts:
  - experience-library
  - forward-learning-from-experience
---

## Definition

**Experience inheritance** is the property by which an experience library trained against one LLM agent transfers, in plug-and-play fashion, to a different agent (different base model, different tokenizer, different alignment) and yields measurable downstream gains without re-training.

## Intuition

When learned knowledge lives in model weights, it is locked to the source model's architecture and tokenization. When the same knowledge is stored as natural-language strategies in an experience library, it becomes substrate-independent: any agent that can read the library can use it. This decouples learning cost from deployment fleet size — one expensive training pass can produce a cognitive artifact reused across many agents.

## Formal notation

Given two agents $\pi_A$ and $\pi_B$, and a library $\mathcal{E}_A$ trained against $\pi_A$, inheritance asks whether $\mathbb{E}[\Phi(\pi_B(\cdot \mid X, \rho(\cdot \mid X, \mathcal{E}_A)), Y)] > \mathbb{E}[\Phi(\pi_B(\cdot \mid X), Y)]$ — i.e., whether $\pi_B$ benefits from $\mathcal{E}_A$ without any joint training.

## Variants

- **Strong-to-weak distillation**: stronger source model's library uplifts weaker target models. (E.g., Claude-Sonnet-4.5 library lifts Gemini-2.5-Pro by +11 on USPTO50k.)
- **Weak-to-strong generalization**: a weaker source model's library still benefits a stronger target. (E.g., Claude-Sonnet-4 library lifts DeepSeek-V3.1 to its own ceiling on AIME25.)
- **Library mixing**: combining libraries from heterogeneous sources (open question).

## Comparison

- vs. **knowledge distillation**: classical distillation transfers via output logits and requires both models to train together; experience inheritance is post-hoc and gradient-free.
- vs. **prompt transfer**: a learned prompt can transfer, but its capacity is bounded by context length; an experience library is a retrieval-mediated, expandable knowledge base.
- vs. **weight-merging / model souping**: weight-merging requires architecture compatibility; experience libraries are architecture-agnostic.

## When to use

Multi-agent fleets where cost amortization matters; environments mixing open- and closed-source models; settings requiring auditable, human-curatable shared knowledge.

## Known limitations

- Demonstrated only pairwise; mixing libraries from differently-aligned sources may produce negative transfer.
- Inheritance gains observed are domain-bounded (math, chemistry, biology benchmarks); behavior in agentic-software / multi-turn tool use is untested.
- Vulnerable to "library poisoning" if a source agent's failure-mode patterns are encoded as if they were lessons.

## Open problems

- Detecting and quarantining incompatible entries when merging libraries.
- Formal characterization of when weak-to-strong inheritance succeeds vs. fails.
- Distillation efficiency: how compact can an inherited library be while preserving most of the gain?

## Key papers

- [[flex-continuous-agent-evolution-forward-learning]]

## My understanding

The most provocative empirical claim from FLEX. If experience inheritance generalizes beyond curated benchmarks, it implies a future where experience libraries are first-class artifacts shared across agents — much like model checkpoints today — and the economics of agent training shift from per-agent fine-tuning toward shared-substrate exploration.
