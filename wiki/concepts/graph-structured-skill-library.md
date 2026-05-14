---
title: "Graph-Structured Skill Library"
aliases:
  - skill dependency graph
  - graph-aware skill retrieval
  - directed skill graph
tags:
  - agents
  - skills
  - skill-management
  - graph
  - compositional-tasks
maturity: emerging
key_papers:
  - skillgraph-skill-augmented-reinforcement-learning-agents
first_introduced: "2026"
date_updated: 2026-05-14
related_concepts:
  - skill-lifecycle
  - skill-curator
  - agentic-skill
  - experience-library
---

## Definition

A **graph-structured skill library** is an agent skill store in which reusable skills are represented as nodes in a directed graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, and typed weighted edges encode explicit inter-skill relations: `prereq` (A must precede B), `enhance` (general skill A improves task-specific skill B), and `co_occur` (A and B frequently co-appear in successful episodes). In contrast to **flat skill libraries** — where skills are stored as independent entries retrieved by semantic similarity — the graph makes compositional dependencies explicit, enabling dependency-ordered retrieval and principled structural evolution.

## Intuition

Flat skill libraries answer "which skills are relevant?" but not "in what order should they be applied?" For multi-step tasks with strict prerequisites (e.g., heat-and-place in ALFWorld requires locate → pick → heat → place), Top-K similarity returns the right skills in arbitrary order. A graph library encodes that `locate` must precede `pick`, so retrieval produces a topologically sorted skill sequence that acts as a step-by-step plan.

The graph also provides structural signals for maintenance: two skills with highly overlapping graph neighborhoods (similar co-occurrence patterns) are likely redundant and should be merged; a skill with high usage but moderate success (success rate 0.15–0.4) conflates distinct sub-strategies and should be split; a consistently failing high-usage skill should be deprecated.

## Formal notation

Given skill node set $\mathcal{V}$ and edge set $\mathcal{E}$, graph-aware retrieval for task $d$ with type $t(d)$:

$$\mathcal{R}_{\text{ret}} = \text{TopoSort}_{\mathcal{G}}\!\left(\mathcal{R}_{\text{seed}} \cup \mathcal{R}_{\text{BFS}} \cup \mathcal{R}_{\text{beam}}\right)$$

where $\mathcal{R}_{\text{seed}}$ selects general and $t(d)$-type skills from the active set, $\mathcal{R}_{\text{BFS}}$ recovers foundational prerequisites via backward BFS, and $\mathcal{R}_{\text{beam}}$ expands forward via beam search weighted by edge weights.

Edge weights $w(e) \in [0,1]$ evolve via path reinforcement on successful trajectories ($+\alpha$), multiplicative decay ($\times \gamma$), and pruning below $w_{\min}$.

## Variants

- **Single-domain graph** (SkillGraph baseline): built and evolved within one environment; nodes are task-type-labeled.
- **Cross-domain graph** (hypothetical): shared prerequisite structure bootstrapped across environments; unexplored as of 2026.
- **Typed-edge variants**: three-type (prereq/enhance/co_occur) vs. richer ontologies (e.g., precondition/postcondition/conflict).

## Comparison

| Property | Flat skill library | Graph-structured skill library |
|---|---|---|
| Retrieval signal | Semantic similarity | Typed relational edges |
| Output | Unordered Top-K set | Topologically sorted sequence |
| Maintenance cues | Heuristic | Neighborhood overlap, success rate |
| Compositional tasks | Weak | Strong |
| Implementation cost | Low | Higher (teacher model for evolution) |

## Known limitations

- Teacher model dependency: graph evolution operations (insert, merge, split) rely on a strong LLM (e.g., o3), adding significant inference cost during training.
- Single-environment scope: skills and their relational edges are built within one domain; transfer requires re-distillation.
- Graph growth: unbounded insertion may grow the graph faster than deprecation prunes it, especially in diverse task settings.

## Open problems

- Can the graph be shared across environments with minimal adaptation (cross-domain skill transfer)?
- What graph topology invariants (e.g., depth, diameter, branching factor) correlate with agent performance?
- Can the graph be learned end-to-end rather than constructed by a separate teacher model?

## Key papers

- [[skillgraph-skill-augmented-reinforcement-learning-agents]] — introduced graph-structured skill library with co-evolution
