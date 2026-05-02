---
title: "Self-distilled experience principles outperform external-teacher distillation once the agent's base model crosses a capacity threshold"
slug: self-distillation-vs-external-teacher-crossover
status: weakly_supported
confidence: 0.45
tags:
  - self-evolving-agents
  - experience-distillation
  - scaling
  - reinforcement-learning
domain: "NLP"
source_papers:
  - evolver-self-evolving-llm-agents-through
evidence:
  - source: evolver-self-evolving-llm-agents-through
    type: supports
    strength: moderate
    detail: "Qwen2.5-3B EvolveR (self-distill) average EM = 0.382 vs EvolveR (teacher-distill, GPT-4o-mini) = 0.370 across 7 QA benchmarks; the relationship reverses at 1.5B (0.270 vs 0.290) and 0.5B (0.150 vs 0.220), giving a monotone capacity-dependent crossover within one paper."
conditions: "Demonstrated only for Qwen2.5 backbones at 0.5B / 1.5B / 3B on knowledge-intensive multi-hop QA (NQ, HotpotQA, TriviaQA, PopQA, 2Wiki, Musique, Bamboogle), with EM as the outcome reward and GPT-4o-mini as the external teacher. The crossover scale and direction may differ for other architectures, larger backbones, instruction-tuned variants, non-QA tasks, or stronger/weaker teachers."
date_proposed: 2026-05-02
date_updated: 2026-05-02
---

## Statement

Within the experience-driven self-evolution paradigm, having the agent distill its own interaction trajectories into reusable principles starts to *beat* using a stronger external LLM as a distillation teacher once the agent's base model crosses some capacity threshold. Below the threshold, the external teacher dominates; above it, the agent's own distillation wins because principles drawn from its internal representation are more "cognitively aligned" with the policy that has to consume them.

## Evidence summary

The single supporting datapoint is the ablation table in EvolveR: at Qwen2.5-3B, self-distillation averages 0.382 EM versus 0.370 for GPT-4o-mini distillation; at 1.5B the order reverses (0.270 vs 0.290); at 0.5B it reverses more strongly (0.150 vs 0.220). This is a monotone capacity-dependent crossover within one paper but it has not been replicated on a different model family or task suite. The strength of the supporting evidence is *moderate* — same paper, controlled ablation — but the *generality* of the claim is unverified.

## Conditions and scope

The claim is well-defined only when the comparison fixes:

- the agent's base model and training procedure (here: Qwen2.5 + GRPO with the EvolveR loop and an EM outcome reward),
- the external teacher (here: GPT-4o-mini),
- the task family (here: multi-hop and single-hop knowledge QA),
- the principle representation and curation pipeline (here: NL + structured triples, embedding-NN dedup with an LLM equivalence judge, Laplace-smoothed pruning).

Changing any of these — particularly using a *much* stronger teacher (GPT-4o, Claude Opus, etc.) or a *weaker* base than 0.5B — could move the crossover scale up or down, or eliminate it entirely.

## Counter-evidence

None recorded yet. Plausible challenges to keep an eye on:

- A teacher much stronger than GPT-4o-mini could push the crossover above 3B and still dominate at small scales.
- On tasks with denser, more structured reward (e.g., code with unit tests, formal math), the teacher's advantage at distilling structure may persist longer.
- On tasks with sparse or noisy reward, self-distillation could amplify a base policy's blind spots, removing the crossover entirely.

## Linked ideas

None yet.

## Open questions

- Does the crossover replicate on Llama-, Mistral-, or DeepSeek-family backbones?
- Where does it sit on instruction-tuned models of comparable parameter count?
- Is "cognitive alignment" measurable directly (e.g., as some form of representational distance between the agent and its distilled principles), or is it only diagnosable post-hoc through the downstream EM gap?
