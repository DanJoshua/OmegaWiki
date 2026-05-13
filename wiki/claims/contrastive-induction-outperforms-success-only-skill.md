---
title: "Contrastive induction over success+failure trajectories outperforms success-only skill synthesis"
tags:
  - skill-synthesis
  - contrastive-learning
  - trajectories
  - agents
status: supported
confidence: 0.82
evidence:
  - source: skillgen-verified-inference-time-agent-skill
    type: supports
    note: "Ablation A4 (no Failure Lessons) shows reduced gains on ALFWorld OOD and ChemLLMBench yield prediction; the full SkillGen with contrastive induction achieves best results on every dataset-model pair."
---

## Statement

Including failure trajectories and their contrastive analysis against nearby successes — rather than summarizing successful trajectories alone — improves the quality of synthesized agent skills, as measured by held-out performance gains.

## Evidence

- [[skillgen-verified-inference-time-agent-skill]] supports: ablations confirm that removing Failure Lessons (A4) degrades SkillGen performance; contrastive local pairing surfaces small action-choice differences that cluster-level success summaries miss.

## Linked ideas

## Caveats

Established in interactive + scientific task domains (ALFWorld, ScienceWorld, ChemLLMBench). May require sufficient failure trajectories to form meaningful clusters; very low failure rates may degenerate to success-only learning.
