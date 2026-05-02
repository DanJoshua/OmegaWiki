---
title: "SoK: Agentic Skills - Beyond Tool Use in LLM Agents"
slug: sok-agentic-skills-beyond-tool-use
arxiv: "2602.20867"
venue: "arXiv"
year: 2026
tags:
  - agents
  - llm-agents
  - agentic-skills
  - skill-lifecycle
  - design-patterns
  - security
  - governance
  - sok
importance: 4
date_added: 2026-05-02
source_type: tex
s2_id: ""
keywords:
  - agentic skills
  - skill lifecycle
  - representation x scope taxonomy
  - system-level design patterns
  - security in agent systems
domain: "ML Systems"
code_url: ""
cited_by: []
---

## Problem

LLM agents repeatedly re-derive execution strategies from scratch for every task: procedural knowledge gained from experience evaporates with the context window. Existing surveys cover LLM agents broadly, tool use specifically, or multi-agent coordination, but none adopt a *skill-centric* lens that traces the lifecycle from acquisition through governance. The paper systematizes the emerging "skill layer" — reusable, callable, governable procedural modules sitting between atomic tools and one-shot plans.

## Key idea

Define an **agentic skill** as a four-tuple `S = (C, π, T, R)`:

- `C: O × G → {0,1}` — applicability condition (predicate over observation and goal)
- `π: O × H → A ∪ Σ` — executable policy (NL, code, learned controller, or hybrid; may invoke other skills `Σ` for hierarchical composition)
- `T: O × H × G → {0,1}` — termination condition
- `R = (name, params, returns)` — reusable callable interface

This formalization parallels the RL options framework `(I, π, β)` of Sutton et al. but adds the explicit interface `R` so skills are runtime-invocable rather than chosen implicitly by a meta-policy. The four components are argued to be a minimal schema: removing any one collapses skills back to policies, plans, internal knowledge, or metadata.

Two complementary taxonomies organize the space:

1. **Seven system-level design patterns** describing how skills are packaged and executed: P1 metadata-driven progressive disclosure, P2 code-as-skill, P3 workflow enforcement, P4 self-evolving skill libraries, P5 hybrid NL+code macros, P6 meta-skills (skills that create skills), P7 plugin/marketplace distribution.
2. **Orthogonal representation × scope taxonomy** describing what skills *are* (NL, code-as-skill, tool macros, policy-based, hybrid) and what environments they operate over (single-tool, multi-tool, web, OS/desktop, software engineering, robotics).

## Method

Systematization of Knowledge methodology over a curated corpus of LLM-agent and skill-library systems:

- Literature search and selection through major venues (NeurIPS, ICLR, COLM, ACL, arXiv) plus production agent systems (Claude Code, OpenClaw, GPT Store, MCP).
- Taxonomy development: design patterns derived inductively from system architectures; representation × scope axes derived from skill artifacts.
- A seven-stage **skill lifecycle model** anchors the survey: discovery → practice/refinement → distillation → storage → retrieval/composition → execution → evaluation/update, with feedback loops connecting evaluation back to practice and execution back to discovery.
- Security analysis enumerates six threat categories (poisoned skill retrieval, malicious skill payloads, cross-tenant leakage, skill drift exploitation, confused deputy via environmental injection, applicability-condition `C`-poisoning) and maps each to design patterns through a pattern-specific risk matrix.
- A four-tier trust model (T1 metadata only → T2 instruction access → T3 supervised execution → T4 autonomous execution) formalizes progressive disclosure, with sticky tiers and runtime-enforced transitions.
- Anchor case studies: the **ClawHavoc** marketplace supply-chain attack on the OpenClaw ClawHub registry, and the **SkillsBench** benchmark of curated vs self-generated skills.

## Results

- **Concept unification**: a comparison table separates skills from tools, plans, episodic memory, and prompt templates along five axes (unit of reuse, execution semantics, verification surface, composability, governance surface).
- **Pattern co-occurrence**: surveyed systems use a median of 2 patterns (range 1-4); the most common combination is P1+P7 (metadata + marketplace, 4 systems); Claude Code and OpenClaw use 4 patterns each.
- **Empirical anchor (SkillsBench)**: curated skills lift agent pass rates by **+16.2 pp on average**, while self-generated skills *degrade* performance by **-1.3 pp**. Smaller models with curated skills can outperform larger models without them. Domain-specific gains: **+51.9 pp in healthcare**, +41.9 pp in manufacturing, +4.5 pp in software engineering, +6.0 pp in mathematics — skills help most where pretraining data is procedurally sparse.
- **ClawHavoc case study**: 1,184 malicious skills identified across the ClawHub registry within weeks of launch; 36.8% of all published skills contained at least one security flaw; one publisher account responsible for 677 packages (57% of malicious listings); 91% of malicious skills carried prompt-injection payloads weaponizing the agent itself; payloads targeted LLM API keys, 60+ cryptocurrency wallet types, browser credentials, SSH keys, and Keychain entries; over 135,000 exposed OpenClaw instances detected in 82 countries. Belgium's CCB and China's MIIT issued advisories; multiple South Korean firms blocked OpenClaw entirely.
- **Tuple-level audit framework**: argues that traditional binary scanners (e.g., VirusTotal) can only audit `π_code` and partly `R`, missing attacks on `C` (overbroad applicability), `π_NL` (NL-level prompt injection), and `T` (early/late termination evasion). Skill-native auditors like Agent Skills Guard and SkillGuard combine rule/AST analysis, LLM semantic inspection, and reputation scoring across the full `(C, π, T, R)` surface.

## Limitations

- Methodology constraints: corpus selection biased toward English-venue and production-system documentation; rapidly evolving production systems (Claude Code, OpenClaw) may shift between SoK preparation and publication.
- The four-tuple formalization is deliberately representation-agnostic, leaving open *how* applicability `C` and termination `T` are concretely instantiated for NL or hybrid skills — a gap the paper acknowledges.
- The empirical anchor (SkillsBench) is a single benchmark with 86 tasks across 7,308 trajectories; scope-axis claims (healthcare, manufacturing) come from one source.
- Pattern-3 (workflow enforcement) is acknowledged as operating at the controller level rather than as a reusable artifact, blurring the pattern boundary.
- The ClawHavoc analysis depends largely on third-party reporting (VirusTotal, Snyk, security researchers) rather than primary forensic data.

## Open questions

- **Verified autonomous skill generation**: how to gate self-generated skills with regression-style evaluation analogous to CI before admission to a library?
- **Unsupervised skill discovery**: can RL-style unsupervised skill-discovery techniques transfer to LLM agents, identifying skill boundaries from interaction traces alone?
- **Formal verification across heterogeneous representations**: NL/policy skills resist static analysis; combining rule-based, semantic-LLM, and runtime-behavioral verification.
- **Robustness under environmental drift**: detecting when API/UI/data-format changes silently invalidate a skill's assumptions.
- **Governance economics and liability**: assigning responsibility among skill authors, platform operators, and users in marketplace ecosystems, and aligning incentives with reliability via certification.

## My take

The paper's strongest contribution is the `(C, π, T, R)` four-tuple — it gives a concrete reason to distinguish a skill from a plan, prompt template, or memory entry, and grounds the security analysis at the right level of abstraction (the tuple-level audit gap framing is genuinely useful for thinking about defense in depth). The seven-pattern taxonomy is helpful as an organizational scaffold but somewhat hand-curated; Pattern-3's "controller-level" caveat exposes the seam. The ClawHavoc anchor case is a vivid concretization but reads as more journalistic than forensic. The SkillsBench numbers (+16.2 pp curated vs -1.3 pp self-generated) are the empirical lever the field needs — if they replicate, they re-frame "self-evolving libraries" from aspirational pattern to caveat-laden one. The paper's connection to RL options and HTN/BDI/STRIPS planning is the right move and is under-emphasized in adjacent surveys.

## Related

- Concepts: [[agentic-skill]], [[skill-lifecycle]], [[skill-marketplace-supply-chain-risk]]
- Claims: [[curated-skills-outperform-self-generated]], [[skill-marketplaces-expose-supply-chain-risk]]
- Topic: [[self-evolving-agents]]
- Sibling /init papers (paper-paper edges backfilled at fan-in)
