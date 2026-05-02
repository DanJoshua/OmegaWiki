---
title: "Gradient-free experience-library learning can match or exceed gradient-based parameter tuning on agentic reasoning benchmarks"
slug: claim-gradient-free-agents-can-match-parameter-tuning
status: weakly_supported
confidence: 0.45
tags:
  - self-evolving-agents
  - llm-agents
  - gradient-free-learning
  - parameter-efficient-tuning
domain: "NLP"
source_papers:
  - flex-continuous-agent-evolution-forward-learning
evidence:
  - source: flex-continuous-agent-evolution-forward-learning
    type: supports
    strength: moderate
    detail: "FLEX yields large absolute gains over vanilla, ICL, and ReAct baselines on AIME25 (+10 to +23), USPTO50k (+7 to +10), and ProteinGym (+8.9 to +13.7) using only 49-100 training samples and zero parameter updates, on benchmarks where parameter-based reasoning post-training (DAPO, R1-style RL) is the established route."
conditions: "Reported on small test sets (AIME25 n=30, USPTO50k slice n=100); no head-to-head comparison against PEFT (LoRA) or recent RL post-training baselines on equivalent compute."
date_proposed: 2026-05-02
date_updated: 2026-05-02
---

## Statement

A purely gradient-free learning paradigm — keeping the LLM frozen and evolving an external natural-language experience library — can produce reasoning gains on the order of, or larger than, gains typically attributed to parameter-based post-training (RLHF, RFT, RL with verifiable rewards) on multi-domain agentic reasoning benchmarks.

## Evidence summary

Direct evidence is FLEX's main results table. Examples:

- **AIME25**: Claude-Sonnet-4 baseline 40% to 63.3% (+23.3); DeepSeek-V3.1-Terminus 56.7% to 66.6% (+10.0).
- **USPTO50k**: Claude-Sonnet-4.5 20% to 30% (+10); GPT-5 9% to 16% (+7).
- **ProteinGym**: Claude-Sonnet-4 0.460 to 0.597 (+0.137 Spearman).

Across these, ICL and ReAct baselines are also dominated by FLEX. The key ambiguity: FLEX is not benchmarked against modern PEFT (e.g., LoRA-tuned reasoning fine-tunes) or against parameter-based RFT/RL on equivalent compute. The claim of "matching or exceeding" parameter tuning is therefore inferred from absolute deltas, not from a direct comparison.

## Conditions and scope

- Holds for tasks where small training sets (50-100 examples) can be distilled into transferable strategies (math, retrosynthesis, biology).
- Holds when the base LLM is already reasonably capable; FLEX's information-theoretic argument assumes the model distribution is close to the true conditional.
- Open whether the claim holds on tasks requiring perceptual grounding, long-horizon planning, or large training corpora.

## Counter-evidence

- No published RL post-training baseline at matched compute on the same FLEX configurations.
- Parameter-based reasoning fine-tunes (DeepSeek-R1, DAPO) report comparable or larger absolute reasoning gains in their own settings, leaving open which paradigm wins under matched evaluation.
- Test slices are small (AIME25 n=30; USPTO50k n=100), so confidence intervals overlap baseline noise.

## Linked ideas

(none yet)

## Open questions

- Direct head-to-head: FLEX vs. LoRA-tuned reasoning fine-tune on AIME25 with matched compute and matched data.
- Does FLEX's advantage shrink or grow on tasks where parameter tuning has more headroom (e.g., low-resource domain pretraining)?
- Are the gains additive with parameter-based methods, or competitive?
