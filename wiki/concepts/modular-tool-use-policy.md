---
title: "Modular Tool-Use Policy"
aliases:
  - modular agent policy
  - planner-selector-caller-synthesizer
  - decomposed tool-use policy
tags:
  - llm-agents
  - tool-use
  - agent-architecture
  - policy-decomposition
maturity: emerging
key_papers:
  - evotool-self-evolving-tool-use-policy
first_introduced: "2026"
date_updated: 2026-05-02
related_concepts:
  - trajectory-grounded-blame-attribution
  - diversity-aware-population-selection
---

## Definition

A Modular Tool-Use Policy is a fixed compositional decomposition of an LLM agent's tool-use behavior into four explicit sub-policies — Planner, Selector, Caller, and Synthesizer — each parameterized by an evolvable natural-language specification under frozen base-LLM weights. The full policy is a composition $\Pi = \pi_{\text{syn}} \circ \pi_{\text{call}} \circ \pi_{\text{sel}} \circ \pi_{\text{plan}}$ in which each module operates on intermediate state from the previous module. Optimization touches only the module specifications $\Theta = \{\theta_{\text{plan}}, \theta_{\text{sel}}, \theta_{\text{call}}, \theta_{\text{syn}}\}$.

## Intuition

Tool use is not a single skill; it is a chain of partially competing competencies (high-level decomposition, tool retrieval, schema-faithful argument construction, evidence-grounded synthesis) that can interfere with one another under monolithic optimization. Decomposing the policy makes it explicit which competency is responsible at each step, which (combined with module-level credit signals) enables *targeted* edits without disrupting unrelated behaviors.

## Formal notation

- **Planner** $\pi_{\text{plan}}$: input task → subgoals.
- **Selector** $\pi_{\text{sel}}$: state $s_t$ + subgoal → tool choice (or abstain / clarify).
- **Caller** $\pi_{\text{call}}$: state + chosen tool → schema-valid argument set + execution.
- **Synthesizer** $\pi_{\text{syn}}$: tool outputs + history → final response $\hat{y}$.

Objective: $J(\Theta; W) = \mathbb{E}_x \mathbb{E}_{\tau \sim \pi_{\Theta,W}|x}[R(x, \hat{y}(\tau))]$, optimized only over $\Theta$.

## Variants

- **Four-module (EvoTool default)**: Planner / Selector / Caller / Synthesizer.
- **Three-module collapses**: collapse Selector + Caller into a single "Tool-call" module (closer to ReAct-style scaffolds) — simpler but loses the schema-vs.-choice distinction needed by Caller-targeted blame.
- **Five-or-more-module extensions**: add Memory, Verifier, or Critic modules. Untested in EvoTool but suggested by the introducing paper as a natural extension.

## Comparison

- Vs. **monolithic prompt agents** (single system prompt covering all behaviors): modular decomposition exposes stage-specific failure modes for diagnosis.
- Vs. **single-aspect optimization** (AdaPlanner, EasyTool, DRAFT, AnyTool — each fixes one component): the modular decomposition keeps every module evolvable so cross-module error propagation can be addressed.
- Vs. **monolithic + reflection** (e.g. Reflexion over a single agent prompt): modular decomposition lets reflection be aimed at the responsible module rather than rewriting the global prompt.

## When to use

- Long-horizon agent tasks with structured tool APIs where error can plausibly originate at any of the four stages.
- Settings where you want interpretable, auditable updates: each generation tells you which module changed and why.
- As a substrate for blame-aware optimization (see [[trajectory-grounded-blame-attribution]]).

## Known limitations

- The four-module decomposition is hand-designed; whether it is optimal for non-API tool ecosystems (multi-modal tools, embodied agents) is untested.
- Module boundaries can blur in practice — e.g., a Selector that "thinks ahead" implicitly does some planning, leaking competencies between modules.
- Editing module specifications is still discrete prompt editing, with all the brittleness of that medium.

## Open problems

- Are there principled criteria (information-theoretic or empirical) for choosing the right number / boundaries of modules per task family?
- Can module boundaries be *learned* rather than hand-specified?
- How does the modular structure interact with longer agent loops that include verification, self-correction, or memory updates?

## Key papers

- [[evotool-self-evolving-tool-use-policy]] — formalizes the four-module composition and uses it as the substrate for blame-aware mutation

## My understanding

The four-module decomposition is the *enabling assumption* of EvoTool's whole pipeline: blame attribution and targeted mutation only make sense if the policy has clean module boundaries to attribute *to*. The decomposition is intuitive and matches existing tool-use literature (ReAct-style planner + selector vs. function-call APIs), but its sharp boundaries are a modeling choice rather than a learned property.
