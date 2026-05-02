---
title: "Hierarchical experience memory enables LLM agents to self-evolve at test time on long-horizon tasks"
slug: claim-experience-memory-enables-self-evolution
status: weakly_supported
confidence: 0.55
tags:
  - agents
  - memory
  - self-evolution
  - continual-learning
  - long-horizon
domain: "NLP"
source_papers:
  - learning-job-experience-driven-self-evolving
evidence:
  - source: learning-job-experience-driven-self-evolving
    type: supports
    strength: moderate
    detail: "MUSE on TAC achieves S_partial=51.78% vs prior SOTA 43.19% (+20% relative) using only Gemini-2.5 Flash; continuous-learning experiment on 18-task subset shows monotonic improvement across 3 iterations, beating the memory-less baseline by >10% in the final round; cross-LLM transfer to DeepSeek-V3 still yields 36.75% with memory vs 28.01% without."
conditions: "Demonstrated only on the TAC productivity benchmark (175 tasks, 6 roles), with Gemini-2.5 Flash and DeepSeek-V3 base models, and with the MUSE three-layer (strategic/procedural/tool) hierarchy. Continuous-learning evidence is over 18 tasks and 3 iterations; longer-horizon stability is untested. The claim assumes a reflection process of comparable quality to MUSE's Reflect agent — ablation shows removing the Reflect agent drops S_partial from 55.85% to 43.21%, indicating reflection quality is an essential precondition."
date_proposed: 2026-05-02
date_updated: 2026-05-02
---

## Statement

For LLM-based agents tackling long-horizon, multi-application tasks, equipping the agent with a hierarchical natural-language memory module (covering strategic, procedural, and tool levels) and a reflection process that distills successful trajectories into that memory is sufficient to produce monotonic, autonomous test-time improvement, generalization to unseen tasks, and cross-LLM portability of accumulated knowledge — without modifying base-model parameters.

## Evidence summary

Single-paper (MUSE) evidence covers three claim facets:

1. **Test-time improvement.** Continuous-learning experiment on $\mathcal{T}_{cl}$ (18 tasks) shows $S_{ckpt}$ and $S_{partial}$ growing monotonically across 3 iterations, with the final round exceeding the memory-less baseline by >10%.
2. **Cross-task generalization.** On $\mathcal{T}_{hard}$ (12 unseen hard tasks), pre-accumulated memory raises $S_{partial}$ from 23.65% to 33.41% — a zero-shot transfer.
3. **Cross-LLM portability.** Replacing Gemini-2.5 Flash with DeepSeek-V3 still benefits from memory (28.01% → 36.75%), supporting the LLM-agnostic claim.

Reflect-agent ablation (55.85% → 43.21% on $\mathcal{T}_{cl}$ without memory in either condition) is an important *precondition* signal: the memory mechanism alone is insufficient without a reliable reflection process that produces high-signal SOPs.

## Conditions and scope

- Benchmark: TAC (TheAgentCompany) productivity tasks; behavior on other long-horizon agent benchmarks (OSWorld, WebArena, GAIA) is not yet measured.
- Tested base models: Gemini-2.5 Flash, DeepSeek-V3. Untested: smaller open models (<10B), models without strong tool-use training.
- Memory was acquired from ~10% of available tasks; behavior under saturation (thousands of SOPs) is unknown.
- The claim presumes the reflection process meets a quality bar; with weak reflection, memory accumulation may store noise.

## Counter-evidence

- Authors themselves note MUSE struggles on tasks requiring high-level planning or multi-hop search, suggesting memory-based self-evolution is not sufficient for all long-horizon difficulty modes.
- TAC evaluation scripts are rigid and may overstate the contribution of any memory framework that aligns with the benchmark's specific solution patterns. The +20% relative improvement should be interpreted cautiously until reproduced on independent benchmarks.

## Linked ideas

(none yet)

## Open questions

- Does the monotonic-improvement property hold beyond 3 iterations, or does memory dedup eventually erase useful specificity?
- Is the cross-LLM transfer claim robust when the source and target models differ substantially in tool-use training (e.g., a Gemini-trained memory used by a Llama-class model)?
- What is the minimum reflection-process quality below which memory accumulation hurts rather than helps?
