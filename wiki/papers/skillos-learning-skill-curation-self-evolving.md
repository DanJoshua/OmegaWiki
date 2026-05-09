---
title: "SkillOS: Learning Skill Curation for Self-Evolving Agents"
slug: skillos-learning-skill-curation-self-evolving
arxiv: "2605.06614"
venue: "arXiv"
year: 2026
tags:
  - agents
  - llm-agents
  - self-evolving-agents
  - skill-curation
  - reinforcement-learning
  - procedural-memory
  - skill-lifecycle
importance: 3
date_added: 2026-05-09
source_type: tex
s2_id: "2653e4c7fa3be13d3db4b7a6ff3032ac17f7f467"
keywords:
  - skill curation
  - experience-driven RL
  - skill curator
  - SkillRepo
  - grouped task streams
  - GRPO
  - procedural memory
domain: "NLP"
code_url: ""
cited_by: []
---

## Problem

LLM-based agents deployed in streaming settings are effectively amnesiac: each task begins from scratch, with no reuse of lessons from past interactions. Reusable skills distilled from experience provide a natural mechanism for self-evolution, but **high-quality skill curation is the bottleneck**. Existing approaches either rely on human-authored skills (which do not scale), hand-coded heuristic operations (which lack downstream feedback), or RL optimised over short task horizons (which misses complex long-term curation decisions like when to update vs. delete a skill). None of them close the loop between curation decisions and long-run executor performance.

## Key idea

SkillOS introduces a **modular two-component design**: a *frozen agent executor* that retrieves and applies skills from an external `SkillRepo`, paired with a *trainable skill curator* that updates the repository via file I/O operations (insert / update / delete). The curator is trained end-to-end with RL (GRPO) using a composite reward that attributes downstream executor performance to curation decisions. Two training innovations provide dense signals for this hard credit-assignment problem: (1) **grouped task streams** — semantically related tasks are grouped so that earlier curator updates are evaluated on later within-group tasks; (2) **composite reward** — task outcome + function-call validity + content quality (LLM judge) + compression ratio.

## Method

**Architecture.** Skills are stored as Markdown files (YAML frontmatter for description + NL instructions for executable content), managed via BM25 retrieval. The executor (frozen Qwen3-8B at train time) samples actions conditioned on retrieved skills. The curator (trainable, also Qwen3-8B base) observes the trajectory + self-judged outcome + related skills, then emits a sequence of structured tool calls to mutate `SkillRepo`.

**Training instance construction.** Tasks are annotated with latent attributes (topic, common pitfalls) by Gemini-2.5-Pro. Related instances are grouped; within each group, `SkillRepo` starts empty, curator updates propagate across tasks, and rewards are averaged over the group minus the first task (which has no prior skills).

**Composite reward:**
$$r = r^{\text{task}} + \lambda_f r^{\text{fc}} + \lambda_u r^{\text{cnt}} + \lambda_c r^{\text{comp}}$$
- Task outcome reward: average success on tasks 2…|G|
- Function call reward: fraction of valid, successfully executed operations
- Content quality: external judge score (Qwen3-32B)
- Compression: rewards keeping `SkillRepo` smaller than the curator's input context

**Optimisation.** GRPO with $N=8$ rollouts per group; clipped surrogate objective applied over all curation steps; KL term dropped to encourage exploration. Training on 16 H100s: ~3 days for ALFWorld, ~2.5 days for reasoning, ~5 days for WebShop.

## Results

Evaluated on ALFWorld (text household tasks), WebShop (web shopping agent), and single-turn reasoning (AIME24, AIME25, GPQA-Diamond):

- **ALFWorld**: SkillOS lifts average SR from 55.7 (ReasoningBank baseline, strongest) to 61.2 with Qwen3-8B executor (+9.8% relative); reduces interaction steps by 2.2–3.1 steps versus no-memory baseline.
- **Gemini-2.5-Pro executor**: SkillOS achieves 80.2 SR vs. 66.4 for no-memory, an absolute +13.8pp; the 8B RL-trained curator outperforms using Gemini-2.5-Pro directly as the curator, showing that executor-alignment matters more than raw model scale.
- **Cross-domain transfer**: curators trained on reasoning tasks transfer better to agentic tasks than vice versa, because reasoning skills encode more abstract decomposition and verification strategies.
- **Skill evolution**: the `SkillRepo` evolves from flat task notes into richly structured Markdown with higher-level meta-skills over training.

## Limitations

- Retrieval is BM25-only; richer semantic or graph-based retrieval could further improve skill selection.
- Skills are represented as flat Markdown files; hierarchical or compositional representations are unexplored.
- The executor is frozen during curator training, creating a potential curator-executor mismatch if the executor is updated later.
- Validated on ALFWorld, WebShop, and math reasoning; open-ended coding, long-horizon planning, and multi-agent settings remain untested.

## Open questions

- Can skill curators transfer across agent ecosystems without executor-specific fine-tuning?
- How should `SkillRepo` be pruned or reorganised when the executor itself is updated?
- Can agentic skill search (finding the right skill in a large repo) be co-optimised with curation?
- Do meta-skills that emerge in `SkillRepo` correspond to human-interpretable strategies?

## My take

SkillOS cleanly separates what the agent *does* (executor) from what it *learns from doing* (curator), making curation a first-class learnable module. The grouped task stream construction is the key methodological insight: it converts the notoriously hard credit-assignment problem of skill curation into a tractable RL problem by structuring training data to expose delayed feedback. The result that a small RL-trained 8B curator beats a frontier model curator used zero-shot is important: it shows that scale alone does not solve curation and that executor-alignment — knowing which skills actually help *this particular executor* — is the critical axis. The main open question is whether `SkillRepo`-style curation scales to longer horizons and more heterogeneous task distributions without the explicit grouping structure.

## Related

- [[skill-lifecycle]] — SkillOS instantiates stages 2–7 of the lifecycle (practice, distillation, storage, retrieval, execution, evaluation/update) with a learned curation policy
- [[agentic-skill]] — SkillRepo skills are instances of agentic skills in Markdown format
- [[experience-library]] — SkillRepo functions as an experience library; SkillOS adds an RL-trained curator to manage it
- [[experience-driven-self-evolution-lifecycle]] — SkillOS fits within this lifecycle but uses gradient-based RL on the curator rather than gradient-free forward learning
- [[skill-curator]] — introduces the skill curator as an architectural pattern
- [[rl-trained-skill-curator-outperforms-frontier-curator]] — core empirical claim from this paper
- [[comprehensive-survey-self-evolving-ai-agents]] — cited survey; provides taxonomy of self-evolution paradigms
- [[evo-memory-benchmarking-llm-agent-test]] — cited benchmark for LLM agent memory
