---
title: "Skill Marketplace Supply-Chain Risk"
aliases:
  - skill supply-chain attack
  - agent skill marketplace risk
  - skill registry compromise
tags:
  - security
  - supply-chain
  - agents
  - skills
  - governance
maturity: emerging
key_papers:
  - sok-agentic-skills-beyond-tool-use
first_introduced: "2026"
date_updated: 2026-05-02
related_concepts:
  - agentic-skill
  - skill-lifecycle
---

## Definition

**Skill marketplace supply-chain risk** is the class of threats arising when LLM agents pull executable or NL-policy skills from third-party registries (Pattern-7 in the SoK pattern taxonomy). A compromised, malicious, or drifted skill propagated through the registry can act with the agent's full permission scope — exfiltrating credentials, persisting in infrastructure, or weaponizing the agent itself via prompt injection — while appearing benign at the metadata level.

## Intuition

Skill marketplaces inherit the threat model of npm/pip/extension stores but add three multipliers: (i) skills *execute* agent actions, not just code in a sandbox; (ii) NL components carry prompt-injection payloads invisible to binary scanners; (iii) the agent is itself a programmable accomplice — a malicious skill can use the agent's legitimate tools to achieve ends the user never authorized (the *confused deputy* via environmental injection).

## Formal notation

Mapping to the agentic-skill tuple `S = (C, π, T, R)`:

- `R` (interface) — name-squatting, misleading descriptions, faked download counts manipulate discovery.
- `C` (applicability) — overbroad predicates that return `1` everywhere maximize blast radius (`C`-poisoning).
- `π_code` — supply-chain code-injection (the npm/pip analogue).
- `π_NL` — prompt-injection embedded in skill text/README; invisible to AV.
- `T` (termination) — premature termination to evade logging, or non-termination to maintain persistent access.

Defense-in-depth requires auditors to cover all four components; binary scanners cover only `π_code` (and weakly `R`).

## Variants

- **Direct payload attacks**: malicious code in `π_code` (e.g., AMOS-style infostealers in OpenClaw skills).
- **Documentation-as-attack-surface**: README/setup instructions tell users to run `curl | bash` pipelines (Pattern-5 NL/code boundary exploit).
- **Confused-deputy attacks**: prompt injection in skill payloads steers the agent to misuse a privileged but uncompromised skill.
- **Drift-exploitation**: a skill safe at authoring time becomes unsafe as the environment evolves; adversary controls the environment, not the skill.
- **Self-evolving propagation**: a Pattern-4 library ingests a malicious community skill as a template; poison propagates through the agent's own generation loop.

## Comparison

| Surface | Traditional pkg risk | Skill marketplace risk |
|---|---|---|
| Code | Yes (covered by AV/SCA) | Yes |
| NL/docs | Documentation only | **Executable instruction-following payload** |
| Activation scope | Explicit imports | **Embedding-similarity retrieval over `R`** |
| Privilege | Process-level | **Agent's full tool/permission scope** |
| Defender | OS sandbox, AV | OS sandbox + skill-native auditor + runtime monitor |

## When to use

Apply this concept whenever an agent's skill source includes any third-party or community channel: assess provenance signing, dependency auditing, continuous monitoring, version pinning, and tuple-level (not just binary) skill auditing.

## Known limitations

- Tuple-level auditors (e.g., Agent Skills Guard, SkillGuard) are early-stage; published evaluations are small (39 test cases including 4 adversarial samples).
- Reputation scoring is gameable when download/star counts can be inflated (see ClawHavoc: 4,000 faked downloads inflated a malicious skill's ranking).
- Runtime behavioral monitoring covers attacks on `T` and context-dependent exploits but raises overhead.

## Open problems

- Detecting `C`-poisoning (overbroad applicability) automatically.
- Anti-injection guarantees for NL policies that cannot be statically analyzed.
- Liability allocation among skill authors, platform operators, and users.
- Certification mechanisms that align market incentives with reliability.

## Key papers

- [[sok-agentic-skills-beyond-tool-use]] — provides the threat-model taxonomy, the trust-tier model, and the ClawHavoc anchor case study (1,184 malicious skills, 36.8% flaw rate, 91% prompt-injection payloads, 135,000+ exposed instances across 82 countries).

## My understanding

The non-obvious risk multiplier is not the code in `π_code` (well-trodden npm-style territory) but the agent-as-accomplice channel: a skill's NL payload uses *legitimate* tool access to achieve the attacker's goal, so any defense that operates only at the skill artifact level misses it. The right defensive posture is layered: rule/AST analysis for `π_code`, LLM semantic inspection for `π_NL` and `C`, and runtime behavioral monitoring for `T` and context-dependent exploits. Trust tiers (T1 metadata-only → T4 autonomous) are useful but only when transitions are runtime-enforced, not metadata-declared.
