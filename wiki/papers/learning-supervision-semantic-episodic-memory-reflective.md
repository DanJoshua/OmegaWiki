---
title: "Learning from Supervision with Semantic and Episodic Memory: A Reflective Approach to Agent Adaptation"
slug: "learning-supervision-semantic-episodic-memory-reflective"
arxiv: "2510.19897"
venue: "ACM Conference on AI and Agentic Systems (CAIS '26)"
year: 2026
tags:
  - agent-memory
  - episodic-memory
  - semantic-memory
  - test-time-learning
  - in-context-learning
  - agent-adaptation
  - reflective-learning
  - critique-generation
importance: 3
date_added: 2026-05-07
source_type: tex
s2_id: "ce907aa5956608438d6225d404644d78d25efccb"
keywords:
  - episodic memory
  - semantic memory
  - suggestibility
  - critique generation
  - agent adaptation
  - memory-augmented learning
  - parameter-free adaptation
domain: NLP
code_url: ""
cited_by: []
---

## Problem

LLM agents are deployment-time static: their capabilities are locked into pretrained parameters once training ends. Fine-tuning is the standard remedy but is computationally expensive, inflexible (requires retraining for every new task or domain), opaque, and impossible for closed-source models. Shallow in-context learning alternatives (few-shot RAG) recover surface-level patterns without deeper task understanding. The goal is to enable continuous, lightweight adaptation from labeled supervision without any parameter updates.

## Key idea

A two-tier memory architecture where a **critic agent** generates structured, label-grounded critiques for each training example, and the resulting critiques are stored as either:
- **Episodic memory** (instance-level: specific past experiences retrieved via RAG for similar test inputs)
- **Semantic memory** (dataset-level: all critiques distilled into a single set of reusable task-level principles)

The best strategy, EP+SEM_CRIT, combines both. Critiques are structured into three fields — **assertion** (restate correct answer), **rationale** (instance-specific explanation), **reflection** (generalizable insight) — to reduce confirmation bias in the critic model. The approach introduces **suggestibility** as a diagnostic metric: how receptive is a model to external reasoning in context, independent of its overall capability.

## Method

**Setup**: A performance agent (PA) with a frozen LLM + external memory module. A critic agent (CA, same underlying model) generates critiques for labeled training examples `(x_i, y_i)`.

**Critique generation**: CA receives `(x_i, y_i, PA(x_i))` and outputs structured critique (assertion / rationale / reflection). The three-part structure forces explicit acknowledgment of the correct answer, significantly reducing cases where the critic inherits its own parametric bias.

**Memory strategies evaluated**:
- `EP_LABEL`: episodic memory stores raw labels only (RAG baseline)
- `EP_CRIT`: episodic memory stores full critiques; top-K retrieved at test time (K=5)
- `SEM_CRIT`: semantic memory = single distilled summary of all critique reflections; prepended to prompt at test time
- `EP+SEM_CRIT`: hybrid combining both; best overall strategy
- `EP+SEM_CRIT_LOCAL`: variant with local semantic memory per example cluster

**Suggestibility metric**: Measures whether a model follows critique-encoded reasoning vs. its own parametric default. Higher suggestibility → higher expected benefit from memory augmentation, regardless of model scale.

## Results

- EP+SEM_CRIT yields **+8.1pp** over zero-shot baseline and **+4.6pp** over RAG-style EP_LABEL across 6 datasets and 7 models (fact-oriented: PubMed, BioASQ; preference: Steam, Movie, Anime, Book).
- Peak improvement: **+24.8pp** over RAG baseline on PubMed for gpt-4o-mini.
- Critique-generated memory **reduces thinking tokens by 31.95%** on average for reasoning models (GPT-5, Qwen3-thinking) by externalizing reasoning that would otherwise occur internally.
- Episodic consistently outperforms semantic (lazy vs. eager generalization).
- Suggestibility predicts benefit: Llama 4 Scout (suggestibility 56.2%) gains little; GPT-4o-mini gains most.
- Three failure-mode clusters identified: low-suggestibility models, reasoning models on preference data (already performing critique internally), and factual domains with low cross-instance critique transfer (PubMed).

## Limitations

- Single pair of memory tiers; richer hierarchical structures (G-Memory, H-MEM style) are not evaluated and may scale better to larger datasets.
- Critiques are pre-computed offline; real-time adaptation with streaming supervision not demonstrated.
- Suggestibility metric requires separate measurement; not yet causally linked to model architecture.
- All experiments on classification tasks; generalization to open-ended generation unclear.
- Critique quality depends on critic model's factual accuracy — domains where the base LLM has poor priors will produce low-quality critiques.

## Open questions

- Can suggestibility be predicted from model architecture or pretraining data?
- Does EP+SEM_CRIT scale to long-horizon, multi-turn agents where supervision is sequential and implicit rather than pre-labeled?
- How does critique-grounded memory interact with parameter-level test-time adaptation (LoRA, in-context fine-tuning)?
- Is the three-part critique structure universally optimal or domain-dependent?

## My take

A clean, well-controlled instantiation of the self-evolving memory paradigm in the supervised adaptation setting. The key contribution is not the episodic/semantic split (that exists in prior work) but the critique grounding: converting labeled examples into assertion+rationale+reflection entries is what differentiates this from RAG and explains the accuracy gains. The suggestibility metric is the most intellectually novel contribution — it reframes the "why does in-context learning work for some models but not others" question as a measurable property. The efficiency finding (31.95% token reduction for reasoning models) is a surprising practical payoff.

## Related

- [[self-evolving-memory]]
- [[experience-library]]
- [[forward-learning-from-experience]]
- [[test-time-learning]]
- [[suggestibility-metric-model-receptivity-external-reasoning]]
- [[critique-grounded-memory-improves-agent-adaptation]]
