---
title: "Self-evolving Agents"
tags:
  - agents
  - self-evolution
  - continual-learning
  - tool-use
my_involvement: reading
sota_updated: 2026-05-14
key_venues:
  - arXiv
  - ICLR
  - COLM
  - TMLR
  - ACL
related_topics: []
key_people: []
---

## Overview

Self-evolving agents are LLM-based agents that improve themselves at deployment time — through evolving memory, learned skills, refined tool-use policies, or experience-driven lifecycles. Provisional topic page seeded by `/init` on 2026-05-02; SOTA, seminal works, and key people will be filled in by `/ingest` and subsequent `/check` and `/refine` passes.

## Timeline

To be filled in.

## Seminal works

To be filled in. The two recent surveys provide structural framing:
- [[survey-self-evolving-agents-what-when]]
- [[comprehensive-survey-self-evolving-ai-agents]]

## SOTA tracker

- [[learning-supervision-semantic-episodic-memory-reflective]] (2026, CAIS) — critique-grounded episodic+semantic memory adaptation without parameter updates; +8.1pp over zero-shot across 6 datasets.
- [[skillos-learning-skill-curation-self-evolving]] (2026, arXiv) — RL-trained skill curator (8B) outperforms frontier model curator (Gemini-2.5-Pro) on ALFWorld; +9.8% relative over strongest memory baseline with fewer interaction steps; introduces executor-grounded skill curation via GRPO on grouped task streams.
- [[skill-r1-agent-skill-evolution-reinforcement]] (2026, COLM submitted) — bi-level GRPO trains a separate lightweight skill generator (Qwen3-4B) to iteratively revise skills for a frozen task LLM; +12.1pp over Vanilla GRPO on GAIA (41.8% total); introduces recurrent-skill-evolution with intra/inter-generation advantages.
- [[skillgen-verified-inference-time-agent-skill]] (2026, NeurIPS submitted) — multi-agent framework synthesizes a single auditable skill via contrastive induction over success/failure trajectories + intervention-based verification gate; +3.27 to +10.08pp across 8 base models on 7+ benchmarks; cross-model skill transfer holds for 70% of off-diagonal pairs.
- [[skillgraph-skill-augmented-reinforcement-learning-agents]] (2026, NeurIPS 2026 preprint) — graph-structured skill library with typed dependency edges; graph-aware topological retrieval + co-evolution via RL; +44.3pp over ExpeL on ALFWorld; +11.7 over SkillRL on WebShop; zero-shot transfer across 5 QA datasets.

## Open problems

To be derived from `wiki/graph/open_questions.md` after ingest.

## My position

To be filled in.

## Research gaps

To be filled in.

## Key people

To be populated by `/ingest`.
