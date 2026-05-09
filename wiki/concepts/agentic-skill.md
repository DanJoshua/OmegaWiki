---
title: "Agentic Skill"
aliases:
  - skill (LLM agent)
  - procedural module
  - reusable agent skill
tags:
  - agents
  - llm-agents
  - procedural-memory
  - skills
maturity: emerging
key_papers:
  - sok-agentic-skills-beyond-tool-use
  - skillos-learning-skill-curation-self-evolving
first_introduced: "2026"
date_updated: 2026-05-09
related_concepts:
  - skill-lifecycle
  - skill-curator
  - skill-marketplace-supply-chain-risk
---

## Definition

An **agentic skill** is a reusable, callable module that encapsulates a sequence of actions or policies enabling an LLM-based agent to achieve a class of goals under recurring conditions. Formally, a skill is a four-tuple `S = (C, π, T, R)` where `C` is an applicability condition, `π` is an executable policy, `T` is a termination condition, and `R` is a reusable callable interface (name, params, returns).

## Intuition

Skills are the **procedural memory** of an LLM agent. Without a skill layer, every task forces the agent to re-derive a procedure from first principles inside a finite context window. Skills compress learned procedures into reusable modules, analogous to how chunking in human expertise compresses multi-step procedures into single retrievable units. They are simultaneously *executable* (unlike plans), *reusable* (unlike one-shot reasoning), and *governable* (unlike prompt templates).

## Formal notation

Let an agent interact with environment `E` via action space `A`, observation space `O`, and goal space `G`, with history `H = (o_1, a_1, ..., o_{t-1}, a_{t-1})`. A skill is:

```
S = (C, π, T, R)
C : O × G → {0,1}                  # applicability gate
π : O × H → A ∪ Σ                  # policy; may invoke other skills s ∈ Σ
T : O × H × G → {0,1}              # termination
R = (name, params, returns)        # callable interface
```

Soft applicability scores `C : O × G → [0,1]` with thresholding are common in implementations; the binary form is a simplifying convention. The formalization parallels the RL options framework `(I, π, β)` of Sutton et al. (1999); `R` is the addition that distinguishes skills (explicitly invocable) from options (implicitly chosen by a meta-policy).

## Variants

- **Natural-language skills**: `π` expressed entirely in NL (SOPs, playbooks). Easy to author, hard to verify.
- **Code-as-skill**: `π` is an executable program (Python function, shell script, DSL). Deterministic and testable; brittle to API drift.
- **Tool macros**: structured sequences of tool calls with parameterization logic; middle ground between NL and code.
- **Policy-based skills**: `π` is a learned parameterized function (e.g., a fine-tuned controller). Opaque but captures subtle patterns.
- **Hybrid representations**: combine NL, code, and references in a single skill (e.g., Claude skills, ReAct prompts).

## Comparison

| Concept | Unit of reuse | Execution semantics | Verification surface |
|---|---|---|---|
| Tool | Single API call | Stateless, single invocation | I/O schema |
| Plan | Task decomposition | One-time reasoning scaffold | Step consistency |
| Episodic memory | Stored observation | Retrieval, no execution | Relevance, recency |
| Prompt template | Text fragment | Injected into context | Output quality |
| **Agentic skill** | **Procedural module** | **Callable workflow with termination** | **Outcome correctness, safety** |

## When to use

- Recurring task patterns whose solution is stable enough to package once and call many times.
- Workflows where determinism, testability, or auditability are required (favor code-as-skill).
- Domains where pretraining data is procedurally sparse (e.g., healthcare, manufacturing) — empirical evidence suggests skills add the largest pass-rate gains there.

## Known limitations

- Boundary ambiguity in hybrid NL+code skills creates inconsistent execution.
- Self-generated skills can degrade performance when admitted without verification (see [[curated-skills-outperform-self-generated]]).
- Code skills are brittle to API/UI drift; NL skills resist binary auditing.
- The `(C, π, T, R)` formalization is representation-agnostic but does not specify how `C` and `T` are concretely realized for NL skills.

## Open problems

- Verified autonomous skill generation (CI-style admission gates).
- Unsupervised skill discovery from interaction traces alone.
- Formal verification across heterogeneous representations.
- Robustness under environmental drift.

## Key papers

- [[sok-agentic-skills-beyond-tool-use]] — formalizes the four-tuple definition and the seven-pattern + representation×scope taxonomies.
- [[skillos-learning-skill-curation-self-evolving]] — uses Markdown-format skills (YAML frontmatter + NL instructions) managed by a trainable skill curator; shows that skill representation and curation quality jointly determine self-evolution performance.

## My understanding

The four-tuple is the right level of abstraction: it explains why a tool is not a skill (no `C`, `T` is implicit), why a plan is not a skill (no persistent `R`), and why episodic memory is not a skill (no `π`). The hardest piece in practice is `C`: most production systems either approximate it via embedding similarity over `R.description` (Pattern-1) or push it onto the orchestrator. The `T` component is also under-specified in NL skills — terminating "when the user is satisfied" is not a predicate, just a hope.
