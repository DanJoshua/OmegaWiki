---
title: "State-of-the-art LLM agents fail at combined deep + wide information seeking"
slug: "sota-agents-fail-deep-wide-information-seeking"
status: weakly_supported
confidence: 0.7
tags:
  - agents
  - benchmark
  - search-agents
  - information-seeking
  - evaluation
domain: "NLP"
source_papers:
  - deepwidesearch-benchmarking-depth-width-agentic-information
evidence:
  - source: deepwidesearch-benchmarking-depth-width-agentic-information
    type: supports
    strength: strong
    detail: "On the 220-question DeepWideSearch benchmark, every evaluated frontier LLM and agent framework (GPT-5, Claude Sonnet 4, Gemini 2.5 Pro, DeepSeek-R1, KIMI-K2, Qwen3, plus WebSailor / Smolagents / OWL on top of these backbones) achieves an average Success Rate of 2.39%, with no system exceeding ~1% Avg@4. Error analysis identifies four failure modes — lack of reflection, overreliance on internal knowledge, insufficient retrieval, and context overflow (24.96% of cases) — and notes that agent scaffolds often underperform raw LLMs on width metrics."
conditions: |
  Holds for tasks defined as discovering many target entities and verifying multi-hop attributes for each, evaluated with whole-table exact match plus Row/Item/Column F1. Restricted to agents using the standard Google Search + webpage-visit toolkit with LLM summarization. May not hold under different toolings (browser-use agents, persistent external scratchpads), substantially different question distributions, or reference-free evaluation. Marked weakly_supported because the evidence comes from a single benchmark whose construction methods (Deep2Wide, Wide2Deep) inherit biases from their parent datasets — Wide2Deep instances in particular are notably easier (~88% Entity Accuracy vs ~33% for Deep2Wide).
date_proposed: 2026-05-02
date_updated: 2026-05-02
---

## Statement

Across frontier closed- and open-source LLMs and the leading open-source agent frameworks (WebSailor, Smolagents, OWL), no current system can reliably perform combined deep multi-hop reasoning *and* wide-scale information collection: average whole-table Success Rate sits near 2%, and width metrics are not improved (often degraded) by adding agent scaffolding on top of the LLM backbone.

## Evidence summary

Single supporting paper at the moment, but the evidence is unusually broad within that paper:

- 18+ system configurations evaluated under identical tool stacks and 4 independent runs per question.
- Headline Avg@4 Success Rate: 2.39% across systems; the strongest single configuration is below 1% Avg@4.
- Agents help on depth (e.g. +15.91 Core Entity Accuracy points on average) but consistently fail to improve width (Row-F1, Item-F1) and often regress.
- Quantitative error breakdown: context overflow alone accounts for 24.96% of cases; the other three failure modes (no reflection, internal-knowledge overreliance, insufficient retrieval) are documented with case studies but not isolated quantitatively.

## Conditions and scope

- Applies to deep-and-wide tasks specifically, not deep-only or wide-only.
- Toolset assumed: Google Search API + a webpage-visit tool with LLM summarization. Different toolings may shift results.
- Wide2Deep instances are easier than Deep2Wide; aggregate metrics may understate true difficulty on the deep-and-wide quadrant.
- Single-benchmark evidence — independent replications on different deep-and-wide datasets are absent so far.

## Counter-evidence

None known. Strongest near-counter would be (i) an agent that achieves >>2% Success Rate on DeepWideSearch, or (ii) a different benchmark in the same quadrant where agents close most of the gap to humans. Neither is yet documented.

## Linked ideas

To be filled in by `/ideate` once candidate research directions exist (likely candidates: reflection controllers, internal-vs-external arbitration, structured-context working memory, browser-use agents on deep-and-wide tasks).

## Open questions

- Does the failure persist with browser-use or computer-use agents that maintain persistent external state?
- How much of the gap is closeable purely by better context management, holding the controller fixed?
- Are these failure modes correlated (e.g. context overflow induces premature abort that looks like lack of reflection), or are they independent?
- Is the 2.39% bar an artifact of whole-table exact match, or does it survive under softer set-of-cells metrics?
