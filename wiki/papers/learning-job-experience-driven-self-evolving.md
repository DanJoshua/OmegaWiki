---
title: "Learning on the Job: An Experience-Driven Self-Evolving Agent for Long-Horizon Tasks"
slug: learning-job-experience-driven-self-evolving
arxiv: "2510.08002"
venue: "arXiv"
year: 2025
tags:
  - agents
  - self-evolution
  - memory
  - long-horizon
  - continual-learning
  - tool-use
importance: 3
date_added: 2026-05-02
source_type: tex
s2_id: "f6352c670c573240d310df585d0cf3770054740c"
keywords:
  - hierarchical memory
  - experience-driven agent
  - test-time learning
  - long-horizon productivity tasks
  - reflection
  - procedural memory
domain: "NLP"
code_url: "https://github.com/KnowledgeXLab/MUSE"
cited_by: []
---

## Problem

Existing LLM-based agents are *test-time static*: their capabilities are fixed once pretraining ends, so each task attempt behaves like an "amnesiac executor" that cannot consolidate prior successes or failures. Standard agent benchmarks (OSWorld, WebArena) further hide this gap by evaluating short-horizon (~20 step), single-application tasks. Real-world *productivity tasks* span 100+ steps across multiple applications (chat, code editor, browser, project management), exposing a core deficit: agents cannot learn on the job, cannot accumulate transferable knowledge, and cannot reliably replicate even tasks they previously solved.

## Key idea

Introduce **MUSE** (Memory-Utilizing and Self-Evolving), an LLM-agent framework whose core is a **hierarchical Memory Module** that stores experience at three abstraction levels — Strategic Memory (dilemma to resolution patterns), Procedural Memory (SOP-style sub-task workflows indexed by application), and Tool Memory (per-tool static descriptions plus dynamic post-action instructions). A "Plan-Execute-Reflect-Memorize" loop drives a Planning-Execution agent and an independent Reflect agent: after every sub-task, successful trajectories are distilled into procedural SOPs; after every full task, strategic and tool memories are consolidated. Memory is stored in natural language, making the accumulated experience LLM-agnostic and transferable across base models.

## Method

- **Architecture.** Three components: Memory Module $\mathcal{M} = \{\mathcal{M}_{strat}, \mathcal{M}_{proc}, \mathcal{M}_{tool}\}$, Planning-Execution (PE) agent, Reflect agent. Both agents share a **minimal toolset** $\mathcal{A}_{tool}$ (browser, code interpreter, shell, vision extractor, memory retriever) — no per-application APIs.
- **PE agent.** Decomposes task $\tau$ into an ordered sub-task queue $Q = [st_1, ..., st_M]$, each $st_i = (\text{desc}_i, \text{goal}_i)$. Executes each via a memory-enhanced ReAct $(\theta_t, a_t, o_t)$ loop with action cap $N=20$. Replans dynamically after each sub-task assessment.
- **Reflect agent.** Independent third-party supervisor with the same toolset. Evaluates each sub-task via an ordered checklist (truthfulness verification, deliverable verification, data fidelity) using *trajectory referencing* and *active environment verification*. Emits success/failure flag $f$ plus check report. On success, distills SOP $p_{new}$ into $\mathcal{M}_{proc}$; on failure, returns failure cause analysis $R_{fail}$.
- **Strategic Memory.** Stores $\langle \text{Dilemma}, \text{Strategy} \rangle$ pairs; loaded entirely into system prompt; updated/merged after each task to stay concise.
- **Procedural Memory.** Hierarchical SOP store indexed first by application then by sub-task. Lightweight index loaded at startup; full SOP content $content_p$ retrieved on demand via a dedicated tool $a_{mem}$. Two-stage refinement: dynamic per-sub-task add, post-task global dedup/generalization.
- **Tool Memory.** Pair of static descriptions $D_{static}$ (in system prompt) and dynamic instructions $I_{dynamic}$ (returned with observation $o_t$ to guide $a_{t+1}$); updated by Reflect agent after each task.
- **Retry policy.** On hitting action limit $N$, Reflect agent grants one retry; during retry, PE agent is *not required* to use $\mathcal{M}_{proc}$, encouraging exploration over exploitation when existing knowledge is wrong.

## Results

- **TAC full benchmark (175 tasks).** With Gemini-2.5 Flash: $S_{partial} = 51.78\%$, $S_{ckpt} = 59.92\%$, PCR $= 41.14\%$. First framework to exceed 50% on TAC; ~20% relative gain over previous SOTA (OpenHands-Versa with Claude-4 Sonnet at 43.19%). Memory was acquired from only ~10% of available tasks.
- **Continuous learning ($\mathcal{T}_{cl}$, 18 tasks, 5 runs averaged).** Both $S_{ckpt}$ and $S_{partial}$ grow monotonically across three iterations; final round beats memory-less baseline by >10%.
- **Generalization ($\mathcal{T}_{hard}$, 12 tasks).** With pre-accumulated memory: $S_{partial} = 33.41\%$ vs. 23.65% without memory (zero-shot transfer to unseen hard tasks). OpenHands+Gemini-2.5 Pro reaches only 3.00%; OpenHands-Versa+Claude-4 Sonnet only 2.00%.
- **Ablation — Reflect agent.** Removing it drops $S_{partial}$ on $\mathcal{T}_{cl}$ from 55.85% to 43.21% (no memory in either condition).
- **Ablation — base model.** Swapping Gemini-2.5 Flash for DeepSeek-V3: w/o memory 28.01% $S_{partial}$, w/ pre-accumulated memory 36.75%. Memory transfers across LLMs, confirming the LLM-agnostic claim.

## Limitations

- Memory architecture is not a panacea: weaker on tasks needing high-level planning or multi-hop search.
- TAC benchmark itself has noisy/ambiguous task descriptions and rigid evaluation scripts that can underestimate plausible agent strategies (authors flag two case studies in appendix).
- Authors deliberately reject fine-tuning (compute) and RL (reward design difficulty); this restricts the design space and means the memory-only approach inherits all base-model capability ceilings.
- No quantitative analysis of memory storage cost or context-window usage growth as procedural memory accumulates.
- Continuous-learning evaluation uses only 18 tasks across 3 iterations; long-horizon stability of memory refinement is not tested.

## Open questions

- How does procedural memory scale (retrieval quality, context cost) under thousands of accumulated SOPs?
- Can the agent learn from *failed* trajectories as effectively as from successful ones, beyond replanning hints?
- How robust is the cross-LLM memory transfer when target and source models differ in tool-use conventions or tokenizer assumptions?
- Can human-in-the-loop edits to the memory module accelerate evolution without destabilizing learned behaviors?

## My take

This is a clean, well-engineered instantiation of "memory as the substrate of agent self-evolution." The hierarchical decomposition (strategic / procedural / tool) is more disciplined than most prior memory-augmented agents (Reflexion, ExpeL, Mem0, AWM, Memp), and the SOP index/content split is a practical answer to context-window growth. The Reflect-agent ablation makes the case that high-quality reflection signal — not just memory storage — is what unlocks the gains. The headline TAC number (51.78%, +20% relative) is real but should be read alongside the TAC evaluation-script caveats the authors themselves raise.

## Related

- [[hierarchical-experience-memory]]
- [[claim-experience-memory-enables-self-evolution]]
- [[self-evolving-agents]]
