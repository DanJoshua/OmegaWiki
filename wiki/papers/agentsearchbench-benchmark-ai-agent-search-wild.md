---
title: "AgentSearchBench: A Benchmark for AI Agent Search in the Wild"
slug: agentsearchbench-benchmark-ai-agent-search-wild
arxiv: "2604.22436"
venue: "arXiv (COLM 2026 submission)"
year: 2026
tags:
  - agent-search
  - benchmark
  - retrieval
  - reranking
  - llm-agents
  - execution-grounded-evaluation
importance: 3
date_added: 2026-05-02
source_type: tex
s2_id: "5e0ad2bd6906e48fd8465e55d7dd5dd5d765a61e"
keywords:
  - agent search
  - execution-grounded relevance
  - semantic-performance gap
  - behavioral probing
  - retrieval and reranking
domain: "NLP"
code_url: "https://github.com/Bingo-W/AgentSearchBench"
cited_by: []
---

## Problem

As third-party LLM-agent ecosystems explode (GPT Store, Google Cloud Marketplace, agent.ai, etc.), end users and orchestrators face a new challenge: *which agent should solve a given task?* Unlike traditional tools whose functionality is scoped to a clear API contract, agent capabilities are compositional and **execution-dependent**, so textual descriptions only weakly predict real performance. Existing tool-retrieval and agent-orchestration benchmarks assume well-specified functionalities, small controlled candidate pools, or executable queries only — they leave realistic *agent search* (large open pools, partial documentation, high-level user intent) insufficiently studied.

## Key idea

Treat agent selection as a **retrieval + reranking** problem whose ground truth comes from **executing** candidate agents on tasks rather than from textual similarity. The authors build *AgentBase*, a repository of nearly 10,000 real-world agents, and *AgentSearchBench*, a benchmark layered on top that supports both executable task queries (`T_q`) and high-level non-executable task descriptions (`T_d`). Relevance labels are derived from a 5-point LLM-as-judge applied to actual execution outcomes, and ranking labels further account for documentation-performance alignment (agents that succeed without documented capability are discounted).

## Method

- **Agent collection.** Scraped ~9,759 agents from GPT Store, Google Cloud Marketplace, and AgentAI Platform; ~7,867 expose executable interfaces. A unified four-group schema (metadata, capability description, usage guidance, availability/constraints) normalises heterogeneous documentation.
- **Task query construction.** Synthesised 2,452 single-agent and 500 multi-agent executable queries via document-grounded generation. A hybrid retrieval scorer `s = a*s_lex (BM25) + b*s_sem (BGE) + c*s_tool (ToolRet)` selects a top-K candidate pool to bound per-query evaluation cost. Multi-agent queries are composed from capability-aligned subtasks and validated by NLI entailment.
- **Task description construction.** 259 high-level descriptions, each abstracted from a cluster of ~10 related queries. A rubric-based judge with 5 aspects selects 2 representative queries per aspect to form `Q(T_d)`.
- **Relevance annotation.** For `T_q`, binary `rel = 1[y >= 4]`. For `T_d` and multi-agent queries, graded relevance is the fraction of subtasks with at least one relevant agent. Documentation-misaligned successes get discounted (e.g. 0.5).
- **Evaluation.** ~66,740 executions in total. Retrieval is benchmarked with sparse, dense, tool-aware, and decoder-only embedding families; reranking with cross-encoders, tool-specific rerankers, decoder-only rerankers, and LLM rankers (RankGPT). Metrics: Precision/Recall/NDCG/Completeness@K. *Completeness* requires at least one relevant agent per subtask in the top-K.
- **Execution-aware probing.** Augments description-based ranking with lightweight behavioural signals: (i) full-document indexing including usage examples, and (ii) explicit probing where LLM-generated probe queries are run on candidate agents and the responses scored as additional ranking features.

## Results

- **Retrieval (Task Query).** Tool-aware ToolRet leads (NDCG@5 = 37.52); BM25 (32.41) and BGE-Large (31.78) are close behind; SPLADE collapses (4.09). On Task Description the gap shrinks: BGE-Large (NDCG@5 = 23.08) edges out the tool-aware family — semantics matter more when queries are abstract.
- **Completeness is uniformly low.** Even the best retriever achieves only ~57% Completeness@20 on Task Query and <4% on Task Description, exposing a hard ceiling for description-only retrieval.
- **Reranking.** Tool-Rank 8B (NDCG@1 = 66.67 on `T_q`) and RankGPT GPT-5.2 (NDCG@1 = 66.00 on `T_d`) lead, but reranking gains over a *random shuffle* of the execution-grounded top-20 are modest, confirming a substantial semantic-performance gap.
- **Probing helps.** Full-document indexing (descriptions + usage examples) improves most retrievers and rerankers. Explicit execution probing adds another lift on most rerankers (e.g. Qwen Reranker 4B +1.56% NDCG@5, Tool-Rank 8B +1.46%) and is most effective when probe-score variance across agents is medium-to-high.
- **LLM-as-judge validation.** On 500 hand-annotated executions, LLM judgement matches three AI-PhD annotators with kappa = 0.93, accuracy 96.67%.

## Limitations

- **Synthetic-task framing.** Most queries are LLM-generated from documentation; the authors validate against HLE and a finance benchmark, but absolute performance there is much lower, so generalisation to fully realistic user intents is partial.
- **Judge dependence.** Both relevance labels and rubric-based query/description filtering rely on GPT-5.2 as judge; biases or stylistic preferences of that judge propagate into the gold labels.
- **Cost of execution.** Per-query evaluation is bounded by hybrid pre-retrieval to top-K, so any agent ranked outside that pool is invisible to the benchmark.
- **Probing brittleness.** RankGPT GPT-5.2 actually *loses* 2.69% NDCG@5 with probing — the signal is not strictly additive.
- **No dynamic agents.** AgentBase is a snapshot; capability drift, agent versioning, and live availability are not modelled beyond a single `Indexed` timestamp.

## Open questions

- Can execution-aware probing be made cheap enough (e.g. shared probe banks, cached responses) to deploy as a standard pre-rank layer in production agent stores?
- How should ranking handle *capability composition*: when no single agent covers a multi-step task, should retrievers surface complementary teams rather than top-1 individuals?
- What is the right unit of evaluation for self-evolving agents whose capabilities change between probing and deployment?
- Can the documentation-performance gap be closed at the *source* by inducing agent providers to publish execution traces or behavioural fingerprints?

## My take

AgentSearchBench is the first scale-credible benchmark for agent retrieval where labels come from execution rather than text similarity, and the resulting "semantic-performance gap" is a sharper, more useful framing than the usual "tool retrieval is hard" story. It is most valuable as a *fixture* — the framework, schema, and probing protocol are reusable even if specific GPT-Store agents churn — and as an invitation to a research direction: **execution as a first-class signal in agent indexing**. For self-evolving agents in particular, this benchmark is the natural place to test whether self-improvement actually translates into improved discoverability.

## Related

- [[agent-search]] — concept introduced here
- [[execution-grounded-relevance-vs-semantic-similarity]] — claim supported here
- [[self-evolving-agents]] — broader topic this benchmark feeds into
