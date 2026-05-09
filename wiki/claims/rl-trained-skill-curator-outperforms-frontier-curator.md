---
title: "RL-Trained Skill Curator Outperforms Frontier Model Curator Due to Executor Alignment"
slug: rl-trained-skill-curator-outperforms-frontier-curator
status: weakly_supported
confidence: 0.68
tags:
  - skill-curation
  - self-evolving-agents
  - reinforcement-learning
  - executor-alignment
domain: "NLP"
source_papers:
  - skillos-learning-skill-curation-self-evolving
evidence:
  - source: skillos-learning-skill-curation-self-evolving
    type: supports
    strength: moderate
    detail: "SkillOS's 8B RL-trained curator (Qwen3-8B) outperforms SkillOS-Gemini (Gemini-2.5-Pro used directly as curator) on ALFWorld with Qwen3-8B executor. The gap is especially large for smaller executors, confirming that frontier-model curation without executor-grounding produces skills misaligned with the executor's capacity. Gemini-2.5-Pro still improves over no-memory, but RL training closes an additional +7.9pp on ALFWorld (Qwen3-8B executor) and +9.5pp (Gemini-2.5-Pro executor) versus the RL-untrained base curator."
conditions: "Holds when executor is Qwen3-8B or Qwen3-32B; partially holds with Gemini-2.5-Pro executor. Scope: ALFWorld and WebShop household/shopping tasks. Reasoning task gains exist but are smaller."
date_proposed: 2026-05-09
date_updated: 2026-05-09
---

## Statement

A skill curator trained via reinforcement learning on grouped task streams — with rewards derived from the downstream performance of a *specific* frozen executor — outperforms a stronger frontier LLM used as a zero-shot curator. The mechanism is **executor alignment**: RL training shapes the curator to produce skills that match the executor's actual capacity and usage patterns, whereas a frontier curator produces skills calibrated to its own (stronger) reasoning ability, making them harder for a weaker executor to exploit.

## Evidence summary

- **SkillOS (2026)** evaluates on ALFWorld with Qwen3-8B executor: RL-trained 8B curator achieves SR=61.2, vs. SR=55.7 for ReasoningBank (strongest baseline) and SR≈57 for the Gemini-2.5-Pro zero-shot curator variant. The 8B curator — 4× smaller in parameter count — beats the frontier curator.
- Effect holds for Qwen3-32B executor and partially for Gemini-2.5-Pro executor.
- Analysis shows the RL curator produces more targeted skill use (fewer redundant retrieval misses) and evolves skills into richer meta-skill structures, consistent with the alignment hypothesis.

## Conditions and scope

- Requires a stable frozen executor during curator training; if the executor co-evolves, the alignment target shifts and the advantage may diminish.
- The gap is larger for smaller executors (Qwen3-8B) than larger ones (Gemini-2.5-Pro executor narrows the gap because the frontier curator is better aligned with a frontier executor).
- Task domain: household tasks and online shopping. Math reasoning shows weaker but present gains.
- Validated on a single RL algorithm (GRPO) and one curation framework; other RL algorithms and repository formats are untested.

## Counter-evidence

None directly. Note that SkillOS-Gemini (frontier curator) still improves over no-memory, so the claim is not that frontier curators are harmful — only that executor-grounded training outperforms them.

## Linked ideas

## Open questions

- Does the alignment gap persist when the executor is itself a frontier model (curator and executor equally strong)?
- Can executor-aligned curation be achieved without RL training — e.g., by prompting the curator with explicit executor capacity descriptions?
- Does the gap close with more in-context examples of the executor's behaviour provided to the frontier curator?
