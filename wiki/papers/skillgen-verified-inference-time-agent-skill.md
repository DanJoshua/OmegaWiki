---
title: "SkillGen: Verified Inference-Time Agent Skill Synthesis"
slug: skillgen-verified-inference-time-agent-skill
arxiv: "2605.10999"
venue: "arXiv"
year: 2026
tags:
  - agents
  - llm-agents
  - self-evolving-agents
  - skill-synthesis
  - skill-lifecycle
  - contrastive-learning
  - intervention-verification
  - multi-agent
importance: 3
date_added: 2026-05-13
source_type: tex
s2_id: ""
keywords:
  - skill synthesis
  - contrastive induction
  - trajectory analysis
  - intervention verification
  - net effect
  - repair vs regression
  - generation-verification-refinement loop
  - multi-agent framework
  - inference-time skills
domain: "NLP"
code_url: "https://github.com/yccm/SkillGen"
cited_by: []
---

## Problem

High-quality agent skills are still largely hand-written. Automated skill synthesis methods have two critical shortcomings: (1) they learn primarily from *successful* trajectories, missing the contrastive signal between success and failure — specifically, what a successful agent does that a failed attempt on the same task omits; (2) they do not empirically verify the net effect of a generated skill, ignoring "regressions" (cases where the skill breaks previously-correct behavior). As a result, prior skill-synthesis approaches may generate skills that repair some failures while introducing new ones.

## Key idea

SkillGen frames inference-time skill synthesis as an **interventional problem**: a skill is an intervention on a base agent, and its quality is measured by the causal net-effect Δ(s) = E[Y^s(x) − Y^0(x)] — the expected performance change over the same input distribution. A three-agent pipeline first extracts a **contrastive diagnostic summary** from both successful and failed trajectories (contrastive induction), then runs an **iterative generation–verification–refinement loop** that explicitly tracks repairs (0→1 transitions) and regressions (1→0 transitions) on a held-out verification subset. Only skills that pass a **verification gate** (strictly positive net repair count) are deployed.

## Method

**Stage 1 — Baseline elicitation.** The base agent is run on an induction subset to collect successful (I⁺) and failed (I⁻) trajectories B = {(xᵢ, τ⁰ᵢ, y⁰ᵢ)}.

**Stage 2 — Contrastive behavioral induction.** An *induction agent* produces a diagnostic summary Z = (a₀, F, S, C):
- **a₀** (task summary): describes the task family.
- **F** (failure clusters): root-cause summaries for clusters of similar failures, including corrective rules.
- **S** (success clusters): reusable procedure summaries for clusters of successes.
- **C** (local contrastive observations): for each failed trajectory, the nearest successful trajectory (by embedding distance) is retrieved if it shares the same task type; the agent writes a contrastive observation identifying the behavior present in the success but absent in the failure.

**Stage 3 — Generation–Verification–Refinement loop (K rounds).**
- *Generation agent* converts Z into a structured skill s = (u, a, P, R) with a three-part prompt u = (u_ctx, u_succ, u_fail).
- *Verification agent* rolls out the base agent with and without the skill on identical verification instances, computing repair count n₀₁ and regression count n₁₀; net gain G_m = n₀₁ − n₁₀.
- Structured feedback Φ = (keep, remove, add, emphasize) is passed back for refinement.
- Best-of-K selection returns the skill with the largest G_m; the verification gate requires G_m ≥ γ_m = max{g_abs, ⌈g_rel · m⌉, 1}.

**Deployment.** Active skills are injected into a dedicated system-prompt slot; reference documents use on-demand loading via skill_load_reference; scripts expose only declared top-level skill_ functions.

## Results

- +3.27 to +10.08 pp average accuracy improvement across 8 base models (4 open-weight: Gemma-4-26B, Llama-3.1-8B, Mistral-Nemo, Qwen-2.5-7B; 4 proprietary: Claude-Haiku-4.5, GPT-5.4-Nano, GPT-5.4-Mini, Grok-4-Fast).
- 50 of 80 held-out benchmark–split–model entries improve; only 5 regress.
- Outperforms four baselines (Trace2Skill, SkillX, EvoSkill, CoEvoSkills) on all benchmark–model pairs evaluated.
- Ablations show all components (contrastive induction, refinement, verification gate, failure lessons) contribute.
- Cross-model transfer: 70% of off-diagonal transfers (120 total) are non-negative; 42% exceed +5 pp.

## Limitations

- Skill synthesis requires running a multi-agent pipeline on both induction and verification subsets, which introduces nontrivial compute overhead at skill-construction time.
- The framework synthesizes a **single** skill per task; composing multiple skills or handling multi-skill libraries is left as future work.
- Transfer success depends on which model generates the skill — there is no single best skill-generating model across benchmarks.
- Verification gate threshold parameters (g_abs, g_rel) require setting per-task.

## Open questions

- Can contrastive induction be applied incrementally as new trajectories arrive (online setting)?
- How does SkillGen interact with skill libraries containing many existing skills (retrieval and composition)?
- Can the verification gate be extended to multi-skill portfolios to maximize net gain across a skill library?

## My take

SkillGen's interventional framing is a principled step beyond "summarize successful trajectories" approaches. Tracking regressions explicitly during verification is the key novelty — prior methods had no mechanism to prevent a new skill from breaking cases the agent already solved. The contrastive local pairing (finding the nearest successful neighbor for each failure) is a clean way to surface actionable patterns without needing a large success/failure population. The empirical breadth (8 models, 7+ benchmarks) is strong for a skill synthesis paper.

## Related

- [[skillos-learning-skill-curation-self-evolving]] — RL-trained skill curator that closes the loop between curation decisions and executor performance; SkillGen addresses a different stage (skill generation quality/verification vs. curation policy).
- [[skill-r1-agent-skill-evolution-reinforcement]] — RL-based skill *revision* for NL-policy skills; SkillGen synthesizes new skills from scratch via contrastive induction rather than refining existing ones.
- [[sok-agentic-skills-beyond-tool-use]] — surveys the skill lifecycle pattern taxonomy; SkillGen provides an empirical implementation of the distillation → evaluation stages.
- [[evotool-self-evolving-tool-use-policy]] — trajectory-grounded blame attribution for modular tool-use; SkillGen operates at a higher abstraction (full skill vs. module-level blame).
- [[evolver-self-evolving-llm-agents-through]] — experience-driven agent self-evolution; SkillGen contributes a verified skill synthesis pathway for the distillation stage.
- [[skill-lifecycle]] — SkillGen advances the distillation, evaluation/update, and (via verification gate) governance stages of the skill lifecycle.
- [[contrastive-induction-skill-synthesis]] — concept introduced by this paper.
- [[skill-intervention-verification]] — concept introduced by this paper.
