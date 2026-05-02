---
title: "A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems"
slug: comprehensive-survey-self-evolving-ai-agents
arxiv: "2508.07407"
venue: "arXiv"
year: 2025
tags:
  - agents
  - self-evolution
  - multi-agent
  - lifelong-learning
  - survey
importance: 4
date_added: 2026-05-02
source_type: tex
s2_id: "4d5d951742d101e78646269a45f2573a597d54d6"
keywords:
  - self-evolving agents
  - multi-agent systems
  - agent optimisation
  - lifelong agentic systems
  - prompt optimisation
  - tool optimisation
  - memory optimisation
  - workflow topology
domain: "NLP"
code_url: "https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents"
cited_by: []
---

## Problem

LLM-based agent systems — both single-agent and multi-agent — overwhelmingly rely on manually crafted configurations (prompts, tools, memory, communication topologies) that remain static after deployment. Real-world environments, by contrast, are dynamic: user intents shift, tools change, novel tasks arrive. Manually reconfiguring such systems is labour-intensive and does not scale, and prior surveys focus on agent architecture or specific components (planning, memory, evaluation) rather than the integrated question of how an agent system can autonomously evolve over its lifetime.

## Key idea

Frame the emerging space of *self-evolving AI agents* as the next stage in an LLM-learning paradigm trajectory: **MOP (Model Offline Pretraining) -> MOA (Model Online Adaptation) -> MAO (Multi-Agent Orchestration) -> MASE (Multi-Agent Self-Evolving)**. The authors propose a unified conceptual framework that abstracts every existing self-evolving technique as an iterative optimisation loop with four components: **System Inputs** (task description, data, context), **Agent System** (the optimisation target, possibly multi-agent, decomposable into LLM/prompt/memory/tool/topology), **Environment** (provides feedback signals via evaluation metrics), and **Optimiser** (search space `S` plus optimisation algorithm `H` that updates the agent system). They also formalise the **[[three-laws-self-evolving-ai-agents]]** — Endure (safety), Excel (performance preservation), Evolve (autonomous evolution) — as guiding constraints for any self-evolution mechanism.

## Method

This is a survey, so the "method" is taxonomic. The authors organise the literature along three axes that map onto the unified framework:

1. **Single-agent optimisation** (Section 4): targets one component of the agent system at a time.
   - LLM behaviour optimisation: training-based (SFT on rationales, RL with verifiable / preference / process rewards — STaR, DeepSeek-R1, Absolute Zero, R-Zero) and test-time (feedback-based verifiers, search-based methods like CoT-SC, ToT, GoT, Forest-of-Thought).
   - Prompt optimisation: edit-based (GRIPS, Plum, TEMPERA), generative (ORPO, PromptAgent, MIPRO, Retroformer), text-gradient (ProTeGi, TextGrad), evolutionary (EvoPrompt, Promptbreeder).
   - Memory optimisation: short-term (recursive summarisation, MemoChat, MemoryBank, Reflexion) vs long-term (RAG variants, A-MEM, MemGPT, Mem0, HippoRAG, ChatDB).
   - Tool optimisation: training-based (Toolformer, ToolLLM, GPT4Tools, ToolACE; RL with ReTool, Tool-N1, Tool-Star, ARPO), inference-time (EASYTOOL, DRAFT, Play2Prompt; reasoning-based with ToolChain, Tool-Planner, MCP-Zero), and tool-functionality optimisation that creates new tools (CREATOR, LATM, CRAFT, Alita, CLOVA).
2. **Multi-agent optimisation** (Section 5): four subdimensions.
   - Manually designed paradigms: parallel, hierarchical, debate.
   - Multi-agent prompt optimisation: DSPy Assertions, AutoAgents.
   - Topology optimisation: code-level workflows (AutoFlow, AFlow, ScoreFlow, MAS-GPT) and communication graphs (GPTSwarm, DynaSwarm, G-Designer, MermaidFlow, DyLAN, Captain Agent, Flow, AgentPrune, AGP, G-Safeguard, NetSafe).
   - Unified optimisation jointly over prompts and topology: code-based (ADAS, FlowReasoner), search-based (EvoAgent, EvoFlow, MASS, DebFlow, MAS-ZERO), learning-based (MaAS, ANN).
   - LLM backbone optimisation: reasoning-oriented (multi-agent finetuning, Sirius, MALT, MaPoRL, MARFT, MARTI) and collaboration-oriented (COPPER, OPTIMA).
3. **Domain-specific optimisation** (Section 6): biomedicine (medical diagnosis — MedAgentSim, MDAgents, MDTeamGPT, MMedAgent, MedAgent-Pro; molecular discovery — CACTUS, ChemAgent, OSDA, DrugAgent, LIDDIA), programming (code refinement — Self-Refine, AgentCoder, CodeAgent, CodeCoR, OpenHands; debugging — Self-Debugging, PyCapsule, Self-Collaboration, RGD, FixAgent), and financial / legal research (FinCon, PEER, FinRobot, LawLuo, AgentCourt, LegalGPT).
4. **Evaluation, safety, and ethics**: benchmark-based vs LLM-based evaluation, plus dedicated treatment of safety/alignment/robustness in lifelong evolution settings.

The accompanying **EvoAgentX** open-source framework operationalises the conceptual framework as an executable system.

## Results

As a survey, the paper does not produce numerical results; its deliverables are:

- A **paradigm trajectory** (MOP -> MOA -> MAO -> MASE) that situates dozens of concurrent research threads in one timeline.
- A **unified four-component framework** (Inputs, Agent, Environment, Optimiser) under which every reviewed method can be described by the pair `(search space S, optimisation algorithm H)`.
- The **Three Laws of Self-Evolving AI Agents** as a normative scaffold for ongoing work.
- A **comprehensive taxonomy** spanning single-agent, multi-agent, and domain-specific evolution techniques, organised by which component is being optimised rather than by application area.
- An open-source repository (EvoAgentX) and a curated paper list (Awesome-Self-Evolving-Agents) intended as living artefacts.

## Limitations

- The survey is **broad rather than deep**: each individual technique receives at most a paragraph, so practitioners still need to read primary sources to compare implementations carefully.
- The four-component framework is descriptively powerful but **near-tautological** for any optimisation-based system; it does not yet predict which `(S, H)` choices are likely to succeed for new tasks.
- Coverage is **strongly biased toward 2023-2025 LLM-era work**; classical agent-learning literature (RL agents, evolutionary computation, AutoML) is referenced only via citation, and the relationship between MASE and pre-LLM lifelong-learning work is left implicit.
- The **Three Laws** are stated as priorities but not operationalised — there are no protocols, metrics, or audit mechanisms attached, so the laws function as a research agenda rather than a deployable constraint.
- A concurrent survey (Gao et al. 2025, "what/when/how to evolve") covers overlapping ground; the authors note this but do not perform a systematic side-by-side comparison.

## Open questions

- How do we evaluate self-evolving agents whose target distribution itself is non-stationary? Static benchmarks under-represent the lifelong setting.
- Can the search space `S` be co-optimised across components (LLM + prompts + memory + topology) without combinatorial blow-up? Existing "unified" methods (MASS, EvoFlow, MaAS, ANN) only scratch this surface.
- How should regulators (EU AI Act, GDPR) treat agents whose decision logic mutates after deployment? Current legal frameworks assume static models.
- When ground truth is absent (medicine, law, scientific discovery), what feedback signal can drive safe optimisation without rewarding hallucinated successes?
- What are the convergence guarantees of LLM-based optimisers, and how do we detect divergence before it harms users?

## My take

The strongest contribution is the **conceptual framework**, not the taxonomy. Re-describing dozens of papers as `(S, H)` pairs makes it obvious why most "agent optimisation" papers are mutually orthogonal: they pick different `S` (prompts, memory, topology, tool) but reuse the same handful of `H` (RL, evolutionary, MCTS, gradient-style). That observation is genuinely productive — it predicts where the next round of unified-optimisation work has to go (joint `S` across components, paired with sample-efficient `H`).

The **Three Laws** framing is rhetorically clean but currently aspirational. Until somebody supplies concrete safety audits or convergence proofs, "Endure" is a slogan rather than a constraint. That said, naming the priority order (safety > performance > autonomy) is a useful Schelling point for the field.

For a research wiki, this paper's most useful role is as a **map**: it efficiently compresses 200+ recent papers into one navigable taxonomy. We should treat it as the entry point for the [[self-evolving-agents]] topic and follow its citation chains for any specific subarea (prompt optimisation, multi-agent topology, domain-specific evolution).

## Related

- [[self-evolving-agents]] — the topic this survey defines
- [[mase-paradigm]] — the MASE stage and the broader MOP->MOA->MAO->MASE trajectory
- [[agent-optimisation-feedback-loop]] — the four-component (Inputs, Agent, Environment, Optimiser) framework
- [[three-laws-self-evolving-ai-agents]] — Endure / Excel / Evolve as guiding principles
- [[single-llm-matches-multi-agent-debate]] — challenge claim re-framed by the survey as motivation for self-evolving rather than handcrafted multi-agent designs
- [[jinyuan-fang]] — co-first author
- [[zaiqiao-meng]] — corresponding author
