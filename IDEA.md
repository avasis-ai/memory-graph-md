# Memory-Graph.md (#43)

## Tagline
Infinite, structured memory for long-running autonomous agents.

## What It Does
Replacing flat, easily confused vector databases with dynamic knowledge graphs, this SKILL.md extension dictates how the agent extracts entities and relationships from conversations. It builds a local graph allowing the agent to remember complex facts accurately over years of use.

## Inspired By
Neo4j, LlamaIndex, Mem0 + Knowledge Graphs

## Viral Potential
Solves the notorious goldfish memory problem of current LLM agents. Highly visual, interactive graph interfaces look incredible in demos. Essential for personal AI assistants (like OpenClaw).

## Unique Defensible Moat
A localized, ultra-fast graph traversal algorithm injects relevant sub-graphs directly into the LLM context window in under 10 milliseconds, a speed generic graph databases cannot achieve.

## Repo Starter Structure
/graph-engine, /memory-manager, Apache 2.0, local visualizer UI

## Metadata
- **License**: Apache-2.0
- **Org**: avasis-ai
- **PyPI**: memory-graph-md
- **Dependencies**: networkx>=3.0, pyyaml>=6.0, click>=8.0
