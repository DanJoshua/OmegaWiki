---
title: "FLEX: Continuous Agent Evolution via Forward Learning from Experience"
slug: flex-continuous-agent-evolution-forward-learning
arxiv: "2511.06449"
venue: "arXiv"
year: 2025
tags:
  - self-evolving-agents
  - llm-agents
  - gradient-free-learning
  - experience-replay
  - continual-learning
  - reasoning
importance: 4
date_added: 2026-05-02
source_type: tex
s2_id: "142e787c3499fe054c46346be00f3f40b961aac5"
keywords:
  - experience library
  - forward learning
  - agent evolution
  - knowledge inheritance
  - experiential scaling
domain: "NLP"
code_url: "https://flex-gensi-thuair.github.io"
cited_by: []
---

## Problem

LLM-driven autonomous agents excel at end-to-end reasoning across coding, scientific discovery, and deep research, but their parameters are frozen after training. They cannot accumulate lessons from on-the-fly trial and error, which causes brittle performance on hard or unseen tasks. Gradient-based remedies are ill-suited for continuous agent evolution because (i) backpropagation is computationally prohibitive at LLM scale, (ii) parameter updates suffer catastrophic forgetting and so cannot effectively integrate experience over time, and (iii) most state-of-the-art LLMs are closed-source, making direct parameter optimization infeasible. Existing self-evolving agent paradigms that evolve prompts, workflows, or tools are task-specific, capacity-limited (cannot scale with accumulated experience), and model-specific (cannot transfer across agents).

## Key idea

Replace parameter optimization with **forward learning from experience**: keep the LLM frozen and instead optimize an external, persistent **experience library** $\mathcal{E}$ that stores semantically-distilled lessons from past trajectories. Learning becomes a forward probabilistic update governed by an updater agent $\mu$, with the analog "gradient" $\nabla_{\mathcal{E}} \mathcal{J}(\mathcal{E}_i) \triangleq \mu(\cdot \mid \mathcal{E}_i, \{\tau_i \mid X_i, \pi\}) - \mathcal{E}_i$. Information-theoretically, the objective reduces to minimizing $\mathcal{H}(Y \mid X, \varepsilon)$ — retrieved experiences provide additional information about the target output, raising prediction confidence. Because experiences are stored as natural-language strategies, the library is interpretable, scalable, and inheritable across agents.

## Method

FLEX is formalized as a hierarchical Meta-MDP:

- **Base-level MDP** (per-sample exploration): an actor-critic loop. The actor $\pi$ samples multiple trajectories per query (parallel scaling via rejection sampling); the critic supplies semantic feedback on incorrect trajectories (sequential scaling via Reflexion/TextGrad-style refinement). When a trajectory is correct or the budget is exhausted, distilled experience $E^T$ is emitted.
- **Meta-level MDP** (cross-sample library evolution): the updater $\mu$ ingests $E^T$ and decides whether to discard (duplicate), merge (semantically similar), or insert. The library is hierarchically structured into three levels — high-level strategic principles, mid-level reasoning patterns, low-level factual knowledge — and partitioned into a *golden* zone (lessons from successes) and a *warning* zone (failure-mode diagnostics).
- **Retrieval at inference**: the experience library is exposed as a tool callable by the agent. Retrieval is contextualized (not pure semantic-similarity) and hierarchical (strategy then pattern then instance), with top-$k$ ($k{=}5$) per stage. Retrieval can be invoked dynamically mid-reasoning, not just before inference.

Training data is small: 49 historical AIME problems, 50 USPTO50k samples, ~1.47% of ProteinGym mutations per target.

## Results

Across four scientific benchmarks FLEX consistently outperforms vanilla LLM, ICL, and ReAct-Agent baselines:

- **AIME25**: Claude-Sonnet-4 40.0% to **63.3%** (+23.3); DeepSeek-V3.1-Terminus 56.7% to **66.6%** (+10.0).
- **GSM8k**: GPT-4 93.8% to **95.9%**; Llama-3.2-1B 74.3% to **80.9%**; consistent gains across GPT-3.5 and Llama-3.2-3B.
- **USPTO50k** (retrosynthesis): GPT-5 9.0% to **16.0%**; Gemini-2.5-Pro 9.0% to **18.0%**; Claude-Sonnet-4.5 20.0% to **30.0%**.
- **ProteinGym** (Spearman $\rho$): Claude-Sonnet-4 0.460 to **0.597**; GPT-OSS-120B 0.477 to **0.573**; DeepSeek-V3.1 0.479 to **0.568**.

Two emergent properties:

- **Scaling law of experience.** On GSM8k across 5 epochs, train accuracy follows a power-law in library size (81.2% at 1,001 entries; 94.2% at 1,904); test accuracy improves 81.3% to 83.3% with reduced variance. Library growth itself is logistic-like (rapid then selective), suggesting principled saturation.
- **Experience inheritance.** Libraries built by one model improve other models in plug-and-play fashion, in both directions: strong-to-weak distillation (Claude-4.5 library lifts Gemini-2.5-Pro on USPTO50k by +11) and weak-to-strong generalization (Claude-Sonnet-4 library lifts DeepSeek-V3.1 on AIME25 to par with its own).

## Limitations

- All "forward gradients" are language-mediated; reliability depends heavily on the critic's calibration. The paper does not stress-test miscalibrated critics or adversarial trajectories.
- Reported gains rest on small training sets and small test slices (100 instances on USPTO50k, AIME25 has only 30 problems); statistical significance is not analyzed.
- The hierarchical / golden-warning library schema is hand-designed and benchmark-specific (hierarchical for AIME25/USPTO50k, non-hierarchical for GSM8k/ProteinGym), which weakens the claim of a universal paradigm.
- No comparison against parameter-efficient fine-tuning baselines (LoRA-style adapters), so cost-equivalence claims are indirect.
- Inheritance experiments are pairwise; no analysis of mixing libraries or of negative transfer / experience contamination.
- Closed-source-LLM dependence is framed as a feature but also limits reproducibility of the strongest results.

## Open questions

- Can the experience library scale to open-ended deployment (millions of entries) without pathological retrieval drift?
- Does the scaling law hold across base-model sizes, or is it conditional on a sufficiently capable frozen LLM?
- What governs negative transfer when libraries from differently-aligned models are merged?
- How does FLEX compare against well-tuned RL fine-tuning (DAPO, GRPO) on equivalent compute?
- Is the "semantic gradient" formalism a useful theoretical bridge or a metaphor — i.e., are convergence guarantees attainable?

## My take

FLEX is a clean, well-engineered restatement of the experience-driven self-evolving-agent thesis with three contributions worth taking seriously: a unified Meta-MDP formalism, the empirically observed scaling law of experience, and clear evidence of cross-agent inheritance. The mathematical reframing of $\mu$ as a forward gradient is mostly notational, but it does crystallize the design space. The empirical wins are real but the test sets are small and the baseline ladder excludes both PEFT and recent experience-bank methods (ReasoningBank, AgentKB) at full strength, so the apples-to-apples picture is incomplete. Most exciting practically: the inheritance result hints at a future where one expensive run produces a portable cognitive substrate.

## Related

- [[experience-library]]
- [[forward-learning-from-experience]]
- [[experience-inheritance]]
- [[claim-experience-library-scaling-law]]
- [[claim-gradient-free-agents-can-match-parameter-tuning]]
- [[hao-zhou]]
- [[jiangtao-feng]]
- [[forge-self-evolving-agent-memory-no]] — complementary: both are gradient-free self-improvement protocols; FORGE uses population broadcast vs FLEX's experience-library scaling
