---
title: "Graph-structured skill retrieval outperforms flat skill libraries on compositional tasks"
slug: graph-structured-skill-retrieval-outperforms-flat
status: weakly_supported
confidence: 0.72
tags:
  - skill-management
  - agents
  - compositional-tasks
  - graph
  - retrieval
domain: "NLP"
source_papers:
  - skillgraph-skill-augmented-reinforcement-learning-agents
evidence:
  - source: skillgraph-skill-augmented-reinforcement-learning-agents
    type: supports
    strength: strong
    detail: "SkillGraph outperforms ExpeL (best flat-retrieval baseline) by 44.3 points on ALFWorld; gains are largest on prerequisite-ordered subtasks (Clean +44.2, Heat +43.8). Ablation of graph-aware retrieval alone costs -31.2 on ALFWorld. On WebShop, graph structure ablation costs -11.7."
conditions: "Evidence is from a single paper and two benchmarks (ALFWorld, WebShop) with a specific base model (Qwen2.5-7B). Generalization to other task types and base models is unverified."
date_proposed: 2026-05-14
date_updated: 2026-05-14
---

## Statement

Organizing an agent's reusable skill library as a directed dependency graph — with typed prerequisite, enhancement, and co-occurrence edges — and using graph-aware, topologically ordered retrieval yields substantially higher performance on compositional multi-step tasks compared to flat skill libraries that retrieve independently via semantic similarity. The gain is especially large for tasks with strict prerequisite orderings.

## Evidence summary

- [[skillgraph-skill-augmented-reinforcement-learning-agents]] (SkillGraph, NeurIPS 2026): graph-aware retrieval ablation removes 31.2 points on ALFWorld (where clean/heat subtasks require strict ordering). Over best flat-retrieval memory method (ExpeL): +44.3 on ALFWorld. Ablation of graph structure on WebShop: -11.7.
- No countervailing evidence yet in wiki.

## Conditions and scope

- Demonstrated on ALFWorld (household manipulation) and WebShop (web navigation) with Qwen2.5-7B-Instruct as the base policy.
- The gain on prerequisite-ordered tasks (Clean, Heat) is much larger than on flexible-order tasks (WebShop); benefit is task-structure-dependent.
- The graph also co-evolves during RL training — pure retrieval benefit is partially confounded with the benefit of the evolution loop.

## Counter-evidence

None in wiki yet. Candidate counterarguments: (1) gains may be partially attributable to better skill quality from the graph-evolution loop rather than graph retrieval per se; (2) flat libraries with post-hoc dependency annotations could close the gap.

## Linked ideas

## Open questions

- Does the gain transfer to open-ended long-horizon tasks (e.g., SWEBench, OSWorld) where prerequisite structure is implicit?
- How much of the gain is retrieval ordering vs. graph evolution quality?
