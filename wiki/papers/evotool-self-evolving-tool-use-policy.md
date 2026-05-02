---
title: "EvoTool: Self-Evolving Tool-Use Policy Optimization in LLM Agents via Blame-Aware Mutation and Diversity-Aware Selection"
slug: evotool-self-evolving-tool-use-policy
arxiv: "2603.04900"
venue: "arXiv"
year: 2026
tags:
  - llm-agents
  - tool-use
  - self-evolution
  - prompt-optimization
  - evolutionary-search
importance: 4
date_added: 2026-05-02
source_type: tex
s2_id: ""
keywords:
  - tool-use policy
  - blame attribution
  - targeted mutation
  - diversity-aware selection
  - gradient-free optimization
domain: "NLP"
code_url: ""
cited_by: []
---

## Problem

LLM agents that solve complex tasks must coordinate interdependent competencies — goal decomposition, tool selection, schema-valid argument construction, and grounded synthesis of tool outputs — over long-horizon trajectories. Supervision is typically available only at the end of an interaction, collapsing every error source (planning, selection, calling, synthesis) into a single terminal signal. This creates a severe credit-assignment problem: it is impossible to know which module caused failure, so policy improvement is either monolithic (global prompt search that entangles heterogeneous behaviors and induces regressions) or single-aspect (refining one component in isolation while ignoring cross-module error propagation). Neither paradigm simultaneously achieves targeted error correction and multi-module coordination.

## Key idea

Decompose the agent's tool-use policy into four explicit modules — Planner, Selector, Caller, Synthesizer — parameterized by evolvable natural-language specifications under frozen LLM weights. Run a gradient-free evolutionary loop driven by three mechanisms: (1) Trajectory-Grounded Blame Attribution converts trace-level diagnostics (schema violations, tool-choice outcomes, grounding signals) into module-wise blame scores via a Blamer LLM, identifying the single module most responsible for failure; (2) Feedback-Guided Targeted Mutation prompts a Mutator LLM to produce trace-grounded natural-language critique that edits only the blamed module's specification, freezing the rest; (3) Diversity-Aware Population Selection retains candidates based on instance-level wins on a held-out set rather than global average, preserving complementary specialists and preventing premature convergence to a narrow strategy.

## Method

The overall policy is a fixed modular composition $\Pi = \pi_{\text{syn}} \circ \pi_{\text{call}} \circ \pi_{\text{sel}} \circ \pi_{\text{plan}}$, with module specifications $\Theta = \{\theta_{\text{plan}}, \theta_{\text{sel}}, \theta_{\text{call}}, \theta_{\text{syn}}\}$ as the only learnable parameters. EvoTool maintains a population $\mathcal{P}$ of candidate $\Theta$ values and runs $G$ generations:

- **Phase 1 — Trajectory collection.** Sample a parent $\Theta_p$ proportional to its winner frequency $w(\Theta)$, run the policy on a mini-batch from $S_{\text{train}}$, log episode records $e = (x, \tau, \hat{y}, R)$.
- **Phase 2 — Blame attribution.** Extract structured diagnostic events from $\tau$, pass $(e, \text{diagnostics})$ to a Blamer LLM that outputs $\{b_\pi(e) \in [0,1]\}$. Pick $\pi^* = \arg\max_\pi b_\pi(e)$.
- **Phase 3 — Targeted mutation.** A Mutator LLM produces feedback $F(e, \pi^*)$ explaining the error from $\pi^*$'s perspective and proposes a localized edit. Apply the edit to produce a child $\Theta'$ that differs in exactly one component. Add to $\mathcal{P}$ only if the child outperforms its parent on the mini-batch.
- **Phase 4 — Diversity-aware selection.** On a held-out $S_{\text{sel}}$, evaluate every candidate; for each instance, the candidate with the highest $R$ is the winner. Drop candidates that never win any instance; sample parents in proportion to winner frequency $w(\Theta) = \frac{1}{|S_{\text{sel}}|} \sum_x \mathbb{I}[\Theta = W(x)]$.

## Results

Evaluated on four tool-use benchmarks (ToolBench G1/G2/G3, RestBench TMDB/Spotify, $\tau$-Bench Retail/Airline, BFCL Single/Multi-turn) using GPT-4.1 and Qwen3-8B as backbones. EvoTool achieves overall average 70.6 on GPT-4.1 (vs. EvoPrompt 63.8, DRAFT 64.9, EasyTool 64.4 — beating the strongest baseline by ~6 points) and 57.0 on Qwen3-8B (vs. DRAFT 51.8, EvoPrompt 51.4 — beating the strongest baseline by 5.2 points). Gains are largest on long-horizon settings: $\tau$-Bench overall 52.0 vs. AdaPlanner 50.5 and DRAFT 38.8; BFCL multi-turn 42.3 (best). Ablations show: (a) random module targeting is destructive (-9 vs. static); single-module variants generalize poorly; (b) trajectory evidence + natural-language feedback are complementary, dropping feedback hurts more than dropping the trajectory (-9.4 vs. -4.4); (c) diversity-aware selection beats greedy and top-k (57.0 vs. 52.0 / 52.7 avg). Efficiency: EvoTool sits on the Pareto frontier of accuracy vs. log token cost on every benchmark. Transferability: a Qwen3-8B-evolved policy transfers to GPT-4.1 (+4.7 over baseline); a GPT-4.1-evolved policy transfers to Qwen3-8B (+12.7); cross-dataset transfer between ToolBench and RestBench also holds.

## Limitations

The evolutionary loop still requires iterative inference (Blamer, Mutator, candidate evaluation), introducing latency unsuitable for strictly real-time settings even though token cost is favorable vs. monolithic baselines. Evaluation is restricted to textual / API-based environments — multi-modal tools and embodied agents are not tested. Blame attribution depends on a single Blamer LLM and is not validated against human agreement on module attribution (the authors mention this as future work). The single-module-attribution choice ($\arg\max$) commits to one cause per failure even when multiple modules genuinely co-contribute; soft attribution is unexplored. Code is not yet released.

## Open questions

- How accurate is Blamer-LLM module attribution against human annotation, and how does noise in blame scores propagate into population dynamics?
- Does the method scale beyond four-module decomposition (e.g., adding memory, verifier, or critic modules)?
- Can blame and mutation be jointly trained rather than supplied as zero-shot prompts to a separate LLM?
- How does the diversity-aware selection rule degrade when $|S_{\text{sel}}|$ is small (few-shot deployment)?

## My take

The core methodological commitment — that *intermediate trajectory diagnostics convert delayed reward into a per-module credit signal* — is the right move for tool-use settings, and the paper executes it cleanly with a separation between blame (where to edit), mutation (what to edit), and selection (which variants to keep). The most novel contribution is treating module-level blame as the primary lever, rather than a side feature of a global optimizer. The diversity-aware population selection is a sensible defense against the well-known greedy-collapse failure of evolutionary prompt search, but its mechanism is fairly standard (instance-wins, sample-by-frequency). The reported gains are large enough to be interesting, but they hinge on a Blamer LLM whose accuracy is not directly measured — this is the most fragile assumption in the pipeline.

## Related

- [[trajectory-grounded-blame-attribution]] — introduced concept (this paper)
- [[modular-tool-use-policy]] — introduced concept (this paper)
- [[diversity-aware-population-selection]] — introduced concept (this paper)
- [[module-level-blame-attribution-enables-stable]] — supporting claim
- [[diversity-aware-population-selection-prevents-premature]] — supporting claim
- [[soyeon-caren-han]] — corresponding author
- [[shuo-yang]] — first author
