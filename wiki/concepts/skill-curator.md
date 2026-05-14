---
title: "Skill Curator"
aliases:
  - trainable skill curator
  - skill curation policy
  - RL skill curator
tags:
  - agents
  - self-evolving-agents
  - skill-management
  - reinforcement-learning
  - procedural-memory
maturity: emerging
key_papers:
  - skillos-learning-skill-curation-self-evolving
  - skillgraph-skill-augmented-reinforcement-learning-agents
first_introduced: "2026"
date_updated: 2026-05-14
related_concepts:
  - skill-lifecycle
  - agentic-skill
  - experience-library
  - graph-structured-skill-library
---

## Definition

A **skill curator** is a dedicated, trainable policy module responsible for managing an agent's external skill repository — deciding when to insert new skills, update existing ones, and delete obsolete ones, based on interaction trajectories and downstream task performance. The curator is architecturally decoupled from the *agent executor* (the policy that uses skills to solve tasks), enabling each component to be optimised independently.

Formally, given a skill repository $\mathcal{S}_t$ and the executor's trajectory $\xi_t$ on task $x_t$ (plus a self-judged correctness signal $\mathbbm{1}_{\xi_t}$), the curator policy $\pi_{\mathcal{S}}$ produces a sequence of structured curation operations:
$$c_t = (u_t^1, \ldots, u_t^{M_t}) \sim \pi_{\mathcal{S}}(\cdot \mid \xi_t, \mathbbm{1}_{\xi_t}, \tilde{\mathcal{S}}_t)$$
where each $u_t^m \in \{\texttt{insert}, \texttt{update}, \texttt{delete}\}$. Applying these transforms the repository: $\mathcal{S}_{t+1} = \textsc{ApplyOps}(\mathcal{S}_t, c_t)$.

## Intuition

Most skill-based agent systems conflate two distinct problems: *using* skills (which depends on the executor's capacity and domain knowledge) and *managing* the skill library (which depends on understanding which skills are durable, composable, and matched to the executor's actual strengths). Conflating them — by having the same policy both retrieve-and-apply and curate — makes each objective harder.

Separating the curator from the executor allows the curation policy to be trained with signals that are invisible at execution time: whether skills induced from *earlier* tasks actually help on *later related* tasks (a delayed credit-assignment signal). This is analogous to separating a librarian (who decides what goes in the library) from a reader (who looks up what is there), where the librarian's job requires a longitudinal view not available during any single retrieval.

## Formal notation

**Modular two-component design (SkillOS):**

- **Frozen executor** $\pi_{\mathcal{L}}$: retrieves relevant skills $\tilde{\mathcal{S}} \subseteq \mathcal{S}$ by BM25, conditions on $(x_t, o_t, \tilde{\mathcal{S}}_t)$, produces trajectory $\xi_t$.
- **Trainable curator** $\pi_{\mathcal{S}}$: observes $(\xi_t, \mathbbm{1}_{\xi_t}, \tilde{\mathcal{S}}_t)$, emits curation operations; trained via GRPO.

**Composite reward for curator training:**
$$r = r^{\text{task}} + \lambda_f r^{\text{fc}} + \lambda_u r^{\text{cnt}} + \lambda_c r^{\text{comp}}$$
- $r^{\text{task}}$: average executor success on tasks 2…|G| (downstream performance signal)
- $r^{\text{fc}}$: fraction of valid function calls (structural correctness)
- $r^{\text{cnt}}$: LLM judge score on curated skill content (semantic quality)
- $r^{\text{comp}}$: compression ratio (discourages verbatim trajectory copying)

**Grouped task stream training:** Related tasks are grouped so that curator decisions on task $i$ propagate to tasks $i+1, \ldots, |G|$, making the long-term utility of each curation decision observable during training.

## Variants

- **Prompt-only curator**: a strong LLM (e.g., Gemini-2.5-Pro) used zero-shot as the curator. Simple and requires no training, but produces skills misaligned with the executor's capacity — a curator-executor mismatch.
- **Heuristic curator**: rule-based operations (e.g., always insert, merge by similarity). No training needed; deterministic but cannot adapt to long-term curation quality.
- **RL-trained curator (SkillOS)**: trainable policy optimised with GRPO on grouped task streams. Learns executor-grounded curation behaviours; an 8B RL curator outperforms zero-shot frontier-model curators.
- **Joint curator-executor training**: not yet studied; the curator and executor co-evolve, which introduces distribution-shift challenges but may yield tighter alignment.

## Comparison

| Curator type | Training signal | Executor alignment | Long-horizon curation |
|---|---|---|---|
| Human (manual) | Human judgment | High (by design) | N/A |
| Prompt-only (frontier LLM) | None | Low (scale ≠ alignment) | No |
| Heuristic | None | None | No |
| RL-trained (SkillOS) | Grouped task stream reward | High (executor-grounded) | Yes |

Key insight: a small RL-trained curator can outperform a frontier LLM curator because *executor alignment*, not raw reasoning ability, determines curation quality. Skills that work well for a small executor differ from skills that work for a frontier model.

## When to use

- The agent operates in a **streaming task setting** where the same skill domains recur across many tasks.
- Skill curation quality is the performance bottleneck (executor is capable, but skill library is stale or noisy).
- Training signal is available: either task-outcome feedback or proxy rewards (LLM judge, structural validity).
- The executor is stable enough to serve as a fixed reference point for curation training.

## Known limitations

- Curator training requires constructing grouped task streams, which demands domain-specific task-attribute annotation.
- The frozen executor assumption means the curator is optimised for a specific executor; re-training is needed if the executor changes.
- BM25 retrieval limits skill selection quality; the curator cannot compensate for poor retrieval.
- Validated on household navigation and web shopping domains; generalisation to open-ended code generation and long-horizon planning is unconfirmed.

## Open problems

- **Cross-executor transfer**: can a curator trained on executor A be fine-tuned cheaply for executor B?
- **Hierarchical skill curation**: can the curator manage both atomic skills and higher-level meta-skills in a structured hierarchy?
- **Multi-agent shared curators**: can multiple agents share a single curator while maintaining per-agent executor alignment?
- **Drift handling**: as the executor updates over time, how should the curator detect and respond to drift in which skills are useful?

## Key papers

- [[skillos-learning-skill-curation-self-evolving]] — introduces the skill curator design pattern and RL training recipe

## My understanding

The skill curator concept is a natural but previously underexplored decomposition of the self-evolving agent problem. Most prior work either treats the whole agent as a single policy (hard to credit-assign curation decisions) or keeps curation heuristic (misses long-term optimisation). SkillOS shows that freezing the executor and training only the curator is a tractable and effective simplification. The main open question is whether this modular view survives when both the executor and curator need to co-evolve — the split is cleanest when the executor is fixed.
