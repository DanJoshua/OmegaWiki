---
title: "EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle"
slug: evolver-self-evolving-llm-agents-through
arxiv: "2510.16079"
venue: "arXiv"
year: 2025
tags:
  - self-evolving-agents
  - experience-distillation
  - reinforcement-learning
  - multi-hop-qa
  - agent-memory
importance: 3
date_added: 2026-05-02
source_type: tex
s2_id: "26f887d7fd771f2e32ce52833a114d35df36aab2"
keywords:
  - experience-driven distillation
  - agent self-evolution
  - strategic principle abstraction
  - GRPO
  - dynamic experience curation
domain: "NLP"
code_url: "https://github.com/Edaizi/EvolveR"
cited_by: []
---

## Problem

Standard LLM agents treat each task as an isolated episode: they discard interaction trajectories after every run and cannot systematically refine their problem-solving strategies. Existing remedies fall into two unsatisfying buckets — (1) external-teacher distillation, where a powerful third-party LLM writes natural-language reflections that the agent merely consults as a transient hint, leaving its policy unchanged; and (2) raw-trajectory memory (e.g., ExpeL, Memento), where the agent retrieves entire past cases and tends to mimic them rather than abstract reusable principles. Neither approach closes the loop between **interaction**, **abstraction**, and **policy update**, so accumulated experience never becomes durable expertise.

## Key idea

EvolveR organises an LLM agent into a closed-loop **experience lifecycle** with three interlocking phases:

1. **Offline self-distillation** — with policy parameters frozen, the agent re-reads its own past trajectories, role-plays an "expert," and emits a *guiding principle* (from successes) or *cautionary principle* (from failures). Each principle is stored as a natural-language description plus structured knowledge triples.
2. **Online interaction** — at inference, the agent issues `search_experience` calls to retrieve relevant principles from its experience base $\mathcal{E}$ and conditions its think/search/answer loop on them, generating new, principle-guided trajectories.
3. **Policy evolution via GRPO** — the trajectories collected online drive Group Relative Policy Optimisation, so the agent literally learns *how to use its own distilled wisdom* rather than a generic reasoning policy.

The experience base is curated, not just appended: new principles are deduplicated by embedding similarity plus a model-judged binary equivalence check, merged into matches when redundant, and pruned by a Laplace-smoothed empirical utility score $s(p) = (c_{\text{succ}} + 1)/(c_{\text{use}} + 2)$.

## Method

- **Action space**: `search_experience` (query $\mathcal{E}$), `search_knowledge` (external retriever), `answer`. A free-form `think` precedes actions.
- **Principle representation**: NL summary + structured knowledge triples, inspired by Mem0 and G-Memory.
- **Curation**: pairwise semantic dedup within a problem; two-stage merge-vs-create against $\mathcal{E}$ — embedding-NN retrieval, then LLM equivalence judgment; prune below threshold $\theta_{\text{prune}}$.
- **Reward**: $R(\tau) = w_o R_{\text{outcome}} + w_f R_{\text{format}}$. Outcome is binary EM against ground truth; format rewards balanced think counts and the presence of search actions, gated by a structural-completeness indicator (must contain at least one `think`, one search action, and one `answer`).
- **Optimiser**: GRPO with importance-sampling ratio, clipped surrogate, and KL penalty to a reference policy. Sample group size $G=8$, batch 128 prompts, lr $1\mathrm{e}{-6}$, 20-step warmup, 8× A100 on the verl framework.
- **Cold-start**: LoRA fine-tuning on ~700 CoT trajectories sampled from NQ + HotpotQA training splits, à la Search-R1.
- **Backbones evaluated**: Qwen2.5-0.5B / 1.5B / 3B.

## Results

Evaluation covers seven QA benchmarks: in-domain NQ + HotpotQA (training splits used to seed $\mathcal{E}$); out-of-domain TriviaQA, PopQA, 2WikiMultiHopQA, Musique, Bamboogle. Primary metric is Exact Match.

- On Qwen2.5-3B, EvolveR averages **0.382** EM, beating every baseline including Search-R1-instruct (0.325). It tops every benchmark column at this scale (NQ 0.434, HotpotQA 0.373, TriviaQA 0.584, PopQA 0.434, 2wiki 0.381, Musique 0.137, Bamboogle 0.328).
- **Scale generalisation**: average rises monotonically with backbone size — 0.150 (0.5B) → 0.270 (1.5B) → 0.382 (3B).
- **Self- vs teacher-distillation ablation**: at 0.5B and 1.5B, GPT-4o-mini distillation wins (0.220 vs 0.150; 0.290 vs 0.270). At 3B, **self-distillation wins (0.382 vs 0.370)**. The authors call this a "cognitive alignment" effect — once the policy is strong enough, principles distilled from its own internal representation suit it better than a teacher's.
- **Retrieval ablation**: removing access to $\mathcal{E}$ at inference (training unchanged) drops 3B average from 0.382 to 0.340; the gap widens for smaller models (0.150 → 0.078 at 0.5B).

## Limitations

- Distillation quality is fundamentally bounded by the base model's reasoning ability — the self-distillation advantage only materialises at ≥3B in their experiments. The 0.5B and 1.5B regimes still need an external teacher.
- All evaluations are single-domain (knowledge-intensive QA). The closed-loop story is untested on multi-step planning, code, embodied, or long-horizon tool-use settings where the cost of a bad principle is much higher.
- The empirical utility score $s(p) = (c_{\text{succ}}+1)/(c_{\text{use}}+2)$ has no exploration term; useful-but-rarely-triggered principles can be pruned before $c_{\text{use}}$ accumulates.
- Outcome reward is hard EM, which is brittle on multi-answer or paraphrased gold labels — the same trajectory can be marked failure under EM and success under F1, polluting the "guiding vs cautionary" labelling that drives distillation.
- No evidence is offered that principles transfer across base-model families; the experience base is co-evolved with one Qwen2.5 checkpoint per run.

## Open questions

- Does the cognitive-alignment crossover replicate at 7B+ or on instruction-tuned bases of comparable size? The trend line suggests yes, but the paper stops at 3B.
- Can the experience base be *shared* across agents at different scales, or is it fundamentally policy-specific?
- What happens under distribution shift — does pruning by $s(p)$ silently discard principles that were optimal for an earlier task family?
- How does EvolveR compose with retrieval-augmented external knowledge when both sources can answer; the paper trains them together but never disentangles their contributions.

## My take

The paper's contribution is less the components — self-distillation, structured memory, GRPO are all off-the-shelf — and more the **insistence on closing the loop with an RL update** rather than treating retrieved principles as a soft prompt. The teacher-vs-self crossover at 3B is the most interesting empirical claim: if it generalises, it's a non-obvious argument that scaling external supervision is dominated by scaling the agent's own reflective capacity past a threshold. I would treat the paradigm as a serious baseline for any future "agent learns continuously from its own runs" work, while remaining skeptical of generalisation beyond multi-hop QA until shown.

## Related

- [[experience-driven-self-evolution-lifecycle]] — the closed-loop paradigm this paper introduces
- [[self-distillation-vs-external-teacher-crossover]] — claim derived from the ablation
