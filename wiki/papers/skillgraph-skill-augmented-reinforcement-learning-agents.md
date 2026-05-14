---
title: "SkillGraph: Skill-Augmented Reinforcement Learning for Agents via Evolving Skill Graphs"
slug: skillgraph-skill-augmented-reinforcement-learning-agents
arxiv: "2605.12039"
venue: "NeurIPS 2026 (preprint)"
year: 2026
tags:
  - agents
  - llm-agents
  - self-evolving-agents
  - skill-management
  - skill-lifecycle
  - reinforcement-learning
  - graph-structured
  - compositional-tasks
importance: 3
date_added: 2026-05-14
source_type: tex
s2_id: ""
keywords:
  - skill graph
  - dependency-aware retrieval
  - graph evolution
  - GRPO
  - skill composition
  - progressive unlocking
  - co-evolution
domain: "NLP"
code_url: ""
cited_by: []
---

## Problem

Flat skill libraries — where skills are stored as isolated entries and retrieved by semantic similarity alone — fail in two ways: (1) **retrieval is not compositional**: complex multi-step tasks require skills in dependency order, which a Top-K similarity search cannot enforce; (2) **skill updates are not structured**: without explicit inter-skill relations, the library lacks principled cues for merging redundant skills, splitting overly broad skills, or deprecating failures. Existing approaches such as ExpeL and SkillRL treat each skill as independent, so compositional sequential tasks suffer from retrieval that returns relevant skills in no guaranteed execution order.

## Key idea

Represent the skill library as a **directed dependency graph** with typed relational edges (prerequisite, enhancement, co-occurrence). Retrieval traverses this graph — expanding from task-relevant seed skills via BFS (backward) and beam search (forward), then topologically sorting the result — to produce a dependency-ordered skill sequence that acts as compositional guidance for the agent. The graph **co-evolves** with the agent's policy during RL: node-level operations (insert, merge, split, deprecate) and edge-level operations (path reinforcement, co-occurrence discovery, decay-and-pruning) continuously refine both skill quality and relational structure. A **progressive unlocking** curriculum exposes higher-level skills only after lower-level skills have reached a success threshold.

## Method

**Graph structure.** Nodes are skills distilled from trajectories (title, core principle, applicability condition, category label). Edges carry weights $w(e) \in [0,1]$ and belong to three types: `prereq` (A must be applied before B), `enhance` (general skill A improves task-specific skill B), `co_occur` (A and B frequently succeed together). Each node tracks usage count, success count, and success rate $\hat{p}(v)$; topological level $\ell(v)$ encodes dependency depth.

**Graph-aware retrieval.** Given task description $d$ with type $t(d)$:
1. Seed selection: all general and $t(d)$-type skills from the active set.
2. Backward BFS (depth $D=2$) to recover foundational prerequisites.
3. Forward beam search (width $B=3$) weighted by propagated relation strength.
4. Topological sort of the union, capped at $K_{\max}=8$ skills, prepended to prompt.

**Graph evolution** (at each validation checkpoint): *Insert* new skills targeting unhandled failures; *Merge* skills with Jaccard-similar neighborhoods ($\tau_{\text{merge}} = 0.85$); *Split* high-usage/medium-success skills ($\hat{p} \in [0.15, 0.4]$); *Deprecate* high-usage/low-success skills ($\hat{p} < 0.15$). *Path reinforcement* increments edge weights by $\alpha = 0.05$ on successful paths; *Co-occurrence discovery* adds new edges; multiplicative decay ($\gamma = 0.99$) prunes stale edges below $w_{\min} = 0.05$.

**Policy optimization.** GRPO with Qwen2.5-7B-Instruct; teacher model is OpenAI o3 (distillation + graph operations). Closed training loop: better policy → richer trajectories → refined graph → better retrieval → better policy.

## Results

On **ALFWorld** (six household manipulation categories): SkillGraph surpasses the best flat-retrieval baseline (ExpeL) by 44.3 points overall, with the largest gains on Clean (100.0 vs. 55.0) and Heat (100.0 vs. 56.2) — subtasks with strict prerequisite ordering. Outperforms GPT-4o by 42.6 points and Gemini-2.5-Pro by 30.3 points with a 7B model. Over vanilla GRPO: +13.0 points.

On **WebShop** (web navigation): +18.3 over GRPO; +11.7 over SkillRL. The graph evolution component contributes the most ($-14.1$ when removed), reflecting that skill quality matters more than ordering in this flexible navigation domain.

On **seven search-augmented QA tasks** (NQ, TriviaQA, PopQA, HotpotQA, 2Wiki, MuSiQue, Bamboogle): average 48.9, best overall; trained only on NQ + HotpotQA and generalizes zero-shot to five unseen datasets. Prerequisite-ordered retrieval helps multi-hop tasks decompose chained queries.

Graph evolution dynamics: node count grows ~20 → ~140 but active count plateaus as deprecation self-regulates; co-occur edges grow fastest; average node success rate rises steadily.

## Limitations

- Relies on a strong teacher model (o3) for skill distillation and graph operations — significant inference cost during evolution.
- Skill graph is built and evolved within a single environment; cross-environment transfer is unexplored.
- Scaling to larger base models and more diverse task distributions is an open question.

## Open questions

- Can self-distillation (agent distills its own skills) replace the expensive teacher model in graph evolution operations?
- How does a pre-trained SkillGraph transfer to a new environment via few-shot graph bootstrapping?
- Does graph topology eventually converge, or does it grow unboundedly as task diversity increases?

## My take

SkillGraph is a clean extension of the flat-skill-library paradigm: the core insight — that inter-skill relations are valuable structural information, not noise — is correct, and the results on prerequisite-ordered tasks are especially convincing. The co-evolution loop (policy ↔ graph) is tight and well-motivated. Limitations are honest: the teacher-model cost is real, and the single-environment graph is a significant constraint for practical deployment. The connection to the wiki's `skill-lifecycle` concept is direct — SkillGraph is essentially a fully implemented retrieval/composition + evaluation/update loop with explicit graph structure. A natural successor would try skill-graph sharing across environments (cross-domain skill transfer).

## Related

- [[skillos-learning-skill-curation-self-evolving]] — trainable skill curator with RL; focuses on insert/update/delete decisions rather than graph topology
- [[skill-r1-agent-skill-evolution-reinforcement]] — recurrent skill evolution with bi-level GRPO; evolves skill text, not library structure
- [[evolver-self-evolving-llm-agents-through]] — self-distillation of experience principles; flat experience base, no graph
- [[sok-agentic-skills-beyond-tool-use]] — taxonomizes skill lifecycle and governance; SkillGraph implements retrieval/composition + evaluation stages
- [[skillgen-verified-inference-time-agent-skill]] — contrastive skill synthesis; complementary (acquisition vs. organization)
- [[graph-structured-skill-library]] — concept introduced by this paper
- [[graph-structured-skill-retrieval-outperforms-flat]] — claim introduced by this paper
- [[skill-lifecycle]]
- [[skill-curator]]
- [[recurrent-skill-evolution]]
