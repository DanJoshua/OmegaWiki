---
title: "Deep and Wide Information Seeking"
aliases:
  - depth-width information seeking
  - deep-wide search
  - combined deep and wide search
  - deep+wide retrieval
tags:
  - agents
  - information-seeking
  - search-agents
  - benchmark
maturity: emerging
key_papers:
  - deepwidesearch-benchmarking-depth-width-agentic-information
first_introduced: "2025"
date_updated: 2026-05-02
related_concepts: []
---

## Definition

*Deep and wide information seeking* is the joint capability of an agent to (a) identify many target entities relevant to a query (the *width* axis: row-level coverage of an answer table) and (b) recover non-trivial multi-hop facts about each entity (the *depth* axis: per-row column verification that requires multiple search steps). The output is typically a structured table whose rows are entities the agent must discover and whose columns are attributes the agent must populate from the web.

It is not a new tool or architecture; it is an evaluation/capability axis that exposes a combinatorial regime that single-axis benchmarks (deep-only or wide-only) miss.

## Intuition

Two dimensions, one quadrant:

- *Low width, high depth* — find one tricky entity (GAIA, BrowseComp).
- *Low width, low depth* — answer a single fact-finding question (TriviaQA, HotpotQA).
- *High width, low depth* — fill a large table whose rows are given (WideSearch, PaSa).
- *High width, high depth* — discover the rows *and* verify them column by column. This is the deep-and-wide quadrant.

Real-world examples: "list the top-10 EV makers in China by MoM sales growth in Aug 2025 and their top-3 best-selling new EVs (price and range)"; market analysis; competitor benchmarking; literature gap analysis with structured outputs.

## Formal notation

A deep-and-wide task is a tuple `(Q, C)` where:

- `Q` is a natural-language query that does not enumerate the target entities.
- `C = {c_1, ..., c_N}` is a column schema specifying the attributes that must be filled per entity.

The agent must output a table `R` with rows `{r_1, ..., r_M}`, where each `r_i` is an entity satisfying `Q` and `r_i.c_j` is an atomic value for column `c_j`. Discovering `r_i` requires multi-hop search (depth); covering all `r_i` requires broad enumeration (width).

Standard metrics decompose along both axes:

- depth: Column-F1, Core Entity Accuracy
- width: Row-F1, Item-F1, Success Rate (whole-table exact match)
- efficiency: input/output tokens, dollar cost, tool-call counts

## Variants

- *Deep2Wide instances* — start from a deep single-entity question, augment with a table schema describing the entity's attributes.
- *Wide2Deep instances* — start from a wide table-filling question, replace each explicit core entity with a synthesized sub-question that requires a hop to recover.
- *Real-world deep-and-wide* — naturally arising BD / market-research / scientific-literature queries whose answer is a structured table the analyst must build from scratch.

## Comparison

- vs *deep search* (BrowseComp, GAIA): adds the requirement to discover and verify *many* entities, multiplying retrieval load.
- vs *wide search* (WideSearch, PaSa): the rows are not given; finding them requires multi-hop reasoning per row.
- vs *deep research* in the OpenAI sense: deep research often produces prose; deep-and-wide search produces a structured table whose entries each have a verifiable ground truth.

## When to use

Use this framing when:

- The query implicitly enumerates an unknown set of entities (top-K, all-of, list-of) *and* requires non-trivial verification per entity.
- A correct answer is checkable cell by cell against authoritative sources.
- The agent's bottleneck is plausibly context length, retrieval coverage, or coordination across many sub-searches rather than one tricky reasoning hop.

## Known limitations

- Reference-based evaluation requires expensive human-curated tables.
- Construction-method asymmetry — synthesizing deep sub-questions on top of wide tables tends to produce easier instances than the reverse.
- Solution paths can drift from how a real analyst would approach the same question, blunting external validity.
- Pure deep-and-wide setups may overstate context-management failures relative to settings where browser-use agents can persist state externally.

## Open problems

- Reflection-driven replanning when a trajectory fails on either axis.
- Internal-knowledge-vs-search arbitration for column filling.
- Context management strategies for trajectories that span dozens of search and visit calls.
- Reference-free evaluation so benchmarks can scale beyond hand-curated tables.
- Architectures that explicitly decompose row-discovery from column-filling pipelines.

## Key papers

- [[deepwidesearch-benchmarking-depth-width-agentic-information]] — formalizes the task, releases the first benchmark, reports four failure modes.

## My understanding

Deep-and-wide is best read as a *load* axis on top of existing search benchmarks: it doesn't introduce a new reasoning primitive, it just composes depth and width far enough that current agents collapse under the combinatorial cost. The interesting design space it opens is meta-cognitive — how agents decide when to search, when to trust internal knowledge, when to replan, and how to keep their working memory under control across very long trajectories. Improvements on this axis will probably look more like context engineering and controller design than like tool innovation.
