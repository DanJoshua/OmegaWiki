---
title: "Skill Lifecycle"
aliases:
  - agentic skill lifecycle
  - skill curation lifecycle
  - skill management lifecycle
tags:
  - agents
  - skills
  - lifecycle
  - skill-management
maturity: emerging
key_papers:
  - sok-agentic-skills-beyond-tool-use
  - skillos-learning-skill-curation-self-evolving
  - skill-r1-agent-skill-evolution-reinforcement
first_introduced: "2026"
date_updated: 2026-05-02
related_concepts:
  - agentic-skill
  - skill-marketplace-supply-chain-risk
---

## Definition

The **skill lifecycle** is a seven-stage model that traces an agentic skill from initial formation to retirement: **discovery → practice/refinement → distillation → storage → retrieval/composition → execution → evaluation/update**. Skills are treated as evolving system components rather than static artifacts, with feedback loops connecting evaluation back to practice, retrieval back to storage, and execution back to discovery.

## Intuition

Skills do not appear fully formed. An agent first *notices* a recurring pattern (discovery), *iterates* to make it reliable (practice), *compresses* it into a stable representation (distillation), *files* it where it can be found (storage), *retrieves and composes* it for new tasks (retrieval), *runs* it under sandboxing (execution), and *monitors and updates or retires* it as the world changes (evaluation/update). Each stage is a research surface and an operational hand-off.

## Formal notation

Stages and primary research questions:

```
1. Discovery       : when does a recurring pattern justify encapsulation?
2. Practice        : how does iteration improve reliability without parameter updates?
3. Distillation    : how is a trace compressed into a stable (C, π, T, R) tuple?
4. Storage         : indexing, versioning, metadata for retrieval and governance
5. Retrieval       : embedding similarity, contextual relevance, compatibility checks
6. Execution       : sandboxing, permission control, resource limits
7. Evaluation/Update: drift detection, outcome verification, retirement
```

Feedback loops: `Evaluation → Practice` (underperforming skill), `Retrieval → Storage` (indexing miss), `Execution → Discovery` (runtime failure reveals new skill need).

## Variants

- **Tightly-coupled lifecycle (e.g., Voyager)**: discovery, practice, distillation, storage, retrieval, and execution are all owned by one closed-loop system in a deterministic environment (Minecraft).
- **Decoupled lifecycle (e.g., marketplace)**: discovery and distillation happen offline (human authors); storage, retrieval, and execution happen online; evaluation/update is delegated to community signals.
- **Self-evolving lifecycle (Pattern-4)**: every stage is automated, raising quality-control concerns at distillation and update.

## Comparison

The lifecycle complements but does not duplicate:

- **Software development lifecycle** (SDLC): shares stages but lacks the discovery-as-pattern-mining and unsupervised-discovery dimensions central to agent skills.
- **RL options framework**: covers discovery, execution, and termination but not storage, retrieval, or marketplace governance.
- **Cognitive psychology procedural memory**: covers practice and distillation (skill chunking) but not the explicit interface or marketplace stages.

## When to use

Apply the lifecycle as a *coverage checklist* when surveying or designing a skill-based agent system: which stages are owned by the system, which are delegated to humans, which are missing entirely?

## Known limitations

- The lifecycle is descriptive, not prescriptive — it does not say what stage *boundaries* are.
- Feedback loops are acknowledged but not formalized; in particular, drift-triggered re-discovery and retirement criteria remain open.

## Open problems

- Unsupervised discovery without human curricula or task definitions.
- CI-style admission gates between distillation and storage.
- Drift detection between execution and evaluation/update.
- Governance integration in storage (provenance, signing) and retrieval (trust-tier filtering).

## Key papers

- [[sok-agentic-skills-beyond-tool-use]] — proposes the seven-stage lifecycle and maps representative systems to lifecycle contributions.
- [[skillos-learning-skill-curation-self-evolving]] — instantiates stages 2–7 (practice, distillation, storage, retrieval, execution, evaluation/update) with a learned RL curation policy; introduces the modular skill-curator/executor split.

## My understanding

The lifecycle's main analytical value is exposing *missing stages* in production systems: most systems have execution and (some) retrieval, fewer have explicit distillation, and almost none have a real evaluation/update loop. Drift-triggered retirement is the stage least addressed by current research and most needed for long-lived deployments.
