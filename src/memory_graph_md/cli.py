"""Command-line interface for Memory Graph MD."""

import click
import json
from typing import Optional

from .graph_engine import (
    MemoryGraph,
    GraphNode,
    GraphEdge,
    MemoryEntry,
    NodeType,
    RelationshipType
)


@click.group()
@click.version_option(version="0.1.0", prog_name="memory-graph")
def main() -> None:
    """Memory Graph MD - Infinite, structured memory for long-running autonomous agents."""
    pass


@main.command()
@click.option("--name", "-n", default="default", help="Graph name")
def init(name: str) -> None:
    """Initialize memory graph."""
    graph = MemoryGraph(name)
    
    click.echo(f"\n📊 Memory Graph Initialized")
    click.echo("=" * 60)
    click.echo(f"Name: {graph._name}")
    click.echo(f"Nodes: 0")
    click.echo(f"Edges: 0")
    click.echo(f"Entries: 0")


@main.command()
@click.argument("label")
@click.option("--type", "-t", type=click.Choice([
    "entity", "concept", "event", "person", "location",
    "organization", "date", "generic"
]), default="generic", help="Node type")
@click.option("--confidence", "-c", default=0.9, help="Confidence score")
def add_node(label: str, type: str, confidence: float) -> None:
    """Add a node to the memory graph."""
    graph = MemoryGraph()
    
    node_type = NodeType[type.upper()]
    node = graph.add_entity(
        label=label,
        entity_type=node_type,
        properties={"created_by": "cli"},
        confidence=confidence
    )
    
    click.echo(f"\n✅ Node Created!")
    click.echo(f"   ID: {node.node_id}")
    click.echo(f"   Label: {node.label}")
    click.echo(f"   Type: {node.node_type.value}")
    click.echo(f"   Confidence: {node.confidence_score:.2f}")


@main.command()
@click.argument("source_id")
@click.argument("target_id")
@click.option("--rel", "-r", type=click.Choice([
    "related_to", "part_of", "causes", "leads_to",
    "belongs_to", "occurs_at", "occurs_on", "created_by",
    "knows", "works_for", "located_at", "unknown"
]), required=True, help="Relationship type")
def add_edge(source_id: str, target_id: str, rel: str) -> None:
    """Add a relationship edge between nodes."""
    graph = MemoryGraph()
    
    rel_type = RelationshipType[rel.upper()]
    
    edge = graph.add_relationship(
        source_id=source_id,
        target_id=target_id,
        relationship_type=rel_type,
        properties={"created_by": "cli"}
    )
    
    if edge:
        click.echo(f"\n✅ Edge Created!")
        click.echo(f"   ID: {edge.edge_id}")
        click.echo(f"   Source: {source_id[:20]}...")
        click.echo(f"   Target: {target_id[:20]}...")
        click.echo(f"   Relationship: {edge.relationship_type.value}")
    else:
        click.echo(f"\n❌ Failed to add edge")
        click.echo("   Nodes may not exist")


@main.command()
@click.argument("content")
@click.option("--source", "-s", default="cli", help="Source of memory")
@click.option("--confidence", "-c", default=0.85, help="Confidence score")
def add_memory(content: str, source: str, confidence: float) -> None:
    """Add a memory entry to the graph."""
    graph = MemoryGraph()
    
    entry = graph.add_memory_entry(
        content=content,
        source=source,
        confidence=confidence
    )
    
    click.echo(f"\n✅ Memory Entry Created!")
    click.echo(f"   ID: {entry.entry_id}")
    click.echo(f"   Content: {entry.content[:50]}...")
    click.echo(f"   Entities: {len(entry.entity_links)} linked")
    click.echo(f"   Confidence: {entry.confidence_score:.2f}")


@main.command()
@click.argument("node_id")
@click.option("--depth", "-d", default=2, help="Traversal depth")
def neighbors(node_id: str, depth: int) -> None:
    """Get neighboring nodes."""
    graph = MemoryGraph()
    
    neighbors = graph.get_neighbors(node_id, max_depth=depth)
    
    if not neighbors:
        click.echo(f"\nNo neighbors found for {node_id[:20]}...")
        return
    
    click.echo(f"\n🔗 Neighbors of {node_id[:20]}...")
    click.echo("=" * 60)
    
    for neighbor_id, rel_type, distance in neighbors:
        node = graph.get_node(neighbor_id)
        if node:
            click.echo(f"\n  [{distance}] {neighbor_id[:20]}...")
            click.echo(f"    Label: {node.label}")
            click.echo(f"    Type: {node.node_type.value}")
            click.echo(f"    Relationship: {rel_type}")


@main.command()
@click.option("--limit", "-l", default=10, help="Max entries to show")
@click.option("--entity", "-e", help="Filter by entity")
def history(limit: int, entity: str) -> None:
    """Show recent memory entries."""
    graph = MemoryGraph()
    
    entries = graph.get_recent_entries(limit, entity_filter=entity)
    
    if not entries:
        click.echo("\nNo memory entries found")
        return
    
    click.echo(f"\n📝 Recent Memory Entries ({len(entries)})")
    click.echo("=" * 60)
    
    for entry in entries:
        click.echo(f"\n  {entry.entry_id[:20]}...")
        click.echo(f"  Content: {entry.content[:50]}...")
        click.echo(f"  Entities: {len(entry.entity_links)}")
        click.echo(f"  Timestamp: {entry.timestamp.strftime('%Y-%m-%d %H:%M')}")


@main.command()
@click.argument("query")
@click.option("--type", "-t", type=click.Choice([
    "entity", "concept", "event", "person", "location",
    "organization", "date", "generic"
]), help="Entity type filter")
def search(query: str, type: Optional[str]) -> None:
    """Search for entities."""
    graph = MemoryGraph()
    
    entity_type = NodeType[type.upper()] if type else None
    
    results = graph.search_entities(query, entity_type=entity_type)
    
    if not results:
        click.echo(f"\nNo results found for: {query}")
        return
    
    click.echo(f"\n🔍 Search Results for '{query}'")
    click.echo("=" * 60)
    
    for node in results:
        click.echo(f"\n  {node.node_id[:20]}...")
        click.echo(f"  Label: {node.label}")
        click.echo(f"  Type: {node.node_type.value}")
        click.echo(f"  Confidence: {node.confidence_score:.2f}")


@main.command()
def stats() -> None:
    """Show graph statistics."""
    graph = MemoryGraph()
    
    stats = graph.get_statistics()
    
    click.echo(f"\n📊 Memory Graph Statistics")
    click.echo("=" * 60)
    click.echo(f"Graph Name: {stats['graph_name']}")
    click.echo(f"Total Nodes: {stats['total_nodes']}")
    click.echo(f"Total Edges: {stats['total_edges']}")
    click.echo(f"Total Entries: {stats['total_entries']}")
    
    if stats['entity_types']:
        click.echo(f"\nEntity Types:")
        for etype, count in stats['entity_types'].items():
            click.echo(f"  • {etype}: {count}")
    
    if stats['relationship_types']:
        click.echo(f"\nRelationship Types:")
        for rtype, count in stats['relationship_types'].items():
            click.echo(f"  • {rtype}: {count}")


@main.command()
def demo() -> None:
    """Run a memory graph demo."""
    click.echo("\n🧪 Memory Graph Demo")
    click.echo("=" * 60)
    
    graph = MemoryGraph("demo_graph")
    
    # Add entities
    click.echo("\n📝 Adding Entities...")
    
    alice = graph.add_entity(
        label="Alice Smith",
        entity_type=NodeType.PERSON,
        properties={"age": 30, "occupation": "Engineer"},
        confidence=0.95
    )
    
    google = graph.add_entity(
        label="Google",
        entity_type=NodeType.ORGANIZATION,
        properties={"industry": "Technology"},
        confidence=0.98
    )
    
    san_francisco = graph.add_entity(
        label="San Francisco",
        entity_type=NodeType.LOCATION,
        properties={"country": "USA"},
        confidence=0.99
    )
    
    # Add relationships
    click.echo("\n🔗 Adding Relationships...")
    
    graph.add_relationship(
        alice.node_id,
        google.node_id,
        RelationshipType.WORKS_FOR,
        properties={"since": "2020"}
    )
    
    graph.add_relationship(
        alice.node_id,
        san_francisco.node_id,
        RelationshipType.LOCATED_AT,
        properties={"since": "2019"}
    )
    
    # Add memory entries
    click.echo("\n📖 Adding Memories...")
    
    memory1 = graph.add_memory_entry(
        content="Alice started working at Google in 2020",
        source="conversation",
        confidence=0.90
    )
    
    memory2 = graph.add_memory_entry(
        content="Alice lives in San Francisco since 2019",
        source="conversation",
        confidence=0.95
    )
    
    # Show graph stats
    click.echo("\n📊 Graph Statistics:")
    stats = graph.get_statistics()
    click.echo(f"  Nodes: {stats['total_nodes']}")
    click.echo(f"  Edges: {stats['total_edges']}")
    click.echo(f"  Entries: {stats['total_entries']}")
    
    # Show neighbors
    click.echo(f"\n🔗 Neighbors of Alice:")
    neighbors = graph.get_neighbors(alice.node_id, max_depth=1)
    for neighbor_id, rel_type, dist in neighbors:
        node = graph.get_node(neighbor_id)
        if node:
            click.echo(f"  • {node.label} ({rel_type})")
    
    # Show recent entries
    click.echo(f"\n📝 Recent Memories:")
    entries = graph.get_recent_entries(2)
    for entry in entries:
        click.echo(f"  • {entry.content[:40]}...")


def main_entry() -> None:
    """Main entry point."""
    main(prog_name="memory-graph")


if __name__ == "__main__":
    main_entry()
