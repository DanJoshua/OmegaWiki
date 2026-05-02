---
title: "A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence"
slug: survey-self-evolving-agents-what-when
arxiv: "2507.21046"
venue: "TMLR"
year: 2026
tags:
  - survey
  - self-evolving-agents
  - llm-agents
  - continual-learning
  - taxonomy
importance: 4
date_added: 2026-05-02
source_type: tex
s2_id: ""
keywords:
  - agent evolution
  - continual adaptation
  - evolutionary dynamics
  - multi-agent co-evolution
  - real-time learning
domain: "NLP"
code_url: "https://github.com/CharlesQ9/Self-Evolving-Agents"
cited_by: []
---

## Problem

Large Language Models are fundamentally static: they cannot adapt their internal parameters, memory, tools, or workflow when faced with novel tasks, evolving knowledge domains, or dynamic interaction contexts. This becomes a critical bottleneck as LLMs are deployed in open-ended interactive environments where conventional retrieval is inadequate. Existing surveys treat agent evolution as a subsidiary topic inside broader agent taxonomies, leaving the core questions of *what* should evolve, *when* it should evolve, and *how* to implement that evolution underexplored as a first-class research paradigm.

## Key idea

Self-evolving agents are characterized not by a specific algorithm but by **the locus of autonomy**: an agent that modifies its internal parameters, contextual state, toolset, or architectural topology based on its own trajectories or feedback signals, with the explicit objective of improving future performance. The survey establishes a unified taxonomy organized around four orthogonal dimensions — *what to evolve* (model, memory, tools, architecture), *when to evolve* (intra-test-time vs inter-test-time), *how to evolve* (reward-based, imitation/demonstration, population-based), and *where to evolve* (general vs specialized domains) — and frames the field as a path toward Artificial Super Intelligence (ASI).

## Method

The survey formalizes the agent system as a tuple over a partially observable Markov Decision Process (POMDP) and defines a *self-evolving strategy* as a transformation `f(Π, τ, r) → Π'` that maps the current agent system to a new state given a trajectory and feedback. Three inclusion criteria operationally bound the paradigm: (i) updates must be **experience-dependent**, (ii) updates must produce a **persistent, policy-changing** effect rather than transient instruction-following, and (iii) the system must possess **autonomous exploration or self-initiated learning**. The authors then map the literature into a structured taxonomy across the four dimensions and contrast self-evolving agents with curriculum learning, lifelong learning, model editing, and unlearning through both a problem-setting and a solution-paradigm lens.

## Results

- A unified theoretical framework for characterizing self-evolutionary processes anchored on three foundational dimensions: what evolves, when, and how.
- A landscape covering evolution across model parameters, prompts, memory, tools, single- and multi-agent architectures, mapped against intra- vs inter-test-time stages and against reward-based, imitation, and population-based methods.
- A dedicated review of evaluation goals (adaptivity, retention, generalization, efficiency, safety, self-directedness) and three evaluation paradigms (static, short-horizon, long-horizon lifelong assessment).
- A practitioner-oriented compliance checklist covering tool/code safety, self-modification control, behavioral and alignment safety, data privacy, and operational governance.
- Identification of safety-critical phenomena such as **misevolution** and the **Alignment Tipping Process (ATP)** as emergent risks unique to self-evolving systems.

## Limitations

- Conceptual rather than empirical: the survey itself contributes no measurements; categorical placements depend on author judgment.
- The taxonomy is acknowledged to be "guiding synthesis rather than a review of a fully established paradigm" — boundaries between proto-evolution and strong self-evolution remain fuzzy.
- Evaluation coverage exposes that current benchmarks underserve long-horizon lifelong assessment and intersected capabilities (adaptivity AND safety AND retention together).
- Coverage skews toward LLM-centric agents; embodied and robotic self-evolution receive lighter treatment.

## Open questions

- How to evaluate self-evolving agents over long horizons in a fair, reproducible way that disentangles base-model improvements from genuine self-evolution gains?
- What guarantees can be given against misevolution (safety/alignment drift induced by the evolution process itself)?
- How to enable knowledge transfer across self-evolving agents without collapsing into shallow pattern matching?
- What is the right interface between self-evolution and human oversight (approval gates, rollback, audit trails) that scales to autonomous operation?
- How do co-evolutionary dynamics between agents and their environments converge or diverge?

## My take

This is the framing reference for the self-evolving-agents topic in this wiki: the *what / when / how / where* decomposition is the most compact taxonomy currently in use and is the right axis to file subsequent ingests against. The operational definition (experience-dependent, persistent, autonomous) is strong enough to gate what counts as self-evolution versus iterated prompting. The paper's safety section — particularly the misevolution and ATP framings — should anchor any future claims about safety/alignment drift in evolving agents. Treat as a structural index rather than a source of empirical claims.

## Related

- [[self-evolving-agent]] — core concept formalized here
- [[misevolution]] — emergent safety risk identified by this survey
- [[what-when-how-evolution-taxonomy]] — the survey's organizing taxonomy
- [[claim-static-llm-agents-need-evolution]] — motivating claim
- [[claim-self-evolution-introduces-emergent-safety-risks]] — safety-critical claim
