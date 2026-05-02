---
title: "Description-based retrieval underperforms execution-grounded relevance for selecting AI agents"
slug: execution-grounded-relevance-vs-semantic-similarity
status: weakly_supported
confidence: 0.7
tags:
  - agent-search
  - retrieval
  - reranking
  - benchmark
  - llm-agents
domain: "NLP"
source_papers:
  - agentsearchbench-benchmark-ai-agent-search-wild
evidence:
  - source: agentsearchbench-benchmark-ai-agent-search-wild
    type: supports
    strength: strong
    detail: "Benchmark over ~9,759 real agents and 66,740 executions shows a persistent gap between best description-based retrievers/rerankers and the oracle execution-grounded ranking; Completeness@20 on Task Description stays below ~4% for every retriever, and reranking gains over a random shuffle of the execution-grounded top-20 are modest. Lightweight execution-aware probing improves most rerankers (e.g. Qwen Reranker 4B +1.56% NDCG@5)."
conditions: "Holds in open agent ecosystems where (a) the candidate pool is large (thousands of heterogeneous agents), (b) documentation styles and granularity vary across providers, and (c) at least some agents have overlapping or weakly-described capabilities. May not hold for small, well-curated tool/agent sets with normalised schemas."
date_proposed: 2026-05-02
date_updated: 2026-05-02
---

## Statement

Across realistic open agent ecosystems, retrieval and reranking systems that score agents by textual similarity to the user task systematically underperform an oracle ranking induced by actual agent execution outcomes. The gap is largest for high-level (non-executable) task descriptions, where description-based methods rarely surface agents that completely satisfy multi-subtask requirements. Lightweight behavioural signals (full-document indexing including usage examples, or explicit execution probing) reduce — but do not close — this gap.

## Evidence summary

- *AgentSearchBench* (2026): on 2,952 task queries and 259 task descriptions over ~9,759 agents, the best description-based retriever (ToolRet on `T_q`, BGE-Large on `T_d`) achieves Completeness@20 ~57% and ~3.4% respectively. Reranking strong cross-encoders, tool-rankers, and LLM rankers over the execution-grounded top-20 gains only modestly over a random shuffle (e.g. Tool-Rank 8B NDCG@1 = 66.67 vs random 51.43 on `T_q`). Probing yields consistent additional gains on most rerankers (e.g. +1.56% NDCG@5 for Qwen Reranker 4B).

## Conditions and scope

- The benchmark uses LLM-as-judge (GPT-5.2) to label execution outcomes, so the claim depends on that judge being a reasonable proxy for human relevance — validated at kappa = 0.93 on 500 human-annotated executions.
- Most queries are LLM-synthesised from agent documentation; absolute numbers on truly realistic queries (HLE, finance benchmark) are lower, but the *relative ordering* of method families is preserved, which is what this claim actually concerns.
- The claim is about open ecosystems with thousands of heterogeneous agents; in small curated tool sets (e.g. a fixed in-house agent registry with consistent schemas), description-based retrieval may already suffice.

## Counter-evidence

- RankGPT GPT-5.2 with execution probing *loses* 2.69% NDCG@5 on 100 task descriptions, showing probing is not strictly additive and can hurt very strong general-purpose LLM rerankers.
- Within the executable Task Query setting, BM25 already reaches NDCG@5 = 32.41, close to the best dense retriever (BGE-Large 31.78), suggesting that for sufficiently concrete queries, lexical matching alone is competitive.

## Linked ideas

- *(none yet — to be added by future `/ingest` or `/ideate` runs)*

## Open questions

- How cheap can execution-aware probing be made before its signal collapses?
- Does the gap shrink for self-evolving agents whose documentation is automatically updated from execution traces?
- Can agent providers be incentivised to publish behavioural fingerprints that close this gap at the source?
