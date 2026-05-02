---
title: "DeepWideSearch: Benchmarking Depth and Width in Agentic Information Seeking"
slug: "deepwidesearch-benchmarking-depth-width-agentic-information"
arxiv: "2510.20168"
venue: "arXiv"
year: 2025
tags:
  - agents
  - benchmark
  - information-seeking
  - search-agents
  - llm-agents
  - evaluation
importance: 3
date_added: 2026-05-02
source_type: tex
s2_id: "d53102facc1b5ea89a2490a7605685d18b21d1ad"
keywords:
  - deep search
  - wide search
  - multi-hop retrieval
  - agentic information seeking
  - benchmark
domain: "NLP"
code_url: "https://github.com/AIDC-AI/Marco-Search-Agent"
cited_by: []
---

## Problem

Existing benchmarks for LLM-based search agents evaluate either *depth* (multi-hop reasoning to find one entity, e.g. GAIA, BrowseComp) or *width* (broad atomic information collection over a known schema, e.g. WideSearch, PaSa) — but not both simultaneously. Many real-world tasks (comprehensive market analysis, business development, competitive intelligence) require an agent to gather a large set of candidate entities *and* perform deep multi-hop verification on each. No benchmark probes this combinatorial complexity, so progress on agents that must scale both dimensions has gone unmeasured.

## Key idea

Define *deep-and-wide information seeking* as the joint task of identifying many target entities (rows of a table) where each entity needs multi-step web search to be discovered and verified, and the columns themselves require additional retrieval per entity. Construct a benchmark — DeepWideSearch — by *converting* existing single-axis datasets along the missing axis: extending deep-search questions with annotated table schemas (Deep2Wide), or replacing explicit entities in wide-search questions with synthesized multi-hop sub-questions (Wide2Deep). Evaluate jointly with depth metrics (Column-F1, Core Entity Accuracy) and width metrics (Row-F1, Item-F1, Success Rate), plus efficiency (tokens, cost).

## Method

- **Dataset construction.** 220 questions, 15 domains, EN+ZH.
  - *Deep2Wide* (85 instances): sample 80 BrowseComp-zh + 20 BrowseComp questions whose answers are valid core entities, have human annotators design table schemas around each entity, then exhaustively populate the table from the web (~30 min/instance). Timestamps are added so answers stay invariant.
  - *Wide2Deep* (135 instances): take 160 WideSearch questions, extract the core entity with an LLM, recursively crawl official sites to gather entity facts, synthesize a deep sub-question that uniquely picks out the entity but requires at least one extra hop, fuse the sub-question into the original wide query (Claude Sonnet 4), then have seven master's-level annotators validate (~40 min/instance).
- **Task formulation.** Each task is a tuple `(Q, C)`: a natural-language query plus a set of column attributes `C = {c_i}`. Output is a structured table `R`.
- **Metrics.** Depth: Column-F1 (precision/recall over unique columns of the produced table) and Core Entity Accuracy. Width: Row-F1, Item-F1 (cell-level), and binary Success Rate (whole-table exact match). Efficiency: input/output token counts and dollar cost. Each system runs 4 times per question; report Avg@4, Max@4, and Pass@4.
- **Baselines.** Closed-source LLMs (o3-mini, GPT-4o, GPT-5, Claude Sonnet 4, Gemini 2.5 Pro, Qwen-Max), open-source LLMs (DeepSeek-V3/R1, KIMI-K2, Qwen3 family), and open-source agent frameworks (WebSailor, Smolagents, OWL) backed by GPT-5 / Claude Sonnet 4 / Gemini 2.5 Pro, all using Google Search + a webpage-visit tool with LLM summarization.

## Results

- **Headline.** Average Success Rate across all systems is **2.39%**; the best single configuration (e.g. Smolagents/Claude Sonnet 4, OWL/Claude Sonnet 4) reaches under 1% Avg@4 Success Rate. The benchmark is far from saturated.
- **Agents vs raw LLMs.** Agent frameworks improve depth metrics (e.g. +15.91 absolute points in Core Entity Accuracy on average) but not width — they often *underperform* their backbone LLM on Row-F1 and Item-F1, suggesting wide-scale information collection is not what scaffolds were designed for.
- **Cost.** OWL (GPT-5) averages ~\$2.75/query, ~\$6.8/query under retry; WebSailor (Claude Sonnet 4) averages ~\$1.40/query. Many of these costly runs still produce empty or wrong tables.
- **Tool-call scaling.** Within WebSailor, the Claude Sonnet 4 backbone issues 23.23 search calls/sample versus 4.77 (Gemini 2.5 Pro) and 8.72 (GPT-5), and is also the strongest on width metrics — more aggressive search correlates with better wide coverage.
- **Construction-method asymmetry.** Deep2Wide is much harder than Wide2Deep (Avg LLM Success Rate 0.0% vs 1.17%; Entity Accuracy 33.3% vs 88.8%), because Wide2Deep's synthesized sub-questions tend to be guessable from internal knowledge.
- **Per-topic.** Politics/Finance are easiest on depth metrics; History and Games are hardest across the board (e.g. Column-F1 ~5% on History).
- **Four failure modes** identified by error analysis:
  1. *Lack of reflection* — agents abort and return an empty table after a wrong trajectory or tool error instead of replanning.
  2. *Overreliance on internal knowledge* — even after correctly identifying the core entity, agents often fill the table from parametric memory rather than searching, producing stale/wrong cells.
  3. *Insufficient retrieval* — agents find the right pages but skip the visit step or rely on lossy LLM summaries that drop critical fields.
  4. *Context overflow* — observed in 24.96% of cases; deep+wide search produces trajectories that exceed the agent's context window.

## Limitations

- Wide2Deep questions, despite the synthesized hop, are still significantly easier than Deep2Wide (88.8% vs 33.3% Entity Accuracy), revealing limits of automatic deep-question synthesis.
- Authors note that solution paths in the curated questions don't always match real-world deep-and-wide queries (e.g. natural BD/market-research workflows).
- Heavy reliance on human annotation (30–40 min/instance, seven annotators) limits scalability of the benchmark itself.
- Reference-based evaluation requires complete human-verified tables; expanding the benchmark therefore inherits annotation cost.
- All baseline agents share the same tool stack (Google Search + Visit + LLM summarizer); results may not generalize to richer toolkits or browser-use agents.
- The 24.96% context-overflow figure is reported without a per-system breakdown, making it hard to attribute to specific architectures.

## Open questions

- Can a *reflection*-enabled controller (explicit replan after dead-end trajectories) close the gap on the four failure modes without ballooning cost?
- How should an agent decide when to trust internal knowledge vs trigger a search? The "internal-then-verify" hybrid is sketched but not tested.
- What context-management strategy (hierarchical memory, retrieval-augmented working memory, learned summarization) keeps deep+wide trajectories under context-window limits while preserving critical evidence?
- Can a reference-free evaluator be built so the benchmark scales beyond hand-curated tables?
- Will improvements on DeepWideSearch transfer to genuinely real-world BD / market-analysis workflows, or is the curated table format itself the bottleneck?

## My take

DeepWideSearch is a useful concrete instantiation of an evaluation gap that practitioners have felt for a while: most "deep research" demos quietly stop at one entity, and most wide-collection demos quietly assume the entity list is given. Forcing both axes simultaneously produces near-zero success rates across every flagship model and agent framework, which is a meaningful negative result. The dataset-construction trick (convert existing benchmarks along the missing axis instead of building from scratch) is pragmatic but inherits the parent benchmarks' biases — Wide2Deep being notably easier than Deep2Wide is direct evidence of this. The four failure modes are not surprising individually, but seeing them quantified together (especially context overflow at ~25%) is a useful reframing: scaling search agents is increasingly a context-management and meta-cognition problem rather than a planning or tool-use problem.

## Related

- [[deep-and-wide-information-seeking]] — the central capability this paper formalizes and benchmarks
- [[sota-agents-fail-deep-wide-information-seeking]] — the empirical claim this paper most directly supports
