---
title: "Skill marketplaces expose LLM agents to a distinctive supply-chain attack surface"
slug: skill-marketplaces-expose-supply-chain-risk
status: supported
confidence: 0.8
tags:
  - security
  - supply-chain
  - agents
  - skills
  - governance
domain: "ML Systems"
source_papers:
  - sok-agentic-skills-beyond-tool-use
evidence:
  - source: sok-agentic-skills-beyond-tool-use
    type: supports
    strength: strong
    detail: "ClawHavoc anchor case study: 1,184 malicious skills identified across the OpenClaw ClawHub registry within weeks of launch; 36.8% of all published skills carried at least one security flaw (Snyk audit); one publisher account responsible for 677 malicious packages (57% of malicious listings); 91% of malicious skills carried prompt-injection payloads weaponizing the agent itself; payloads exfiltrated LLM API keys, 60+ cryptocurrency wallet types, browser-stored credentials, SSH keys, and Keychain entries; 135,000+ exposed OpenClaw instances detected across 82 countries; emergency advisories from Belgium's CCB and China's MIIT."
conditions: "Applies to skill registries that lack provenance signing, dependency auditing, behavioral monitoring, and version pinning at launch. Risk is highest under Pattern-7 (marketplace) combined with Pattern-2 (code-as-skill) when skills run with the agent's full system permissions."
date_proposed: 2026-05-02
date_updated: 2026-05-02
---

## Statement

LLM-agent skill marketplaces (Pattern-7) introduce a supply-chain attack surface that is *qualitatively distinct* from traditional package ecosystems: skills can carry NL prompt-injection payloads invisible to binary scanners, can execute under the agent's full tool permission scope, and can weaponize the agent itself as an accomplice (confused-deputy via environmental injection). Defending requires tuple-level auditing across `(C, π, T, R)` plus runtime behavioral monitoring — binary scanning alone is insufficient.

## Evidence summary

- ClawHavoc campaign: 1,184 malicious skills, 36.8% flaw rate, 91% prompt-injection payloads, primary payload Atomic macOS Stealer (AMOS) targeting `.env` API keys, 60+ wallet types, browser credentials, SSH keys.
- VirusTotal partnership scanned 3,016+ ClawHub skills; found hundreds with malicious characteristics; explicitly acknowledged scanning is "not a silver bullet."
- Snyk audit: 283 of 3,984 skills (7.1%) exposed sensitive credentials in plaintext through LLM context windows and output logs.
- 135,000+ exposed OpenClaw instances detected in 82 countries; multiple South Korean firms blocked OpenClaw; Belgium CCB and China MIIT issued advisories.
- The SoK paper formally argues why binary scanners under-cover the threat: VirusTotal audits `π_code` and weakly `R`, but misses attacks on `C` (overbroad applicability), `π_NL` (NL prompt injection), and `T` (termination evasion).

## Conditions and scope

- Holds when registries lack provenance signing, dependency auditing, version pinning, and behavioral monitoring.
- Risk magnitude scales with the agent's tool permission breadth (file system, network, credentials, browser).
- Hard-gated workflows (Pattern-3) are less exposed because they constrain the agent's action space.

## Counter-evidence

- Tuple-level skill auditors (Agent Skills Guard, SkillGuard) report no false positives on legitimate skills and detection of adversarial samples that VirusTotal labeled benign — suggesting the attack surface, while distinctive, is partially defendable with skill-native tooling.
- Marketplace governance (provenance signing, version pinning, continuous monitoring) materially reduces risk where deployed (e.g., MCP-style authenticated servers).

## Linked ideas

To be linked when relevant ideas are recorded.

## Open questions

- What fraction of the 36.8% ClawHub flaw rate is generalizable vs. specific to OpenClaw's permission model?
- Can a tuple-level auditor robustly detect `C`-poisoning at scale?
- What liability and certification regime aligns marketplace incentives with reliability?
