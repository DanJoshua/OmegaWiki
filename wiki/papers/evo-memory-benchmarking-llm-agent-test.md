---
title: "Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory"
slug: evo-memory-benchmarking-llm-agent-test
arxiv: "2511.20857"
venue: arXiv
year: 2025
tags:
  - llm-agents
  - memory
  - test-time-learning
  - benchmark
  - self-evolution
importance: 4
date_added: 2026-05-02
source_type: tex
s2_id: "87dc9cf7adf0a6446c07231c6ff2ae71d48235d3"
keywords:
  - self-evolving memory
  - test-time evolution
  - experience reuse
  - action-think-memory refine
  - streaming task streams
domain: NLP
code_url: ""
cited_by: []
---

## Problem

Existing LLM memory systems treat memory as **static recall** — retrieving prior dialogue facts to compensate for finite context — rather than as a substrate for **experience reuse** that abstracts reasoning strategies for future tasks. Existing benchmarks (StreamBench, LifelongBench, LongMemEval) measure factual retention or long-horizon recall, but none unify how an agent should *retrieve, integrate, and update* memory continuously during deployment across both multi-turn goal-oriented environments and single-turn reasoning. The community lacks a standardized streaming benchmark and protocol that isolates the effect of memory design from raw LLM capability.

## Key idea

Reframe memory evaluation around **test-time evolution**: an agent processes a stream of tasks $(x_1, \dots, x_T)$ under a unified `search -> synthesis -> evolve` loop, where memory $M_t$ is a first-class state variable that is updated after every interaction. Convert traditionally static datasets (MMLU-Pro, GPQA, AIME, ToolBench, AgentBoard suites) into sequential task streams, hold the LLM backbone and prompting templates fixed, and force every memory module — RAG, hierarchical, workflow, dynamic-cheatsheet — through the same retrieval/synthesis/update interface so that observed differences reflect memory design alone. On top of the benchmark, introduce **ReMem**, an *action-think-memory refine* policy that augments the ReAct action space with an explicit `Refine` operator over memory itself, so reflection becomes part of the decision loop rather than a passive post-processing pass.

## Method

The paper formalizes any memory-augmented agent as a tuple $(F, U, R, C)$: base LLM $F$, update pipeline $U$, retriever $R$, and context-construction $C$. At step $t$ the agent computes $R_t = R(M_t, x_t)$, then $\tilde{C}_t = C(x_t, R_t)$, predicts $\hat{y}_t = F(\tilde{C}_t)$, and finally evolves memory via $M_{t+1} = U(M_t, m_t)$ where $m_t = h(x_t, \hat{y}_t, f_t)$ encodes the step's experience and feedback signal $f_t$.

Two reference algorithms instantiate the framework:

- **ExpRAG** — task-level retrieval-augmented baseline. Stores $m_i = S(x_i, \hat{y}_i, f_i)$ as structured experience text, retrieves top-$k$ experiences via similarity score $\phi$, conditions in-context, and appends the new experience: $M_{t+1} = M_t \cup \{(x_t, \hat{y}_t, f_t)\}$. One-shot experience reuse without iterative reasoning.
- **ReMem** — at every step, the agent picks $a_t^n \in \{\text{Think}, \text{Act}, \text{Refine}\}$. *Think* produces internal reasoning; *Act* executes in the environment or emits a final answer; *Refine* performs meta-reasoning over $M_t$ — exploiting useful experiences, pruning noise, reorganizing entries. The step terminates when *Act* fires; multiple Think/Refine rounds may occur before that. The state is $s_t^n = (x_t, M_t, o_t^{1:n-1})$ and the formulation is an MDP over the extended action space.

Ten representative memory modules are unified under this protocol — ReAct, A-Mem, SelfRAG, MemOS, Mem0, LangMem, Dynamic Cheatsheet (Cumulative + Synthesis variants), Agent Workflow Memory — plus the proposed ExpRecent / ExpRAG / ReMem family. Backbones: Gemini-2.5 (Flash, Flash-Lite, Pro) and Claude (3.5-Haiku, 3.7-Sonnet). Evaluation along four axes: answer accuracy (single-turn), success/progress rate (multi-turn), step efficiency, and sequence robustness under task-order perturbations.

## Results

- **Single-turn (AIME-24/25, GPQA, MMLU-Pro, ToolBench).** Evolving-memory methods give consistent but moderate gains; ReMem reaches 0.65 average exact match and 0.85/0.71 API accuracy on Gemini-2.5 Flash. ExpRAG already outperforms many more complex memory designs.
- **Multi-turn (AlfWorld, BabyAI, Jericho, PDDL, ScienceWorld).** Gains are much larger. ReMem reaches 0.92/0.96 progress on BabyAI and 0.95/0.62 on ScienceWorld; ExpRAG hits 0.66 success on AlfWorld and 0.56 on ScienceWorld, materially above all retrieval-only baselines.
- **Step efficiency.** ReMem cuts AlfWorld average steps from 22.6 to 11.5; ExpRAG / ExpRecent are competitive. Continual refinement reduces the *length* of reasoning, not just its accuracy.
- **Task-similarity correlation (RQ2).** ReMem's gain over the history baseline correlates with within-dataset task similarity: Pearson $r = 0.717$ on Gemini-2.5 Flash, $r = 0.563$ on Claude 3.7 Sonnet. PDDL and AlfWorld (high cluster coherence) yield large gains; AIME-25 and GPQA (low coherence) yield small gains.
- **Sequence difficulty (RQ3).** Baselines degrade noticeably from Easy->Hard. ReMem stays stable in both directions, peaking at 0.94/0.97 success/progress in Hard->Easy, indicating that continual reflection retains transferable knowledge under distribution shift.
- **Failure-aware feedback (RQ4).** When successful and failed traces both enter memory, baselines drop because of accumulation noise; ReMem stays robust because Refine actively prunes failure traces.
- **Cumulative time-step curves (RQ5).** ReMem's cumulative success rate climbs faster and stabilizes higher than the History baseline on AlfWorld, BabyAI, PDDL, and ScienceWorld, evidencing genuine continual adaptation rather than once-off retrieval gains.

Smaller backbones (Flash-Lite, Haiku) benefit disproportionately, suggesting test-time memory evolution is a practical capability lever for cheaper LLMs.

## Limitations

- **No backbone retraining.** ReMem's improvements come from prompting and memory orchestration; the underlying LLM is frozen, so gains plateau at the backbone's reasoning ceiling.
- **Embedding-coherence dependence.** Gains correlate with within-dataset cosine cluster tightness; on diverse low-similarity datasets (AIME-25, GPQA), evolving memory adds little because there is little reusable structure to transfer.
- **Excluded settings.** MemOS and LangMem are dropped from multi-turn embodied tasks for compatibility reasons, weakening the head-to-head story for those systems. Pure factual-recall systems (MemoryBank, MemoryGPT) are excluded by design.
- **Feedback-signal assumption.** $f_t$ is treated as a binary correctness signal supplied by the environment; in real deployments such feedback is often delayed, sparse, or unavailable.
- **Compute and memory budgets.** ReMem's Think+Refine rounds inflate per-step token usage; the paper does not deeply ablate the reasoning-budget vs. final-accuracy frontier.

## Open questions

- How should memory evolve when feedback $f_t$ is unavailable, delayed, or noisy — i.e., genuinely unsupervised lifelong deployment?
- Is the Think/Act/Refine action augmentation specific to ReAct-style agents, or can it be folded into other agentic scaffolds (planner-executor, MCTS-guided agents) without losing the refinement gains?
- What is the right formal complexity class of "experience reuse" — does it admit transfer guarantees beyond same-dataset cluster similarity?
- How should memory updates trade off against context window growth? ReMem's Refine is the only baseline that prunes; can pruning policies themselves be learned?
- Can self-evolving memory be combined with parameter-level test-time learning (LoRA-style adapters, in-context fine-tuning) without catastrophic interference?

## My take

The paper is most useful as a **standardized harness**: it pulls a fragmented landscape of memory systems through one `search-synthesis-evolve` interface and a fixed task-stream protocol, which is exactly what the field has been missing. ReMem itself is a clean, unsurprising augmentation of ReAct — adding a *Refine-memory* operator alongside Think/Act is the obvious move once you accept memory is a first-class state — but the empirical message that *task-level memory utilization beats more elaborate retrieval architectures* (ExpRAG approximately equals ReMem and substantially beats workflow-memory baselines) is the paper's real load-bearing claim and it generalizes across both Gemini and Claude backbones. The within-dataset task-similarity correlation analysis (Pearson 0.717 on Flash) is the kind of mechanism-revealing diagnostic the benchmarking literature usually omits and is the most cite-worthy figure here. The main caveat: gains depend on the existence of a reliable feedback signal $f_t$, so the deployment story for fully unsupervised lifelong agents is still open.

## Related

- [[self-evolving-memory]] (introduced concept)
- [[test-time-learning]] (uses concept)
- [[task-level-experience-reuse-beats-fine-grained-memory-architectures]] (supports)
- [[memory-evolution-gain-correlates-with-task-similarity]] (supports)
- Topic: [[self-evolving-agents]]
